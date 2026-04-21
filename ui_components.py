"""
UI utilities and Streamlit-specific components for the ATC Training Progress Tracker.
Contains reusable UI functions and configuration.
"""
import streamlit as st
from typing import Optional, Dict, Any
from PIL import Image


def setup_page_config():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title="ATC Training Progress Tracker",
        page_icon="🎯",
        layout="wide"
    )


def display_sidebar():
    """Display the sidebar with application information and navigation."""
    with st.sidebar:
        # Load and display main icon with transparent background
        try:
            main_icon = Image.open("imgs/ATCO logo.png")
            st.image(main_icon, use_container_width=True)
        except:
            st.markdown("# 🎯")
            st.markdown("**ATC Training Tracker**")
        
        st.markdown("---")
        
        # Navigation using radio buttons
        st.markdown("### 🧭 Navigation")
        
        # Initialize session state for page navigation
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Dashboard'
        
        page_options = [
            'Dashboard',
            'Training Plan',
            'Training Sessions',
            'Dialogue Sessions',
            'Performance Summary',
            'Validation Assessment',
            'About Us',
            'Methodology'
        ]
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
        st.info("🎯 Track trainee progress and competencies")
        st.success("🤖 AI-powered insights and recommendations")
        
        # Display AI configuration
        display_ai_configuration()
        
        st.markdown("---")
        st.markdown("**ATC Training Progress Tracker**")
        st.markdown("Comprehensive training management system for Air Traffic Controller trainees.")
        
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

