"""
Main Streamlit application entry point for ATC Training Progress Tracker.
Clean, focused on UI orchestration using modular components.
"""
import streamlit as st
import warnings
import traceback

# Clear Streamlit cache on startup to ensure fresh data loading
st.cache_data.clear()

from ui_components import (
    setup_page_config, 
    display_sidebar
)
from dashboard_page import display_dashboard
from training_plan_page import display_training_plan_page
from performance_summary_page import display_performance_summary_page
from validation_assessment_page import display_validation_assessment_page
from about_page import display_about_page
from methodology_page import display_methodology_page

# Suppress warnings
warnings.filterwarnings("ignore", message="Importing verbose from langchain root module is no longer supported.*")


def main():
    """Main application entry point."""
    try:
        # Setup page configuration
        setup_page_config()
        
        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Dashboard'
        
        # Display sidebar (includes navigation)
        display_sidebar()
        
        # Render the selected page
        current_page = st.session_state.current_page
        
        if current_page == 'Dashboard':
            display_dashboard()
        elif current_page == 'Training Plan':
            display_training_plan_page()
        elif current_page == 'Performance Summary':
            display_performance_summary_page()
        elif current_page == 'Validation Assessment':
            display_validation_assessment_page()
        elif current_page == 'About Us':
            display_about_page()
        elif current_page == 'Methodology':
            display_methodology_page()
        else:
            display_dashboard()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please refresh the page and try again.")
        
        # Display error details in expander for debugging
        with st.expander("Error Details (for debugging)"):
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
