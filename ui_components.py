"""
UI utilities and Streamlit-specific components for the Pilot Licensing Assessment Tool.
Contains reusable UI functions and progress handling.
"""
import streamlit as st
import pandas as pd
from typing import Tuple, Optional, Dict, Any
from PIL import Image


def setup_page_config():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title="Pilot Licensing Assessment Tool",
        page_icon="✈️",
        layout="wide"
    )


def display_sidebar():
    """Display the sidebar with application information and navigation."""
    with st.sidebar:
        # Load and display main icon with transparent background
        try:
            main_icon = Image.open("imgs/icon_transparent-color-nobg.png")
            st.image(main_icon, use_container_width=True)
        except:
            st.markdown("# ✈️")
            st.markdown("**Pilot Licensing Tool**")
        
        st.markdown("---")
        
        # Navigation using radio buttons
        st.markdown("### 🧭 Navigation")
        
        # Initialize session state for page navigation
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Main'
        
        page_options = ['Main', 'About Us', 'Methodology']
        current_index = page_options.index(st.session_state.current_page)
        
        selected_page = st.radio(
            "Select Page:",
            options=page_options,
            index=current_index,
            key="page_navigation_radio"
        )
        
        # Update session state if page changed
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()
        
        st.markdown("---")
        
        # Quick stats or info
        st.markdown("### 📊 Quick Info")
        st.info("💡 Upload logbook images to get started")
        st.success("🤖 AI vision for accurate data extraction")
        
        # Display AI configuration
        display_ai_configuration()
        
        st.markdown("---")
        st.markdown("**Pilot Licensing Assessment Tool**")
        st.markdown("Upload pilot logbook images to extract flight data and assess license eligibility.")
        
        # Powered By label
        st.markdown("---")
        st.markdown("**Powered By**")
        try:
            sidebar_image = Image.open("imgs/stsidebarimg.png")
            st.image(sidebar_image, use_container_width=True)
        except:
            st.markdown("OpenAI GPT-4o Vision")


def display_ai_configuration():
    """Display current AI configuration in the sidebar."""
    from config_manager import get_ai_source, get_llm_model, get_azure_model, config
    
    ai_source = get_ai_source()
    
    st.sidebar.markdown("### 🤖 AI Configuration")
    
    # Add reload configuration button
    if st.sidebar.button("🔄 Reload Config", help="Reload configuration from config.json"):
        config.reload()
        st.sidebar.success("✅ Configuration reloaded!")
        st.rerun()
    
    if ai_source == "azure":
        model = get_azure_model()
        st.sidebar.info(f"**Azure OpenAI**\nModel: {model}")
    else:
        model = get_llm_model()
        st.sidebar.info(f"**OpenAI**\nModel: {model}")
    
    st.sidebar.caption(f"Source: {ai_source}")


def display_logbook_upload_section() -> Optional[Any]:
    """
    Display the logbook image upload section for pilot licensing.
    
    Returns:
        The uploaded image file or None
    """
    st.markdown("### Step 1: Upload Pilot Logbook")
    
    st.markdown("""
    📖 Upload a clear image or scan of your pilot logbook pages. The system will extract flight data 
    including flight hours, aircraft types, and other relevant information for license assessment.
    """)
    
    # Image upload
    uploaded_image = st.file_uploader(
        "Choose logbook image",
        type=["png", "jpg", "jpeg", "pdf"],
        help="Upload a clear scan or photo of your pilot logbook page(s)",
        key="logbook_image_uploader"
    )
    
    if uploaded_image is not None:
        st.success(f"✅ Image uploaded: {uploaded_image.name}")
        
        # Display preview (if it's an image)
        if uploaded_image.type.startswith('image'):
            try:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Logbook Preview", use_container_width=True)
                # Reset file pointer after displaying
                uploaded_image.seek(0)
            except Exception as e:
                st.warning(f"Could not display preview: {str(e)}")
        
        # File size warning
        if uploaded_image.size > 10 * 1024 * 1024:  # 10MB
            st.warning("⚠️ Large file detected. Processing may take longer.")
    else:
        st.info("👆 Please upload a logbook image to begin analysis")
    
    return uploaded_image


def process_logbook_with_ui(uploaded_image) -> Tuple[bool, Optional[Dict]]:
    """
    Process logbook image with UI progress updates.
    
    Args:
        uploaded_image: The uploaded logbook image file
        
    Returns:
        Tuple of (success: bool, result_data: dict)
    """
    from logbook_processor import process_logbook_image
    
    # Progress container
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Processing Logbook")
        progress_placeholder = st.empty()
        
        # Initialize progress messages in session state if not exists
        if 'logbook_progress_messages' not in st.session_state:
            st.session_state.logbook_progress_messages = []
        
        def progress_callback(message: str):
            """Callback to update progress messages."""
            st.session_state.logbook_progress_messages.append(message)
            with progress_placeholder.container():
                for msg in st.session_state.logbook_progress_messages:
                    st.info(msg)
        
        try:
            # Process the logbook image
            success, result = process_logbook_image(uploaded_image, progress_callback)
            
            if success:
                st.success("✅ Logbook processing completed successfully!")
                return True, result
            else:
                st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
                return False, result
                
        except Exception as e:
            st.error(f"❌ Unexpected error during processing: {str(e)}")
            return False, {"error": str(e)}


def display_logbook_results(result_data: Dict[str, Any]):
    """
    Display the extracted logbook data and license assessment.
    
    Args:
        result_data: Dictionary containing extraction results and assessment
    """
    st.markdown("### 📊 Logbook Analysis Results")
    
    # Display extracted data
    if "extracted_data" in result_data:
        extracted = result_data["extracted_data"]
        
        # Display summary statistics
        if "summary" in extracted and extracted["summary"]:
            st.markdown("#### Flight Hours Summary")
            summary = extracted["summary"]
            
            # Create columns for summary display
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Flight Hours", summary.get("total_flight_hours", "N/A"))
                st.metric("PIC Hours", summary.get("total_pic_hours", "N/A"))
            
            with col2:
                st.metric("Dual Instruction", summary.get("total_dual_hours", "N/A"))
                st.metric("Cross Country", summary.get("total_cross_country_hours", "N/A"))
            
            with col3:
                st.metric("Night Hours", summary.get("total_night_hours", "N/A"))
                st.metric("Instrument Hours", summary.get("total_instrument_hours", "N/A"))
            
            with col4:
                st.metric("Aircraft Types", summary.get("unique_aircraft_count", "N/A"))
                st.metric("Date Range", summary.get("date_range", "N/A"))
        
        # Display individual flight entries if available
        if "flights" in extracted and extracted["flights"]:
            st.markdown("#### Individual Flight Entries")
            from logbook_processor import create_flight_dataframe
            
            df = create_flight_dataframe(extracted)
            if df is not None:
                st.dataframe(df, use_container_width=True)
                
                # Add CSV export button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Flight Data (CSV)",
                    data=csv,
                    file_name="flight_data.csv",
                    mime="text/csv"
                )
    
    # Display license assessment
    if "license_assessment" in result_data and result_data["license_assessment"]:
        st.markdown("#### 🎓 License Eligibility Assessment")
        assessment = result_data["license_assessment"]
        
        if "assessment_text" in assessment:
            st.markdown(assessment["assessment_text"])
    
    # Display raw response if available (for debugging)
    if "extracted_data" in result_data and "raw_response" in result_data["extracted_data"]:
        with st.expander("🔍 View Raw AI Response"):
            st.text(result_data["extracted_data"]["raw_response"])


def display_persistent_logbook_results():
    """Display persistent logbook results from session state."""
    if 'logbook_results' in st.session_state and st.session_state.logbook_results is not None:
        if st.session_state.get('show_persistent_logbook_results', False):
            st.markdown("---")
            display_logbook_results(st.session_state.logbook_results)
