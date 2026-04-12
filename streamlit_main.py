"""
Main Streamlit application entry point.
Clean, focused on UI orchestration using modular components.
"""
import streamlit as st
import warnings
import traceback

# Clear Streamlit cache on startup to ensure fresh data loading
st.cache_data.clear()

from ui_components import (
    setup_page_config, 
    display_sidebar, 
    display_logbook_upload_section,
    process_logbook_with_ui,
    display_persistent_logbook_results,
    display_logbook_results
)
from about_page import display_about_page
from methodology_page import display_methodology_page

# Suppress warnings
warnings.filterwarnings("ignore", message="Importing verbose from langchain root module is no longer supported.*")

def display_main_page():
    """Display the main processing page for pilot licensing."""
    # Main content area
    st.title("✈️ Pilot Licensing Assessment Tool")
    
    st.markdown("""
    Welcome to the AI-powered pilot licensing assessment system. Upload your pilot logbook images 
    and the system will extract flight data and assess your eligibility for different pilot licenses.
    """)
    
    # Initialize session state for persistent results
    if 'logbook_results' not in st.session_state:
        st.session_state.logbook_results = None
    if 'last_processed_logbook' not in st.session_state:
        st.session_state.last_processed_logbook = None
    
    # Logbook upload section
    uploaded_image = display_logbook_upload_section()
    
    # Create current input signature for change detection
    current_input = {
        'file_name': uploaded_image.name if uploaded_image else None,
        'file_size': uploaded_image.size if uploaded_image else None
    }
    
    # Check if input has changed (clear results if it has)
    if st.session_state.last_processed_logbook != current_input:
        if st.session_state.last_processed_logbook is not None:  # Don't clear on first load
            st.session_state.logbook_results = None
    
    # Show processing button if image is uploaded
    if uploaded_image is not None:
        if st.button("🚀 Analyze Logbook", type="primary", use_container_width=True,
                    help="Process the uploaded logbook image and assess license eligibility"):
            # Clear progress messages for fresh processing run
            if 'logbook_progress_messages' in st.session_state:
                st.session_state.logbook_progress_messages = []
            # Flag to indicate we're starting processing
            st.session_state.show_persistent_logbook_results = False
            
            # Start processing
            with st.spinner("Analyzing logbook..."):
                success, result_data = process_logbook_with_ui(uploaded_image)
                
                if success:
                    # Store results in session state
                    st.session_state.logbook_results = result_data
                    st.session_state.last_processed_logbook = current_input
                    st.session_state.show_persistent_logbook_results = True
                    st.toast('✅ Analysis completed! Scroll down to view results.')
                else:
                    st.error("Processing failed. Please check your image and try again.")
    
    # Display persistent results if available
    if (st.session_state.logbook_results is not None and 
        st.session_state.get('show_persistent_logbook_results', True)):
        st.markdown("---")
        display_logbook_results(st.session_state.logbook_results)

def main():
    """Main application entry point."""
    try:
        # Setup page configuration
        setup_page_config()
        
        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Main'
        
        # Display sidebar (includes navigation)
        display_sidebar()
        
        # Render the selected page
        current_page = st.session_state.current_page
        
        if current_page == 'About Us':
            display_about_page()
        elif current_page == 'Methodology':
            display_methodology_page()
        else:
            display_main_page()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please refresh the page and try again.")
        
        # Display error details in expander for debugging
        with st.expander("Error Details (for debugging)"):
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
