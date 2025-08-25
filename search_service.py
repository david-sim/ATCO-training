"""
Unified Google search service with timeout handling and retry logic.
Combines functionality from google_search.py and simple_google_search.py.
"""
import time
import logging
import requests
from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# Import handling for different environments
try:
    from serpapi import GoogleSearch
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False
    GoogleSearch = None
    print("⚠️ WARNING: serpapi not installed. Google search functionality will be limited.")

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

# Rate limiting globals
_last_api_call_time = 0
_api_call_count = 0
_rate_limit_reset_time = 0

# Account info caching globals
_cached_account_info = None
_account_info_cache_time = 0
_account_info_cache_duration = 300  # Cache for 5 minutes


def get_rate_limiting_config() -> Dict[str, float]:
    """Get rate limiting configuration from config file or use defaults."""
    defaults = {
        "rate_limit_per_hour": 950,
        "rate_limit_delay": 3.6,
        "min_delay_between_calls": 4.0
    }
    
    try:
        from config_manager import (
            get_rate_limit_per_hour,
            get_rate_limit_delay, 
            get_min_delay_between_calls
        )
        # Read from config.json
        return {
            "rate_limit_per_hour": float(get_rate_limit_per_hour()),
            "rate_limit_delay": float(get_rate_limit_delay()),
            "min_delay_between_calls": float(get_min_delay_between_calls())
        }
    except Exception as e:
        print(f"⚠️ Could not read rate limiting config from config file: {e}")
        return defaults


def apply_rate_limiting():
    """Apply rate limiting to stay within API limits."""
    global _last_api_call_time, _api_call_count, _rate_limit_reset_time
    
    # Get current configuration
    config = get_rate_limiting_config()
    rate_limit_per_hour = config["rate_limit_per_hour"]
    min_delay_between_calls = config["min_delay_between_calls"]
    
    current_time = time.time()
    
    # Reset counter every hour
    if current_time > _rate_limit_reset_time:
        _api_call_count = 0
        _rate_limit_reset_time = current_time + 3600  # Reset in 1 hour
        print(f"🔄 Rate limit counter reset. New reset time: {time.ctime(_rate_limit_reset_time)}")
    
    # Check if we need to delay based on minimum time between calls
    time_since_last_call = current_time - _last_api_call_time
    if time_since_last_call < min_delay_between_calls:
        delay_needed = min_delay_between_calls - time_since_last_call
        print(f"⏳ Rate limiting: waiting {delay_needed:.1f}s before next API call...")
        time.sleep(delay_needed)
    
    # Check if we're approaching hourly limit
    if _api_call_count >= rate_limit_per_hour:
        time_until_reset = _rate_limit_reset_time - time.time()
        if time_until_reset > 0:
            print(f"⚠️ Hourly rate limit reached ({_api_call_count}/{rate_limit_per_hour}). Waiting {time_until_reset:.1f}s...")
            time.sleep(time_until_reset + 1)  # Wait until reset + 1 second buffer
    
    # Update tracking variables
    _last_api_call_time = time.time()
    _api_call_count += 1
    print(f"📊 API Call #{_api_call_count} this hour")


def get_serpapi_key() -> Optional[str]:
    """Get SERPAPI key from secrets, with fallback for testing"""
    if STREAMLIT_AVAILABLE:
        try:
            return st.secrets.get("SERPAPI_API_KEY", None)
        except:
            return None
    
    # Fallback for non-Streamlit environments
    import os
    return os.getenv("SERPAPI_API_KEY")


def perform_search_with_timeout(search_params: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    """Perform Google search with timeout handling."""
    if not SERPAPI_AVAILABLE or GoogleSearch is None:
        return {"error": "SERPAPI not available. Please install: pip install google-search-results"}
    
    def _search():
        try:
            search = GoogleSearch(search_params)
            return search.get_dict()
        except Exception as e:
            return {"error": f"Search API error: {str(e)}"}
    
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_search)
            try:
                return future.result(timeout=timeout)
            except FuturesTimeoutError:
                return {"error": f"Search request timed out after {timeout} seconds"}
    except Exception as e:
        return {"error": f"Search executor error: {str(e)}"}


def google_search_entity(query: str, location: str = "Singapore", max_retries: int = 2, timeout: int = 45) -> Optional[str]:
    """
    Unified Google search with timeout and retry logic.
    
    Args:
        query: Search query string
        location: Location for search context
        max_retries: Maximum number of retry attempts
        timeout: Timeout in seconds for each search attempt
    
    Returns:
        Formatted search results as string or None if failed
    """
    print(f"🔎 Executing Google Search for: {query}")
    
    # Validate API key first
    api_key = get_serpapi_key()
    if not api_key:
        error_msg = "SERPAPI_API_KEY not found in secrets"
        print(f"❌ {error_msg}")
        return None

    for attempt in range(max_retries + 1):
        try:
            print(f"🔎 Attempt {attempt + 1}/{max_retries + 1} - Searching for: {query}")
            
            # Apply rate limiting before making API call
            apply_rate_limiting()
            
            search_params = {
                "q": query,
                "location": location,
                "hl": "en",
                "gl": "sg",
                "filter": "0",
                "api_key": api_key
            }
            
            # Perform search with timeout
            results = perform_search_with_timeout(search_params, timeout=timeout)
            
            if "error" in results:
                error_msg = f"SERP API error: {results['error']}"
                print(f"❌ {error_msg}")
                if attempt < max_retries:
                    print(f"⏳ Retrying in 2 seconds...")
                    time.sleep(2)
                    continue
                else:
                    return None
            
            organic_results = results.get("organic_results", [])
            print(f"✅ Found {len(organic_results)} search results")
            
            if not organic_results:
                return "No search results found for this query"
            
            # Format results using helper function
            return format_search_results(organic_results)
            
        except Exception as e:
            error_msg = f"Search attempt {attempt + 1} failed: {str(e)}"
            print(f"❌ {error_msg}")
            logging.error(error_msg)
            
            if attempt < max_retries:
                print(f"⏳ Retrying in 3 seconds...")
                time.sleep(3)
            else:
                print(f"❌ All search attempts failed for: {query}")
                return None
    
    return None


def format_search_results(organic_results: List[Dict[str, Any]]) -> str:
    """
    Format search results into a consistent string format.
    
    Args:
        organic_results: List of organic search results from SERP API
    
    Returns:
        Formatted search results as string
    """
    if not organic_results:
        return "No search results found"
    
    formatted_results = []
    for item in organic_results:
        title = item.get('title', 'No title')
        link = item.get('link', 'No link')
        snippet = item.get('snippet', 'No snippet')
        date = item.get('date', 'No date available')
        
        formatted_results.append(
            f"Title: {title}\nLink: {link}\nSnippet: {snippet}\nDate: {date}\n"
        )
    
    return "\n".join(formatted_results)


def get_rate_limit_status() -> Dict[str, Any]:
    """Get current rate limiting status for monitoring."""
    global _api_call_count, _rate_limit_reset_time
    
    # Get current configuration
    config = get_rate_limiting_config()
    rate_limit_per_hour = config["rate_limit_per_hour"]
    
    current_time = time.time()
    time_until_reset = max(0, _rate_limit_reset_time - current_time)
    
    return {
        "calls_made_this_hour": _api_call_count,
        "rate_limit": rate_limit_per_hour,
        "calls_remaining": max(0, rate_limit_per_hour - _api_call_count),
        "time_until_reset_minutes": time_until_reset / 60,
        "reset_time": time.ctime(_rate_limit_reset_time) if _rate_limit_reset_time > 0 else "Not set"
    }


def get_serpapi_account_info() -> Optional[Dict[str, Any]]:
    """
    Get SERP API account information including total searches left.
    Uses caching to avoid excessive API calls.
    
    Returns:
        Dictionary containing account information or None if failed
    """
    global _cached_account_info, _account_info_cache_time
    
    # Check if we have valid cached data
    current_time = time.time()
    if (_cached_account_info is not None and 
        current_time - _account_info_cache_time < _account_info_cache_duration):
        print("📋 Using cached SERP account information")
        return _cached_account_info
    
    api_key = get_serpapi_key()
    if not api_key:
        print("❌ SERPAPI_API_KEY not found - cannot retrieve account info")
        return None
    
    try:
        # Make GET request to SERP API account endpoint
        url = f"https://serpapi.com/account?api_key={api_key}"
        
        print("🔍 Retrieving SERP API account information...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            account_data = response.json()
            
            # Cache the result
            _cached_account_info = account_data
            _account_info_cache_time = current_time
            
            print(f"✅ Successfully retrieved SERP account info - cached for {_account_info_cache_duration}s")
            return account_data
        else:
            print(f"❌ SERP API account request failed with status {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ SERP API account request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ SERP API account request failed: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error getting SERP account info: {str(e)}")
        return None


def get_searches_left() -> Optional[int]:
    """
    Get the number of searches remaining in SERP API account.
    
    Returns:
        Number of total searches left or None if failed
    """
    account_info = get_serpapi_account_info()
    if account_info:
        return account_info.get('total_searches_left')
    return None


def get_detailed_account_status() -> Optional[Dict[str, Any]]:
    """
    Get detailed SERP API account status for monitoring dashboard.
    
    Returns:
        Dictionary with formatted account status or None if failed
    """
    account_info = get_serpapi_account_info()
    if not account_info:
        return None
    
    return {
        'plan_name': account_info.get('plan_name', 'Unknown'),
        'searches_per_month': account_info.get('searches_per_month', 0),
        'total_searches_left': account_info.get('total_searches_left', 0),
        'this_month_usage': account_info.get('this_month_usage', 0),
        'last_hour_searches': account_info.get('last_hour_searches', 0),
        'rate_limit_per_hour': account_info.get('account_rate_limit_per_hour', 0),
        'usage_percentage': round((account_info.get('this_month_usage', 0) / account_info.get('searches_per_month', 1)) * 100, 1)
    }


# Legacy compatibility functions
def simple_google_search(address: str, max_retries: int = 2, timeout_seconds: int = 30) -> Optional[str]:
    """Legacy compatibility wrapper for simple_google_search."""
    return google_search_entity(f"{address}", max_retries=max_retries, timeout=timeout_seconds)
