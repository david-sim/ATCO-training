"""
Dialogue Session page for ATC Training Progress Tracker.
Records dialogue sessions between training managers and trainees (every 100 hours).
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def display_dialogue_page():
    """Display the dialogue session logging page."""
    
    st.title("💬 Dialogue Sessions")
    
    st.markdown("""
    A dialogue session is conducted by the training manager every **100 hours** of training 
    to evaluate the trainee's progress, discuss challenges, and plan next steps. These sessions 
    form the basis for creating performance summaries.
    """)
    
    st.markdown("---")
    
    # Trainee Selection and Dialogue Overview
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        trainee_name = st.selectbox(
            "Select Trainee",
            ["John Smith", "Sarah Johnson", "Michael Chen", "Emily Davis"],
            help="Select the trainee for dialogue session"
        )
    
    with col2:
        st.metric(
            "Total Training Hours",
            "147.5 hrs",
            "+8.5 hrs this week"
        )
    
    with col3:
        st.metric(
            "Completed Dialogues",
            "1",
            "Next at 200 hrs"
        )
    
    st.markdown("---")
    
    # Dialogue Session Tabs
    tab1, tab2, tab3 = st.tabs(["📝 New Dialogue Session", "📊 Dialogue History", "🎯 Dialogue Milestones"])
    
    with tab1:
        st.markdown("## 📝 Conduct New Dialogue Session")
        
        st.info("""
        **Dialogue Session Purpose:**  
        A structured conversation to review the trainee's performance over the last 100 hours, 
        identify strengths and areas for improvement, and align on training goals moving forward.
        """)
        
        with st.form("dialogue_session_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                dialogue_number = st.number_input(
                    "Dialogue Session Number",
                    min_value=1,
                    value=2,
                    help="Sequential dialogue number (e.g., Dialogue #2)"
                )
                
                session_date = st.date_input(
                    "Session Date",
                    value=datetime.now()
                )
                
                training_hours_reviewed = st.text_input(
                    "Training Hours Reviewed",
                    value="100-147.5 hrs",
                    help="Range of training hours covered in this dialogue"
                )
                
                training_manager = st.text_input(
                    "Training Manager",
                    value="Robert Williams"
                )
            
            with col2:
                session_duration = st.slider(
                    "Session Duration (minutes)",
                    min_value=15,
                    max_value=180,
                    value=60,
                    step=15
                )
                
                overall_performance = st.select_slider(
                    "Overall Performance Rating",
                    options=["Needs Improvement", "Below Standard", "Satisfactory", "Good", "Excellent"],
                    value="Good"
                )
                
                training_phase = st.selectbox(
                    "Current Training Phase",
                    ["Phase 1 - Foundation", "Phase 2 - Development", "Phase 3 - Consolidation", 
                     "Phase 4 - Pre-Certification"]
                )
            
            st.markdown("---")
            
            # Competency Discussion
            st.markdown("### 🎯 Competency-Based Discussion")
            
            st.markdown("""
            Review each competency area and document the trainee's progress, strengths, 
            and areas requiring further development.
            """)
            
            competencies = [
                "Communication",
                "Situational Awareness", 
                "Decision Making",
                "Workload Management",
                "Teamwork",
                "Technical Knowledge",
                "Procedures",
                "Problem Solving"
            ]
            
            # Create two columns for competency ratings
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Rate Current Competency Levels:**")
                for comp in competencies[:4]:
                    st.slider(
                        comp,
                        min_value=0,
                        max_value=100,
                        value=75,
                        step=5,
                        key=f"comp_{comp.lower().replace(' ', '_')}"
                    )
            
            with col2:
                st.markdown("** **")  # Spacing
                for comp in competencies[4:]:
                    st.slider(
                        comp,
                        min_value=0,
                        max_value=100,
                        value=75,
                        step=5,
                        key=f"comp_{comp.lower().replace(' ', '_')}"
                    )
            
            st.markdown("---")
            
            # Key Discussion Points
            st.markdown("### 💡 Key Discussion Points")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Strengths Identified:**")
                strengths = st.text_area(
                    "Record observed strengths",
                    placeholder="E.g., Excellent communication skills, strong situational awareness during peak hours, effective teamwork with colleagues...",
                    height=150,
                    key="strengths_area"
                )
            
            with col2:
                st.markdown("**Areas for Improvement:**")
                improvements = st.text_area(
                    "Record areas needing development",
                    placeholder="E.g., Decision making in complex scenarios, workload management during emergencies, procedural adherence under pressure...",
                    height=150,
                    key="improvements_area"
                )
            
            st.markdown("---")
            
            # Training Progress & Challenges
            st.markdown("### 📊 Training Progress & Challenges")
            
            progress_discussion = st.text_area(
                "Progress Since Last Dialogue",
                placeholder="Discuss improvements, milestones achieved, notable incidents or achievements...",
                height=120
            )
            
            challenges_faced = st.text_area(
                "Challenges Faced",
                placeholder="Document any difficulties, setbacks, or obstacles encountered during training...",
                height=120
            )
            
            st.markdown("---")
            
            # Action Plan & Goals
            st.markdown("### 🎯 Action Plan & Goals for Next 100 Hours")
            
            col1, col2 = st.columns(2)
            
            with col1:
                focus_areas = st.multiselect(
                    "Priority Focus Areas",
                    competencies,
                    default=["Decision Making", "Workload Management"]
                )
                
                training_activities = st.text_area(
                    "Recommended Training Activities",
                    placeholder="E.g., 5 simulation sessions focusing on emergency procedures, 3 peak-hour training sessions, 2 coordination exercises...",
                    height=120
                )
            
            with col2:
                specific_goals = st.text_area(
                    "Specific Goals to Achieve",
                    placeholder="E.g., Improve decision making score to 85%, complete 10 emergency scenario simulations, reduce response time by 20%...",
                    height=120
                )
                
                next_dialogue_target = st.number_input(
                    "Next Dialogue at (hours)",
                    min_value=100,
                    value=200,
                    step=100
                )
            
            st.markdown("---")
            
            # Trainee Feedback & Comments
            st.markdown("### 💭 Trainee Feedback & Self-Assessment")
            
            trainee_feedback = st.text_area(
                "Trainee's Comments & Self-Reflection",
                placeholder="Record the trainee's self-assessment, concerns, questions, or feedback they provided during the dialogue...",
                height=120
            )
            
            trainee_goals = st.text_area(
                "Trainee's Personal Goals",
                placeholder="What the trainee wants to achieve in the next training period...",
                height=100
            )
            
            st.markdown("---")
            
            # Additional Notes
            additional_notes = st.text_area(
                "Additional Notes & Observations",
                placeholder="Any other relevant information, context, or observations from the dialogue session...",
                height=100
            )
            
            # Form Submission
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                submitted = st.form_submit_button("💾 Save Dialogue Session", type="primary", use_container_width=True)
            
            with col2:
                if st.form_submit_button("📊 Generate Performance Summary", use_container_width=True):
                    st.info("This will create a performance summary based on this dialogue session")
            
            if submitted:
                st.success("✅ Dialogue session saved successfully!")
                st.info("💡 You can now generate a performance summary based on this dialogue session.")
                st.balloons()
    
    with tab2:
        st.markdown("## 📊 Dialogue Session History")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            filter_manager = st.selectbox(
                "Training Manager",
                ["All Managers", "Robert Williams", "Sarah Lee", "Michael Brown"]
            )
        
        with col2:
            filter_period = st.selectbox(
                "Time Period",
                ["All Time", "Last 3 Months", "Last 6 Months", "This Year"]
            )
        
        st.markdown("---")
        
        # Sample dialogue history
        dialogue_history = {
            'Dialogue #': ['Dialogue #1', 'Initial Assessment'],
            'Date': ['Mar 15, 2026', 'Jan 15, 2026'],
            'Training Hours': ['100-105.5 hrs', '0 hrs'],
            'Training Manager': ['Robert Williams', 'Sarah Lee'],
            'Phase': ['Phase 2', 'Phase 1'],
            'Overall Rating': ['Good', 'Satisfactory'],
            'Focus Areas': ['Decision Making, Workload Management', 'Foundation Skills'],
            'Performance Summary': ['Created', 'Created']
        }
        
        df_dialogue = pd.DataFrame(dialogue_history)
        
        st.dataframe(df_dialogue, use_container_width=True, hide_index=True)
        
        # View details button
        st.markdown("---")
        st.markdown("### 📋 View Dialogue Details")
        
        selected_dialogue = st.selectbox(
            "Select dialogue to view full details",
            ["Dialogue #1 - Mar 15, 2026", "Initial Assessment - Jan 15, 2026"]
        )
        
        if st.button("📖 View Full Dialogue Record", type="primary"):
            with st.expander("Dialogue Session Details", expanded=True):
                st.markdown("""
                **Dialogue #1 - March 15, 2026**
                
                **Training Hours Reviewed:** 100-105.5 hrs  
                **Training Manager:** Robert Williams  
                **Duration:** 60 minutes  
                **Overall Performance:** Good
                
                ---
                
                **Competency Ratings:**
                - Communication: 80%
                - Situational Awareness: 75%
                - Decision Making: 65%
                - Workload Management: 68%
                - Teamwork: 82%
                - Technical Knowledge: 78%
                - Procedures: 73%
                - Problem Solving: 65%
                
                ---
                
                **Strengths:**
                - Excellent communication with pilots and team members
                - Strong teamwork and collaboration skills
                - Good technical knowledge foundation
                
                **Areas for Improvement:**
                - Decision making in complex scenarios
                - Workload management during peak hours
                - Problem-solving under pressure
                
                ---
                
                **Action Plan:**
                - Focus on decision-making simulations
                - Additional peak-hour training sessions
                - Emergency scenario practice
                - Target: Reach 85% in all competencies by Dialogue #2
                """)
    
    with tab3:
        st.markdown("## 🎯 Dialogue Milestones & Schedule")
        
        st.markdown("""
        Dialogue sessions are scheduled every **100 hours** of training to ensure regular 
        evaluation and feedback for the trainee.
        """)
        
        # Milestone tracker
        milestones = {
            'Milestone': ['Initial Assessment', 'Dialogue #1', 'Dialogue #2', 'Dialogue #3', 'Dialogue #4', 'Final Assessment'],
            'Target Hours': ['0 hrs', '100 hrs', '200 hrs', '300 hrs', '400 hrs', '500 hrs'],
            'Actual Hours': ['0 hrs', '105.5 hrs', '-', '-', '-', '-'],
            'Status': ['✅ Completed', '✅ Completed', '🔄 Upcoming (at 147.5 hrs)', '⏳ Pending', '⏳ Pending', '⏳ Pending'],
            'Date': ['Jan 15, 2026', 'Mar 15, 2026', 'Scheduled: May 5, 2026', '-', '-', '-'],
            'Performance Summary': ['Created ✓', 'Created ✓', 'Not Created', '-', '-', '-']
        }
        
        df_milestones = pd.DataFrame(milestones)
        st.dataframe(df_milestones, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Progress visualization
        st.markdown("### 📈 Training Progress Visualization")
        
        current_hours = 147.5
        next_milestone = 200
        
        progress = (current_hours / next_milestone) * 100
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.progress(progress / 100)
            st.caption(f"Progress to Dialogue #2: {current_hours} / {next_milestone} hours ({progress:.1f}%)")
        
        with col2:
            hours_remaining = next_milestone - current_hours
            st.metric("Hours Remaining", f"{hours_remaining} hrs")
        
        st.info(f"💡 At the current training pace, Dialogue #2 is estimated for **May 5, 2026**")
    
    st.markdown("---")
    
    # Declaration Checkbox
    st.markdown("## ✍️ Dialogue Session Declaration")
    
    st.markdown("""
    The following declaration confirms that the dialogue session has been conducted 
    in accordance with ATC training standards.
    """)
    
    st.markdown("### 👨‍💼 Training Manager Declaration")
    manager_declares = st.checkbox(
        "I certify that this dialogue session was conducted in a fair and thorough manner, accurately reflects the discussions held, and the action plan has been mutually agreed upon with the trainee.",
        key="manager_declaration_dialogue"
    )
    
    if manager_declares:
        col1, col2 = st.columns(2)
        
        with col1:
            manager_signature = st.text_input("Training Manager Name", value="Robert Williams", disabled=True)
        
        with col2:
            manager_date = st.date_input("Date", value=datetime.now(), key="manager_date_dialogue")
        
        st.success("✅ Dialogue session has been certified and signed off by the training manager.")
    else:
        st.info("ℹ️ Please confirm the declaration to complete the dialogue session certification.")


if __name__ == "__main__":
    display_dialogue_page()
