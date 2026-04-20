"""
About Us page for the ATC Training Progress Tracker.
Contains project information, scope, objectives, and methodology.
"""
import streamlit as st


def display_about_page():
    """Display the About Us page content."""
    
    # Page header
    st.markdown("# 🔍 About Us")
    st.markdown("---")
    
    # Project Overview Section
    st.markdown("## 📋 Project Overview")
    
    st.markdown("""
    **ATC Training Progress Tracker** is an AI-assisted platform developed to revolutionize 
    the way Air Traffic Controller trainees are monitored, evaluated, and developed throughout 
    their training journey.
    
    This innovative solution combines advanced artificial intelligence with comprehensive 
    performance tracking capabilities to streamline training management and ensure optimal 
    trainee development outcomes.
    """)
    
    # Project Scope Section
    st.markdown("## 🎯 Project Scope")
    
    st.markdown("""
    The scope of this project encompasses the development of an intelligent system that:
    
    • **Tracks Training Progress**: Real-time monitoring of trainee competency development
    
    • **Manages Training Plans**: Collaborative planning between trainees and training managers
    
    • **Evaluates Performance**: Comprehensive assessment and validation of skills
    
    • **Provides AI Insights**: Intelligent recommendations for personalized training paths
    
    • **Generates Reports**: Automated reporting and certification documentation
    """)
    
    # Objective Section
    st.markdown("## 🎖️ Objective")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        ### Primary Goals:
        1. **Competency Tracking**
        2. **Training Optimization**
        3. **Performance Validation**
        """)
    
    with col2:
        st.markdown("""
        The primary objective is to create a comprehensive training management system that:
        
        **Phase 1: Progress Monitoring**  
        Track trainee progress across all competency areas with real-time dashboards 
        and detailed analytics showing development patterns and areas requiring focus.
        
        **Phase 2: Training Enhancement**  
        Facilitate training plan discussions and provide AI-powered recommendations 
        to optimize learning paths based on individual trainee needs and performance.
        
        **Phase 3: Validation & Certification**  
        Manage formal assessments and validation processes to ensure trainees meet 
        all required standards before certification.
        """)
    
    # AI Implementation Section
    st.markdown("## 🤖 AI Model Implementation")
    
    st.markdown("""
    The AI system is strategically implemented across **three critical areas** 
    to ensure comprehensive training support:
    """)
    
    # Create three columns for the AI areas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Area 1: Performance Analysis
        
        **Purpose**: Analyze trainee performance data
        
        **Process**:
        - Review competency scores and trends
        - Identify strengths and weaknesses
        - Compare against cohort benchmarks
        - Detect performance patterns
        
        **Output**: Detailed performance insights and trend analysis
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Area 2: Training Recommendations
        
        **Purpose**: Generate personalized training suggestions
        
        **Process**:
        - Analyze learning patterns
        - Identify competency gaps
        - Recommend targeted training activities
        - Optimize training schedules
        
        **Output**: AI-powered training plan recommendations
        """)
    
    with col3:
        st.markdown("""
        ### ✅ Area 3: Assessment Evaluation
        
        **Purpose**: Support validation and certification
        
        **Process**:
        - Evaluate assessment results
        - Generate performance summaries
        - Predict certification readiness
        - Provide improvement insights
        
        **Output**: Comprehensive assessment reports and certification readiness scores
        """)
    
    # Key Features Section
    st.markdown("## 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Dashboard & Monitoring
        - Real-time competency tracking
        - Visual performance charts
        - Progress timeline view
        - Comparative analytics
        
        ### Training Management
        - Collaborative training planning
        - Session scheduling and tracking
        - Focus area identification
        - Training history logs
        """)
    
    with col2:
        st.markdown("""
        ### Assessment & Validation
        - Comprehensive evaluation forms
        - Automated scoring and tracking
        - Certification management
        - Assessment history
        
        ### AI-Powered Insights
        - Performance predictions
        - Personalized recommendations
        - Automated report generation
        - Intelligent analytics
        """)
    
    # Technology Stack
    st.markdown("## 💻 Technology Stack")
    
    st.markdown("""
    - **Framework**: Streamlit (Python-based web application)
    - **Data Visualization**: Plotly for interactive charts and graphs
    - **AI Integration**: OpenAI GPT-4o for intelligent insights
    - **Data Processing**: Pandas for analytics and reporting
    - **UI/UX**: Modern, responsive design with intuitive navigation
    """)
    
    st.markdown("---")
    
    # Contact or Additional Info
    st.markdown("## 📞 Contact Information")
    
    st.info("""
    For questions, support, or feedback about the ATC Training Progress Tracker, 
    please contact your training administrator or system support team.
    """)


if __name__ == "__main__":
    display_about_page()
