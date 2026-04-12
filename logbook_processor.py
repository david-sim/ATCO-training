"""
Logbook Processing Module for Pilot Licensing System
Handles pilot logbook image processing, data extraction, and license eligibility assessment.
"""
import base64
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from io import BytesIO
from PIL import Image
from config_manager import get_azure_endpoint, get_azure_model, get_azure_api_version, get_ai_source
import openai


class LogbookProcessingError(Exception):
    """Custom exception for logbook processing errors"""
    pass


def encode_image_to_base64(image_file) -> str:
    """
    Encode an image file to base64 string.
    
    Args:
        image_file: The uploaded image file object (either raw bytes or file-like object)
        
    Returns:
        Base64 encoded string of the image
        
    Raises:
        LogbookProcessingError: If image encoding fails
    """
    try:
        # Reset file pointer if it's a file-like object
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
            image_bytes = image_file.read()
        else:
            image_bytes = image_file
        
        # Encode to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        return base64_image
        
    except Exception as e:
        raise LogbookProcessingError(f"Failed to encode image: {str(e)}")


def validate_image_file(image_file) -> bool:
    """
    Validate that the uploaded file is a valid image.
    
    Args:
        image_file: The uploaded image file
        
    Returns:
        True if valid image
        
    Raises:
        LogbookProcessingError: If validation fails
    """
    try:
        # Try to open with PIL
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
        
        img = Image.open(image_file)
        img.verify()
        
        # Check image dimensions (should be reasonable for logbook scan)
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
            img = Image.open(image_file)
            width, height = img.size
            
            # Warn if image is too small (likely not a real logbook scan)
            if width < 200 or height < 200:
                raise LogbookProcessingError(f"Image dimensions ({width}x{height}) are too small. Please upload a clearer scan.")
            
        return True
        
    except Exception as e:
        raise LogbookProcessingError(f"Invalid image file: {str(e)}")


def extract_logbook_data_with_vision(image_file, progress_callback=None) -> Dict[str, Any]:
    """
    Extract flight data from logbook image using OpenAI Vision API.
    
    Args:
        image_file: The uploaded logbook image
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Dictionary containing extracted flight data and summary statistics
        
    Raises:
        LogbookProcessingError: If extraction fails
    """
    try:
        if progress_callback:
            progress_callback("🔍 Validating image file...")
        
        # Validate image
        validate_image_file(image_file)
        
        if progress_callback:
            progress_callback("📸 Encoding image for analysis...")
        
        # Encode image to base64
        base64_image = encode_image_to_base64(image_file)
        
        if progress_callback:
            progress_callback("🤖 Analyzing logbook with AI vision...")
        
        # Get LLM configuration
        ai_source = get_ai_source()
        
        if ai_source == "azure":
            # Use Azure OpenAI
            from config_manager import get_azure_api_key
            
            api_key = get_azure_api_key()
            endpoint = get_azure_endpoint()
            model = get_azure_model()
            api_version = get_azure_api_version()
            
            # Configure Azure OpenAI client
            client = openai.AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            
        else:
            # Use regular OpenAI
            from config_manager import get_openai_api_key
            
            api_key = get_openai_api_key()
            client = openai.OpenAI(api_key=api_key)
            model = "gpt-4o"  # Use vision-capable model
        
        # Get extraction rules from config
        from config_manager import get_logbook_extraction_rules
        extraction_rules = get_logbook_extraction_rules()
        
        # Create the vision API request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": extraction_rules
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please analyze this pilot logbook image and extract all flight data according to the instructions. Return the data in JSON format with two main sections: 'flights' (array of individual flight entries) and 'summary' (cumulative statistics)."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4000,
            temperature=0.3
        )
        
        if progress_callback:
            progress_callback("📊 Processing extracted data...")
        
        # Parse the response
        response_text = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Sometimes the response might contain markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            extracted_data = json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw text
            extracted_data = {
                "raw_response": response_text,
                "flights": [],
                "summary": {
                    "extraction_note": "Unable to parse structured data. See raw_response for details."
                }
            }
        
        if progress_callback:
            progress_callback("✅ Logbook data extraction complete!")
        
        return extracted_data
        
    except Exception as e:
        raise LogbookProcessingError(f"Failed to extract logbook data: {str(e)}")


def assess_license_eligibility(summary_data: Dict[str, Any], progress_callback=None) -> Dict[str, Any]:
    """
    Assess pilot's eligibility for various license types based on flight hours.
    
    Args:
        summary_data: Dictionary containing summary flight statistics
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Dictionary containing eligibility assessments for different license types
        
    Raises:
        LogbookProcessingError: If assessment fails
    """
    try:
        if progress_callback:
            progress_callback("🎓 Assessing license eligibility...")
        
        # Get LLM configuration
        ai_source = get_ai_source()
        
        if ai_source == "azure":
            from config_manager import get_azure_api_key
            
            api_key = get_azure_api_key()
            endpoint = get_azure_endpoint()
            model = get_azure_model()
            api_version = get_azure_api_version()
            
            client = openai.AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            
        else:
            from config_manager import get_openai_api_key
            
            api_key = get_openai_api_key()
            client = openai.OpenAI(api_key=api_key)
            model = "gpt-4o"
        
        # Get assessment rules from config
        from config_manager import get_license_assessment_rules
        assessment_rules = get_license_assessment_rules()
        
        # Create assessment prompt
        summary_text = json.dumps(summary_data, indent=2)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": assessment_rules
                },
                {
                    "role": "user",
                    "content": f"Based on the following flight hour summary, please assess the pilot's eligibility for PPL, CPL, IR, and ATPL licenses:\n\n{summary_text}\n\nProvide detailed assessment for each license type."
                }
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        assessment_text = response.choices[0].message.content
        
        if progress_callback:
            progress_callback("✅ License assessment complete!")
        
        return {
            "assessment_text": assessment_text,
            "summary_reviewed": summary_data
        }
        
    except Exception as e:
        raise LogbookProcessingError(f"Failed to assess license eligibility: {str(e)}")


def process_logbook_image(image_file, progress_callback=None) -> Tuple[bool, Dict[str, Any]]:
    """
    Main function to process a logbook image and return extracted data with assessment.
    
    Args:
        image_file: The uploaded logbook image
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Tuple of (success: bool, result_data: dict)
    """
    try:
        # Extract data from image
        extracted_data = extract_logbook_data_with_vision(image_file, progress_callback)
        
        # Assess license eligibility if summary data is available
        assessment = None
        if 'summary' in extracted_data and extracted_data['summary']:
            assessment = assess_license_eligibility(extracted_data['summary'], progress_callback)
        
        # Combine results
        result = {
            "extracted_data": extracted_data,
            "license_assessment": assessment,
            "status": "success"
        }
        
        return True, result
        
    except LogbookProcessingError as e:
        return False, {"error": str(e), "status": "error"}
    except Exception as e:
        return False, {"error": f"Unexpected error: {str(e)}", "status": "error"}


def create_flight_dataframe(extracted_data: Dict[str, Any]) -> Optional[pd.DataFrame]:
    """
    Convert extracted flight data to pandas DataFrame for display/export.
    
    Args:
        extracted_data: Dictionary containing extracted flight data
        
    Returns:
        pandas DataFrame or None if no flight data available
    """
    try:
        if 'flights' in extracted_data and extracted_data['flights']:
            df = pd.DataFrame(extracted_data['flights'])
            return df
        return None
    except Exception as e:
        print(f"Warning: Could not create flight data DataFrame: {str(e)}")
        return None
