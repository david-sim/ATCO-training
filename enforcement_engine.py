"""
Core smart compliance operations processing engine.
Contains the main address processing logic without UI dependencies.
"""
import datetime
import re
import pandas as pd
import io
import json
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
from pydantic import BaseModel, Field
from search_service import google_search_entity
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from csv_processor import process_csv_with_validation, create_csv_for_download, CSVValidationError


# Global cache for multi-unit snippets across processing sessions
_multi_unit_cache: Dict[str, List[Dict[str, str]]] = {}

# Global cache for compliance assessments across processing sessions
_compliance_cache: Dict[str, Dict[str, str]] = {}


class OccupantResult(BaseModel):
    """Structured result for occupant identification analysis."""
    matched_snippet: str = Field(description="Relevant snippets that match the address with sources and credibility")
    multiple_units_snippet: str = Field(description="Matched snippet(s) which suggests that occupant occupies multiple units (e.g. #01-01/02, #01-03 and 04, etc.) in the address, -url, -label credible/non-credible source and -source date OR NA, if none")
    reasoning: str = Field(description="Detailed reasoning for the occupant selection decision")
    confirmed_occupant: str = Field(description="The confirmed occupant name or 'Need more information'")
    business_summary: str = Field(description="Summary of the core and other business activities of the selected occupant")


class ComplianceResult(BaseModel):
    """Structured result for compliance assessment analysis."""
    compliance_level: str = Field(description="The compliance level: Unauthorised Use / Authorised Use / Likely Authorised Use / Likely Unauthorised Use / Need more information")
    rationale: str = Field(description="Detailed rationale explaining the compliance level determination")


def create_compliance_cache_key(occupant: str, primary_approved_use: str, secondary_approved_use: str, address_type: str) -> str:
    """
    Create a unique cache key for compliance assessments.
    
    Args:
        occupant: Confirmed occupant name
        primary_approved_use: Primary approved use for the address
        secondary_approved_use: Secondary approved use for the address
        address_type: Type of address processing
    
    Returns:
        Unique cache key string
    """
    # Normalize strings to handle case variations and extra spaces
    occupant_clean = occupant.strip().lower() if occupant else ""
    primary_clean = primary_approved_use.strip().lower() if primary_approved_use else ""
    secondary_clean = secondary_approved_use.strip().lower() if secondary_approved_use else ""
    address_type_clean = address_type.strip().lower() if address_type else ""
    
    # Create composite key
    cache_key = f"{occupant_clean}|{primary_clean}|{secondary_clean}|{address_type_clean}"
    return cache_key


def store_compliance_assessment(occupant: str, primary_approved_use: str, secondary_approved_use: str, 
                               address_type: str, compliance_level: str, rationale: str) -> None:
    """
    Store compliance assessment for future reference when same occupant is encountered.
    
    Args:
        occupant: Confirmed occupant name
        primary_approved_use: Primary approved use for the address
        secondary_approved_use: Secondary approved use for the address
        address_type: Type of address processing
        compliance_level: Determined compliance level
        rationale: Detailed rationale for the compliance assessment
    """
    if not occupant or occupant in ["Need more information", "Analysis not available"]:
        print(f"❌ [COMPLIANCE-CACHE] Not storing assessment for invalid occupant: '{occupant}'")
        return  # Don't cache assessments for unidentified occupants
    
    cache_key = create_compliance_cache_key(occupant, primary_approved_use, secondary_approved_use, address_type)
    
    _compliance_cache[cache_key] = {
        "occupant": occupant,
        "primary_approved_use": primary_approved_use,
        "secondary_approved_use": secondary_approved_use,
        "address_type": address_type,
        "compliance_level": compliance_level,
        "rationale": rationale,
        "cached_at": datetime.datetime.now().isoformat()
    }
    
    print(f"💾 [COMPLIANCE-CACHE] ✅ Stored assessment for '{occupant}'")
    print(f"    🏢 Uses: {primary_approved_use} / {secondary_approved_use}")
    print(f"    📊 Level: {compliance_level}")
    print(f"    🔑 Cache key: {cache_key[:50]}...")
    print(f"    📈 Cache size: {len(_compliance_cache)} entries")
    
    # Keep cache size manageable (max 100 entries)
    if len(_compliance_cache) > 100:
        # Remove oldest 20 entries (simple LRU-like behavior)
        oldest_keys = list(_compliance_cache.keys())[:20]
        for key in oldest_keys:
            del _compliance_cache[key]
        print(f"🧹 [COMPLIANCE-CACHE] Cache trimmed - removed {len(oldest_keys)} oldest entries")


def get_cached_compliance_assessment(occupant: str, primary_approved_use: str, secondary_approved_use: str, 
                                   address_type: str) -> Optional[Dict[str, str]]:
    """
    Retrieve cached compliance assessment for the same occupant with same approved uses.
    
    Args:
        occupant: Confirmed occupant name
        primary_approved_use: Primary approved use for the address
        secondary_approved_use: Secondary approved use for the address
        address_type: Type of address processing
    
    Returns:
        Cached compliance assessment dict or None if not found
    """
    if not occupant or occupant in ["Need more information", "Analysis not available"]:
        print(f"❌ [COMPLIANCE-CACHE] Cannot retrieve cache for invalid occupant: '{occupant}'")
        return None
    
    cache_key = create_compliance_cache_key(occupant, primary_approved_use, secondary_approved_use, address_type)
    
    if cache_key in _compliance_cache:
        cached_assessment = _compliance_cache[cache_key]
        print(f"✅ [COMPLIANCE-CACHE] 🎯 Cache HIT for '{occupant}'")
        print(f"    🏢 Uses: {primary_approved_use} / {secondary_approved_use}")
        print(f"    📊 Cached level: {cached_assessment.get('compliance_level', 'Unknown')}")
        print(f"    📅 Cached at: {cached_assessment.get('cached_at', 'Unknown')}")
        print(f"    🔑 Cache key: {cache_key[:50]}...")
        return cached_assessment
    
    print(f"❌ [COMPLIANCE-CACHE] 🎯 Cache MISS for '{occupant}'")
    print(f"    🏢 Uses: {primary_approved_use} / {secondary_approved_use}")
    print(f"    🔑 Looking for key: {cache_key[:50]}...")
    print(f"    📊 Current cache size: {len(_compliance_cache)} entries")
    return None


def check_multi_unit_occupant_match(current_address: str, current_occupant: str) -> bool:
    """
    Check if the current occupant matches any occupant in the multi-unit cache for the same base address.
    This helps identify when the same occupant occupies multiple units.
    
    Args:
        current_address: The address currently being processed
        current_occupant: The occupant identified for current address
    
    Returns:
        True if occupant matches existing multi-unit data, False otherwise
    """
    if not current_occupant or current_occupant in ["Need more information", "Analysis not available"]:
        return False
    
    base_address = extract_base_address(current_address)
    
    if base_address not in _multi_unit_cache or not _multi_unit_cache[base_address]:
        return False
    
    # Normalize occupant name for comparison
    current_occupant_clean = current_occupant.strip().lower()
    
    for entry in _multi_unit_cache[base_address]:
        cached_occupant_clean = entry["occupant"].strip().lower()
        if cached_occupant_clean == current_occupant_clean:
            print(f"🔗 [MULTI-UNIT-MATCH] Found matching occupant '{current_occupant}' in cache for base address '{base_address}'")
            return True
    
    return False


def parse_json_response(response: str) -> Optional[dict]:
    """
    Parse JSON response from LLM with robust error handling.
    
    Args:
        response: Raw LLM response string
        
    Returns:
        Parsed JSON dict or None if parsing fails
    """
    try:
        # Clean the response - remove leading/trailing whitespace
        response = response.strip()
        
        # Handle potential code block markers
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        
        response = response.strip()
        
        # Parse JSON
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error parsing JSON: {e}")
        return None


def remove_postal_code(address):
    """
    Remove postal code from Singapore address.
    Handles various postal code formats: 'Singapore 123456', 'S 123456', or just '123456'.
    
    Args:
        address: The original address string
        
    Returns:
        Address string without postal code
    """
    # Remove 'Singapore XXXXXX' pattern
    address = re.sub(r'\s+Singapore\s+\d{6}$', '', address, flags=re.IGNORECASE)
    
    # Remove 'S XXXXXX' pattern  
    address = re.sub(r'\s+S+\d{6}$', '', address, flags=re.IGNORECASE)
    
    # Remove standalone 6-digit postal code at the end
    address = re.sub(r'\s+\d{6}$', '', address)
    
    return address.strip()


def generate_variant(address):
    """
    Generate a variant address format for shophouse addresses.
    Converts between unit notation (#01-XX) and suffix notation (A, B, C, D).
    
    Args:
        address: The original address string
        
    Returns:
        Variant address string or None if no conversion is possible
    """
    unit_pattern = re.match(r"^(\d+)\s+(.*)\s+#(0[1-5])-\d{2}\s+(Singapore\s+\d{6})$", address)
    if unit_pattern:
        block = unit_pattern.group(1)
        street = unit_pattern.group(2).strip()
        floor = unit_pattern.group(3)
        postal = unit_pattern.group(4)

        floor_to_suffix = {"01" : "", "02": "A", "03": "B", "04": "C", "05": "D"}
        suffix = floor_to_suffix.get(floor)
        if suffix:
            return f"{block}{suffix} {street} {postal}"
        else:
            return None

    suffix_pattern = re.match(r"^(\d+)([A-D])\s+(.*)\s+(Singapore\s+\d{6})$", address)
    if suffix_pattern:
        block = suffix_pattern.group(1)
        suffix = suffix_pattern.group(2)
        street = suffix_pattern.group(3).strip()
        postal = suffix_pattern.group(4)

        suffix_to_floor = {"A": "02", "B": "03", "C": "04", "D": "05"}
        floor = suffix_to_floor.get(suffix)
        if floor:
            return f"{block} {street} #{floor}-01 {postal}"
        else:
            return None

    return None


def get_occupant_rules(address_type: str = "industrial") -> str:
    """Get occupant rules from config based on address type, with fallback for testing"""
    try:
        from config_manager import (
            get_shophouse_occupant_rules, 
            get_industrial_occupant_rules
        )
        if address_type.lower() == "shophouse":
            return get_shophouse_occupant_rules()
        else:
            return get_industrial_occupant_rules()
    except Exception as e:
        print(f"⚠️ Could not load occupant rules from config: {e}")
        return ""


def get_compliance_rules(address_type: str = "industrial") -> str:
    """Get compliance rules from config based on address type, with fallback for testing"""
    try:
        from config_manager import (
            get_shophouse_compliance_rules, 
            get_industrial_compliance_rules
        )
        if address_type.lower() == "shophouse":
            return get_shophouse_compliance_rules()
        else:
            return get_industrial_compliance_rules()
    except Exception as e:
        print(f"⚠️ Could not load compliance rules from config: {e}")
        return ""


def extract_base_address(address: str) -> str:
    """
    Extract base address for similarity matching (remove unit numbers).
    
    Args:
        address: Full address string
    
    Returns:
        Base address without unit specifics
    """
    print(f"🔍 [MULTI-UNIT] Extracting base address from: {address}")
    
    # Remove common unit patterns
    base_address = re.sub(r'#\d+-\d+', '', address)  # Remove #01-05 patterns
    base_address = re.sub(r'Unit \d+-\d+', '', base_address, flags=re.IGNORECASE)  # Remove Unit patterns
    base_address = re.sub(r'Level \d+', '', base_address, flags=re.IGNORECASE)  # Remove Level patterns
    base_address = re.sub(r'\b\d+[A-Z]\b', '', base_address)  # Remove block suffixes like 69A
    base_address = re.sub(r'\s+', ' ', base_address).strip()  # Clean whitespace
    
    print(f"✅ [MULTI-UNIT] Base address extracted: '{base_address}'")
    return base_address


def store_multi_unit_data(address: str, occupant: str, multiple_units_snippet: str) -> None:
    """
    Store multi-unit snippet data for future reference.
    
    Args:
        address: Current address being processed
        occupant: Confirmed occupant name
        multiple_units_snippet: Snippet containing multiple unit information
    """
    print(f"💾 [MULTI-UNIT] Attempting to store data for: {address}")
    print(f"    Occupant: {occupant}")
    print(f"    Snippet length: {len(multiple_units_snippet) if multiple_units_snippet else 0} chars")
    
    if multiple_units_snippet and multiple_units_snippet.strip() not in ["NA", "N/A", ""]:
        base_address = extract_base_address(address)
        
        if base_address not in _multi_unit_cache:
            _multi_unit_cache[base_address] = []
            print(f"📝 [MULTI-UNIT] Created new cache entry for base address: '{base_address}'")
        
        # Avoid duplicates
        new_entry = {
            "occupant": occupant,
            "snippet": multiple_units_snippet,
            "source_address": address,
        }
        
        # Check if similar entry already exists
        for entry in _multi_unit_cache[base_address]:
            if entry["occupant"] == occupant and entry["snippet"] == multiple_units_snippet:
                print(f"⚠️ [MULTI-UNIT] Duplicate entry detected, skipping storage")
                return  # Skip duplicate
        
        _multi_unit_cache[base_address].append(new_entry)
        print(f"✅ [MULTI-UNIT] Stored multi-unit data. Cache now has {len(_multi_unit_cache[base_address])} entries for '{base_address}'")
        
        # Keep cache size manageable (max 10 entries per base address)
        if len(_multi_unit_cache[base_address]) > 10:
            _multi_unit_cache[base_address] = _multi_unit_cache[base_address][-10:]
            print(f"🧹 [MULTI-UNIT] Cache trimmed to 10 entries for '{base_address}'")
    else:
        print(f"❌ [MULTI-UNIT] No valid multi-unit snippet to store (empty or NA)")
        base_address = extract_base_address(address)
        
        if base_address not in _multi_unit_cache:
            _multi_unit_cache[base_address] = []
        
        # Avoid duplicates
        new_entry = {
            "occupant": occupant,
            "snippet": multiple_units_snippet,
            "source_address": address,
        }
        
        # Check if similar entry already exists
        for entry in _multi_unit_cache[base_address]:
            if entry["occupant"] == occupant and entry["snippet"] == multiple_units_snippet:
                return  # Skip duplicate
        
        _multi_unit_cache[base_address].append(new_entry)
        
        # Keep cache size manageable (max 10 entries per base address)
        if len(_multi_unit_cache[base_address]) > 10:
            _multi_unit_cache[base_address] = _multi_unit_cache[base_address][-10:]


def get_relevant_multi_unit_data(current_address: str) -> str:
    """
    Get relevant multi-unit data from previous processing for the current address.
    
    Args:
        current_address: The address currently being processed
    
    Returns:
        Formatted string of relevant multi-unit snippets or "No relevant multi-unit data available"
    """
    print(f"🔍 [MULTI-UNIT] Searching for relevant data for: {current_address}")
    base_address = extract_base_address(current_address)
    
    if base_address not in _multi_unit_cache or not _multi_unit_cache[base_address]:
        print(f"❌ [MULTI-UNIT] No cached data found for base address: '{base_address}'")
        return "No relevant multi-unit data available"
    
    print(f"✅ [MULTI-UNIT] Found {len(_multi_unit_cache[base_address])} cached entries for '{base_address}'")
    
    relevant_snippets = []
    for i, entry in enumerate(_multi_unit_cache[base_address]):
        print(f"    📄 Entry {i+1}: {entry['occupant']} from {entry['source_address']}")
        snippet_info = f"""
Previous Record: {entry['source_address']}
Occupant: {entry['occupant']}
Multi-Unit Snippet: {entry['snippet']}
---"""
        relevant_snippets.append(snippet_info)
    
    if relevant_snippets:
        result = f"Relevant multi-unit data from previous processing:\n" + "\n".join(relevant_snippets)
        print(f"🎯 [MULTI-UNIT] Returning {len(relevant_snippets)} relevant snippets")
        return result
    
    print(f"❌ [MULTI-UNIT] No relevant snippets found")
    return "No relevant multi-unit data available"


def clear_multi_unit_cache() -> None:
    """Clear the multi-unit cache. Useful for starting fresh processing sessions."""
    global _multi_unit_cache
    cache_size_before = len(_multi_unit_cache)
    total_entries_before = sum(len(entries) for entries in _multi_unit_cache.values())
    
    print(f"🧹 [MULTI-UNIT] Clearing cache: {cache_size_before} addresses with {total_entries_before} total entries")
    _multi_unit_cache.clear()
    print(f"✅ [MULTI-UNIT] Cache cleared successfully")


def get_multi_unit_cache_stats() -> Dict[str, int]:
    """
    Get statistics about the multi-unit cache.
    
    Returns:
        Dictionary with cache statistics
    """
    total_addresses = len(_multi_unit_cache)
    total_entries = sum(len(entries) for entries in _multi_unit_cache.values())
    cache_size = len(str(_multi_unit_cache))
    
    print(f"📊 [MULTI-UNIT] Cache Stats: {total_addresses} addresses, {total_entries} entries, {cache_size} bytes")
    
    return {
        "cached_addresses": total_addresses,
        "total_multi_unit_entries": total_entries,
        "cache_size_bytes": cache_size
    }


def process_csv(command: str, csv_file) -> Dict[str, List[str]]:
    """
    Process the uploaded CSV file based on the command ("shophouse" or "industrial").
    This function now uses the modular csv_processor for validation and processing.

    Args:
        command: The command, either "shophouse" or "industrial"
        csv_file: The uploaded CSV file object

    Returns:
        Dictionary containing the processed data
        
    Raises:
        CSVValidationError: If CSV validation fails
        ValueError: If command is invalid
    """
    try:
        return process_csv_with_validation(command, csv_file)
    except CSVValidationError as e:
        # Convert CSV validation errors to ValueError for backward compatibility
        raise ValueError(f"CSV validation failed: {str(e)}")


def process_single_address(address: str, llm: Any, primary_approved_use: str = "", secondary_approved_use: str = "", address_type: str = "industrial", progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, str]:
    """
    Process a single address through the complete enforcement workflow.
    
    Args:
        address: Address to process
        llm: Language model instance
        primary_approved_use: Primary approved use for the address
        secondary_approved_use: Secondary approved use for the address
        address_type: Type of address processing ("shophouse" or "industrial")
        progress_callback: Optional callback function for progress updates
    
    Returns:
        Processing result with all required fields
    """
    def log_progress(message: str) -> None:
        if progress_callback:
            progress_callback(message)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}")

    log_progress(f"📍 Processing {address}")
    
    # Clean the address - remove any extra data that might be semicolon-separated
    clean_address = address.split(';')[0].strip() if ';' in address else address.strip()
    
    if clean_address != address:
        log_progress(f"🧹 Cleaned address: '{address}' → '{clean_address}'")
    
    # Initialize variables
    address_search_results_raw = ""
    address_search_results_raw_variant = ""
    confirmed_occupant_google_search_results = ""
    verified_occupant_response = ""
    verification_analysis = ""
    confirmed_occupant = ""
    business_summary = ""
    compliance_level = "Need more information"
    rationale = "Unable to confirm occupant, compliance assessment not performed."
    
    # Get system rules based on address type
    occupant_rules = get_occupant_rules(address_type)
    compliance_rules = get_compliance_rules(address_type)
    today = datetime.date.today().isoformat()
    
    # Step 1: Google search for address
    log_progress(f"🔍 Searching for address information...")
    
    try:
        # Original address search - use cleaned address
        address_search_query = f"{clean_address}"
        
        # Debug: Show what we're actually searching for
        log_progress(f"🔎 Searching with cleaned address: '{clean_address}'")
        if clean_address != address:
            log_progress(f"🔄 Original was: '{address}'")
        
        address_search_results_raw = google_search_entity(address_search_query)
        
        # Variant address search - different logic for shophouse vs industrial
        if address_type.lower() == "shophouse":
            # For shophouse, try to generate an address format variant
            variant_address = generate_variant(clean_address)
            if variant_address:
                address_search_query_variant = variant_address
                log_progress(f"🔄 Generated shophouse variant: '{variant_address}'")
            else:
                # Fallback to standard variant if no format conversion possible
                address_search_query_variant = f"{clean_address}"
                log_progress(f"🔄 Using fallback variant for shophouse: 'address {clean_address}'")
        else:
            # For industrial, use address without postal code
            clean_address_no_postal = remove_postal_code(clean_address)
            address_search_query_variant = f"{clean_address_no_postal}"
            print(f"🔄 Using industrial address variant: '{address_search_query_variant}'")

        address_search_results_raw_variant = google_search_entity(address_search_query_variant)

        # Check if searches failed
        if address_search_results_raw is None:
            address_search_results_raw = "No address search results available"
        
        if address_search_results_raw_variant is None:
            address_search_results_raw_variant = "No variant address search results available"
        
        # Log success if at least one search succeeded
        if (address_search_results_raw != "No address search results available" or 
            address_search_results_raw_variant != "No variant address search results available"):
            log_progress(f"✅ Address search completed")
        else:
            log_progress(f"❌ Both address searches failed")
            
    except Exception as search_error:
        log_progress(f"❌ Address search error: {str(search_error)}")
        address_search_results_raw = f"Address search failed: {str(search_error)}"
        address_search_results_raw_variant = f"Variant address search failed: {str(search_error)}"
    
    # Step 2: LLM Analysis for occupant identification
    log_progress(f"🤖 Analysing occupant...")
    
    # Get relevant multi-unit data from previous processing
    address_multiple_units = get_relevant_multi_unit_data(address)
    
    # Define JSON structure outside f-string to avoid template variable conflicts
    occupant_json_structure = """{{
    "matched_snippet": "Quote the relevant snippets that match the address, including URL and source credibility assessment",
    "multiple_units_snippet": "Matched snippet(s) which suggests that occupant occupies multiple units (e.g. #01-01/02, #01-03 and 04, etc.) in the address, -url, -label credible/non-credible source and -source date OR NA, if none",
    "reasoning": "Show your responses for each step. Why that entity was chosen, or why no match could be confirmed",
    "confirmed_occupant": "Business name from snippets or 'Need more information'",
    "business_summary": "Summarize the core and other business activities of the selected occupant"
}}"""
    
    occupant_prompt = f"""Today's date is {today}
Identify the current occupant of: {address} using the search results below.

<google_search_results_original>
{address_search_results_raw}
</google_search_results_original>

<google_search_results_variant>
{address_search_results_raw_variant}
</google_search_results_variant>

<multi_units_google_snippets>
{address_multiple_units}
</multi_units_google_snippets>

---

Use the information above and follow the step-by-step instructions in the system prompt and provide your analysis in the following JSON structure:
{occupant_json_structure}
"""

    # Create ChatPromptTemplate with system rules and human prompt
    occupant_chat_prompt = ChatPromptTemplate.from_messages([
        ("system", occupant_rules),
        ("human", occupant_prompt)
    ])

    # Create structured LLM chain
    structured_llm = llm.with_structured_output(OccupantResult)
    occupant_chain = occupant_chat_prompt | structured_llm

    try:
        occupant_result = occupant_chain.invoke({})
        log_progress(f"✅ Occupant analysis completed")
        
        confirmed_occupant = occupant_result.confirmed_occupant
        
        # Print and log confirmed occupant details for monitoring
        occupant_details = f"🏢 CONFIRMED OCCUPANT: {confirmed_occupant}"
        print(f"\n{'='*60}")
        print(f"📍 ADDRESS: {address}")
        print(f"🏢 CONFIRMED OCCUPANT: {confirmed_occupant}")
        if hasattr(occupant_result, 'matched_snippet') and occupant_result.matched_snippet:
            print(f"🔍 MATCHED SNIPPET: {occupant_result.matched_snippet}")
        if hasattr(occupant_result, 'business_summary') and occupant_result.business_summary:
            print(f"📝 BUSINESS SUMMARY: {occupant_result.business_summary}")
        if hasattr(occupant_result, 'reasoning') and occupant_result.reasoning:
            print(f"🧠 REASONING: {occupant_result.reasoning}")
        print(f"{'='*60}\n")
        
        # Log to progress callback for UI display
        log_progress(f"🏢 Occupant identified: {confirmed_occupant}")
        
        verification_analysis = f"Matched Snippets: {occupant_result.matched_snippet}\n\nBusiness Summary: {occupant_result.business_summary}\n\nReasoning: {occupant_result.reasoning}"
        
        # Store multi-unit data for future reference if found
        if hasattr(occupant_result, 'multiple_units_snippet'):
            store_multi_unit_data(address, confirmed_occupant, occupant_result.multiple_units_snippet)
        
    except Exception as llm_error:
        log_progress(f"❌ Analysis failed: {str(llm_error)}")
        confirmed_occupant = "Analysis not available"
        verification_analysis = f"LLM analysis failed: {str(llm_error)}"

    # Step 3: Compliance assessment if occupant is identified
    if confirmed_occupant == "Need more information":
        compliance_level = "Not Applicable"
        rationale = "Unable to confirm occupant, compliance assessment not performed."
        confirmed_occupant_google_search_results = "No occupant identified for search"
    else:
        log_progress(f"🔍 Searching for occupant information...")

        # Google Search for Occupant
        try:
            confirmed_occupant_google_search_results = google_search_entity(confirmed_occupant)
            
            if confirmed_occupant_google_search_results is None:
                confirmed_occupant_google_search_results = "No occupant search results available"
                log_progress(f"⚠️ Occupant search failed")
            else:
                log_progress(f"✅ Occupant search completed")
                    
        except Exception as search_error:
            confirmed_occupant_google_search_results = f"Occupant search failed: {str(search_error)}"
            log_progress(f"⚠️ Occupant search failed")

        business_summary = occupant_result.business_summary if hasattr(occupant_result, 'business_summary') else "No business summary available"

        # Check for cached compliance assessment before performing new analysis
        log_progress(f"🔍 Checking compliance cache...")
        cached_assessment = get_cached_compliance_assessment(
            confirmed_occupant, primary_approved_use, secondary_approved_use, address_type
        )
        
        if cached_assessment:
            # Use cached assessment
            compliance_level = cached_assessment["compliance_level"]
            rationale = cached_assessment["rationale"]
            log_progress(f"✅ Using cached compliance assessment")
        else:
            # Perform new compliance assessment
            log_progress(f"⚖️ Assessing compliance...")
            
            # Define JSON structure outside f-string to avoid template variable conflicts
            compliance_json_structure = """{{
    "compliance_level": "One of: Unauthorised Use, Authorised Use, Likely Authorised Use, Likely Unauthorised Use, Need more information",
    "rationale": "Show your responses for each step. Detailed rationale for compliance level with specific references to B1 use categories"
}}"""
            
            compliance_prompt = f"""Assess the occupant's operations based on the following information:

Selected Occupant: {confirmed_occupant}

Occupant's Address: {address}

Google Search Result of Occupant's name: {confirmed_occupant_google_search_results}
Business Summary: {business_summary}

Evaluate whether the occupant's use of the space (e.g. using space as retail display/showroom of motor vehicles is permissible) is reasonably aligned with the approved use based on standard land use interpretations in Singapore.

Primary approved use: {primary_approved_use}
Secondary approved use: {secondary_approved_use}

---

Provide your assessment in the following JSON structure:
{compliance_json_structure}
"""

            # Create ChatPromptTemplate with system rules and human prompt
            compliance_chat_prompt = ChatPromptTemplate.from_messages([
                ("system", compliance_rules),
                ("human", compliance_prompt)
            ])

            # Create structured LLM chain
            structured_compliance_llm = llm.with_structured_output(ComplianceResult)
            compliance_chain = compliance_chat_prompt | structured_compliance_llm

            try:
                compliance_result = compliance_chain.invoke({})
                log_progress(f"✅ Compliance assessment completed")
                
                compliance_level = compliance_result.compliance_level
                rationale = compliance_result.rationale
                
                # Store the assessment in cache for future use
                store_compliance_assessment(
                    confirmed_occupant, primary_approved_use, secondary_approved_use, 
                    address_type, compliance_level, rationale
                )
                
            except Exception as compliance_error:
                log_progress(f"❌ Compliance assessment failed")
                compliance_level = "Assessment failed"
                rationale = f"Compliance assessment failed: {str(compliance_error)}"
    
    # Individual address processing completed - no need for separate log since batch completion will be logged
    
    return {
        'address': address,
        'confirmed_occupant': confirmed_occupant,
        'verification_analysis': verification_analysis,
        'primary_approved_use': primary_approved_use,
        'secondary_approved_use': secondary_approved_use,
        'compliance_level': compliance_level,
        'rationale': rationale,
        'google_address_search_results': address_search_results_raw if address_search_results_raw else "N/A",
        'google_address_search_results_variant': address_search_results_raw_variant if address_search_results_raw_variant else "N/A",
        'confirmed_occupant_google_search_results': confirmed_occupant_google_search_results if confirmed_occupant_google_search_results else "N/A"
    }


def process_addresses_batch(addresses, llm, primary_approved_use_list=None, secondary_approved_use_list=None, address_type="industrial", progress_callback=None):
    """
    Process multiple addresses in batch.
    
    Args:
        addresses: List of addresses to process
        llm: Language model instance
        primary_approved_use_list: List of primary approved uses (same length as addresses)
        secondary_approved_use_list: List of secondary approved uses (same length as addresses)
        address_type: Type of address processing ("shophouse" or "industrial")
        progress_callback: Optional callback function for progress updates
    
    Returns:
        Tuple of (results_list, csv_buffer)
    """
    try:
        results = []
        total_addresses = len(addresses)
        
        # Clear multi-unit cache for fresh batch processing
        # This ensures we start with a clean slate for each new batch
        clear_multi_unit_cache()
        if progress_callback:
            progress_callback("🔄 Multi-unit cache cleared for fresh processing")
        
        # Handle default values for approved use lists
        if primary_approved_use_list is None:
            primary_approved_use_list = [""] * len(addresses)
        if secondary_approved_use_list is None:
            secondary_approved_use_list = [""] * len(addresses)
        
        def batch_progress_callback(message):
            if progress_callback:
                progress_callback(message, current_index=len(results) + 1, total=total_addresses)
        
        for i, address in enumerate(addresses):
            try:
                # Get the corresponding approved uses for this address
                primary_use = primary_approved_use_list[i] if i < len(primary_approved_use_list) else ""
                secondary_use = secondary_approved_use_list[i] if i < len(secondary_approved_use_list) else ""
                
                result = process_single_address(address, llm, primary_use, secondary_use, address_type, batch_progress_callback)
                results.append([
                    result['address'],
                    result['confirmed_occupant'],
                    result['verification_analysis'],
                    result['primary_approved_use'],
                    result['secondary_approved_use'],
                    result['compliance_level'],
                    result['rationale'],
                    result['google_address_search_results'],
                    result['google_address_search_results_variant'],
                    result['confirmed_occupant_google_search_results']
                ])
            except Exception as e:
                error_msg = f"❌ Error processing {address}: {str(e)}"
                if progress_callback:
                    progress_callback(error_msg, current_index=i+1, total=total_addresses)
                
                # Add error result to maintain structure
                primary_use = primary_approved_use_list[i] if i < len(primary_approved_use_list) else ""
                secondary_use = secondary_approved_use_list[i] if i < len(secondary_approved_use_list) else ""
                
                results.append([
                    address,
                    "Error",
                    str(e),
                    primary_use,
                    secondary_use,
                    "Unknown",
                    f"Processing failed: {str(e)}",
                    "N/A",
                    "N/A",
                    "N/A"
                ])
    
        if progress_callback:
            progress_callback(f"🎉 Completed processing {len(results)} address(es)!")
        
        # Create CSV buffer
        csv_buffer = create_csv_for_download(results)
        
        # Debug: Ensure we're not returning None
        print(f"🔍 Debug: About to return results={type(results)}, csv_buffer={type(csv_buffer)}")
        
        return results, csv_buffer
        
    except Exception as e:
        # If any error occurs in the entire batch processing, return error results
        print(f"❌ Critical error in batch processing: {str(e)}")
        if progress_callback:
            progress_callback(f"❌ Critical error: {str(e)}")
        
        # Return empty results with error message
        error_results = [[
            "Error",
            "Critical processing failure",
            str(e),
            "",  # primary_approved_use
            "",  # secondary_approved_use
            "Unknown",
            f"Batch processing failed: {str(e)}",
            "N/A",
            "N/A",
            "N/A"
        ]]
        
        error_csv_buffer = create_csv_for_download(error_results)
        
        # Debug: Ensure we're not returning None in error case
        print(f"🔍 Debug Error: About to return error_results={type(error_results)}, error_csv_buffer={type(error_csv_buffer)}")
        
        return error_results, error_csv_buffer
