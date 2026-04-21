"""
Training Plan Discussion page for ATC Training Progress Tracker.
Enables training managers to discuss and plan training activities with trainees.
"""
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd


def display_training_plan_page():
    """Display the training plan discussion page."""
    
    st.title("📋 Training Plan Discussion")
    
    st.markdown("""
    This page facilitates discussions between training managers and ATC trainees to develop 
    comprehensive training plans tailored to individual needs and competency development goals.
    """)
    
    st.markdown("---")
    
    # Trainee Selection
    st.markdown("## 👤 Select Trainee")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        trainee_name = st.selectbox(
            "Trainee",
            ["John Smith", "Sarah Johnson", "Michael Chen", "Emily Davis"],
            help="Select the trainee for training plan discussion"
        )
    
    with col2:
        st.info(f"**Current Training Phase: Training Phase #2\n\n**Training Manager:** Robert Williams")
    
    st.markdown("---")
    
    # Training Plan Overview
    st.markdown("## 📊 On-the-Job Training Overview")
    
    # Sample training plan data
    training_plan_data = {
        'Phase': ['Phase 1', '100-hour dialogue', 'Performance Summary', 'Validation Assessment'],
        'Duration (weeks)': [4, 6, 6, 1],
        'Status': ['Completed', 'In Progress', 'Not Started', 'Not Started'],
        'Completion (%)': [100, 65, 0, 0],
        'Key Focus Areas': [
            'Basic ATC procedures, Communication',
            'Traffic management, Decision making',
            'Complex scenarios, Emergency handling',
            'Final validation and certification'
        ]
    }
    
    df_plan = pd.DataFrame(training_plan_data)
    
    # Style the dataframe
    def color_status(val):
        if val == 'Completed':
            return 'background-color: #90EE90'
        elif val == 'In Progress':
            return 'background-color: #FFFFE0'
        else:
            return 'background-color: #FFE4E1'
    
    styled_df = df_plan.style.applymap(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    # Meeting Notes
    st.markdown("## 📝 Training Objectives")
    
    meeting_notes = st.text_area(
        "Discussion Summary",
        placeholder="Enter key points discussed during the training plan meeting...",
        height=200
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Notes", use_container_width=True):
            st.success("Notes saved successfully!")
    
    with col2:
        if st.button("📧 Email Summary", use_container_width=True):
            st.info("Email summary feature coming soon!")
    
    with col3:
        if st.button("📄 Generate Report", use_container_width=True):
            st.info("Report generation feature coming soon!")
    
    st.markdown("---")
    
    # Discussion Topics
    st.markdown("## 💬 Discussion Topics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Strengths to Leverage")
        st.success("""
        - Strong communication skills
        - Good teamwork and collaboration
        - Solid understanding of procedures
        - Quick learning ability
        """)
    
    with col2:
        st.markdown("### Areas Requiring Focus")
        st.warning("""
        - Problem-solving under pressure
        - Workload management in peak hours
        - Decision-making speed
        - Emergency procedure execution
        """)
    
    st.markdown("---")
    
    # Training Plan Adjustments
    st.markdown("## 🔧 Proposed Training Plan Adjustments")
    
    with st.expander("📝 Add New Training Activity", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            activity_type = st.selectbox(
                "Activity Type",
                ["Simulation", "Theory Session", "Tabletop Exercise", "Quiz Assessment"]
            )
        
        with col2:
            scheduled_date = st.date_input("Scheduled Date")
        
        with col3:
            duration = st.number_input("Duration (hours)", min_value=0.5, max_value=8.0, value=2.0, step=0.5)
        
        focus_area = st.multiselect(
            "Focus Areas",
            ["Communication", "Situational Awareness", "Decision Making", "Workload Management", 
             "Teamwork", "Technical Knowledge", "Procedures", "Problem Solving"]
        )
        
        notes = st.text_area("Additional Notes", placeholder="Enter any specific objectives or notes for this activity...")
        
        if st.button("Add Activity to Plan", type="primary"):
            st.success("✅ Training activity added to plan successfully!")
    
    st.markdown("---")
    
    # AI-Powered Training Recommendations
    st.markdown("## 🤖 AI-Powered Training Recommendations")
    
    st.info("""
    **Note:** This feature uses generative AI to analyze trainee performance data and suggest 
    personalized training recommendations. The AI analyzes competency scores, learning patterns, 
    and training history to provide tailored suggestions.
    """)
    
    if st.button("🚀 Generate AI Recommendations", type="primary"):
        with st.spinner("Analyzing trainee performance and generating recommendations..."):
            # Placeholder for AI generation
            st.markdown("### 📋 Recommended Training Focus")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Priority 1: Enhance Problem Solving Skills**
                - Current Score: 65%
                - Target: 85%
                - Recommended Activities:
                  - 3x Complex scenario simulations
                  - 2x Problem-solving workshops
                  - 1x Mentoring session with senior controller
                - Estimated Time: 12 hours over 2 weeks
                """)
                
                st.markdown("""
                **Priority 2: Improve Workload Management**
                - Current Score: 68%
                - Target: 85%
                - Recommended Activities:
                  - 4x Peak-hour simulations
                  - 2x Multi-tasking exercises
                  - 1x Stress management training
                - Estimated Time: 10 hours over 2 weeks
                """)
            
            with col2:
                st.markdown("""
                **Priority 3: Strengthen Decision Making**
                - Current Score: 70%
                - Target: 85%
                - Recommended Activities:
                  - 3x Time-critical scenario practice
                  - 2x Decision tree analysis sessions
                  - 1x Case study review
                - Estimated Time: 8 hours over 1 week
                """)
                
                st.markdown("""
                **Additional Recommendations:**
                - Continue leveraging strong communication skills in team exercises
                - Maintain procedural knowledge through regular reviews
                - Schedule weekly progress check-ins with training manager
                """)
            
            st.success("✅ AI recommendations generated successfully!")
            
            # Placeholder note about future AI integration
            st.info("🔮 **Future Enhancement:** This will integrate with actual AI models to provide dynamic, real-time recommendations based on comprehensive trainee data analysis.")
    
    st.markdown("---")
    
    
    # Training History
    st.markdown("## 📚 Previous Training Plan Discussions")
    
    history_data = {
        'Date': ['Apr 1, 2026', 'Mar 15, 2026', 'Mar 1, 2026', 'Feb 15, 2026'],
        'Training Manager': ['Robert Williams', 'Robert Williams', 'Sarah Lee', 'Sarah Lee'],
        'Main Topics': [
            'Mid-phase review, Competency assessment',
            'Workload management strategies',
            'Communication techniques',
            'Initial training plan setup'
        ],
        'Action Items': ['5 items', '3 items', '4 items', '6 items']
    }
    
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Declaration Checkboxes
    st.markdown("## ✍️ Training Plan Signoff")
    
    st.markdown("""
    The following declarations confirm that the training plan has been reviewed and agreed upon 
    by both the trainee and the training manager.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Trainee Declaration")
        trainee_declares = st.checkbox(
            "I acknowledge that I have reviewed and understood the training plan, and I commit to actively participating in all scheduled activities.",
            key="trainee_declaration"
        )
        
        if trainee_declares:
            trainee_signature = st.text_input("Trainee Name", value=trainee_name, disabled=True)
            trainee_date = st.date_input("Date", value=datetime.now(), key="trainee_date")
    
    with col2:
        st.markdown("### 👨‍💼 Training Manager Declaration")
        manager_declares = st.checkbox(
            "I confirm that this training plan is appropriate for the trainee's current competency level and training objectives.",
            key="manager_declaration_tp"
        )
        
        if manager_declares:
            manager_signature = st.text_input("Training Manager Name", value="Robert Williams", disabled=True)
            manager_date = st.date_input("Date", value=datetime.now(), key="manager_date_tp")
    
    if trainee_declares and manager_declares:
        st.success("✅ Training plan has been signed off by both trainee and training manager.")
    elif trainee_declares or manager_declares:
        st.warning("⚠️ Pending signature from both parties.")
    else:
        st.info("ℹ️ Please confirm the declarations to complete the training plan signoff.")
