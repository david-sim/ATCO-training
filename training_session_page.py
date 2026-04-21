"""
Training Session page for ATC Training Progress Tracker.
Tracks training hours and session details for trainees.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go


def display_training_session_page():
    """Display the training session tracking page."""
    
    st.title("📚 Training Sessions")
    
    st.markdown("""
    Track and manage on-the-job training sessions for ATC trainees. This page monitors 
    training hours, session types, and progress toward the 100-hour dialogue milestones.
    """)
    
    st.markdown("---")
    
    # Trainee Selection and Overview
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        trainee_name = st.selectbox(
            "Select Trainee",
            ["John Smith", "Sarah Johnson", "Michael Chen", "Emily Davis"],
            help="Select the trainee to view/log training sessions"
        )
    
    with col2:
        st.metric(
            "Total Training Hours",
            "147.5 hrs",
            "+8.5 hrs this week"
        )
    
    with col3:
        st.metric(
            "Next Dialogue at",
            "200 hrs",
            "52.5 hrs remaining"
        )
    
    st.markdown("---")
    
    # Training Hours Progress
    st.markdown("## 📊 Training Hours Progress")
    
    # Progress toward next dialogue
    total_hours = 147.5
    next_dialogue_target = 200
    progress_percentage = (total_hours / next_dialogue_target) * 100
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.progress(progress_percentage / 100)
        st.caption(f"Progress: {total_hours} / {next_dialogue_target} hours ({progress_percentage:.1f}%)")
    
    with col2:
        st.markdown(f"**Dialogue #{int(total_hours // 100) + 1}**")
        st.caption(f"at {next_dialogue_target} hours")
    
    # Dialogue milestones
    st.markdown("### 🎯 Dialogue Milestones")
    
    milestones_data = {
        'Dialogue #': ['Dialogue #1', 'Dialogue #2', 'Dialogue #3', 'Dialogue #4'],
        'Target Hours': ['100 hrs', '200 hrs', '300 hrs', '400 hrs'],
        'Status': ['✅ Completed (105.5 hrs)', '🔄 In Progress (147.5 hrs)', '⏳ Pending', '⏳ Pending'],
        'Date Conducted': ['Mar 15, 2026', 'Scheduled: May 5, 2026', '-', '-']
    }
    
    df_milestones = pd.DataFrame(milestones_data)
    st.dataframe(df_milestones, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Log New Training Session
    st.markdown("## ➕ Log New Training Session")
    
    with st.form("log_training_session"):
        col1, col2 = st.columns(2)
        
        with col1:
            session_date = st.date_input(
                "Session Date",
                value=datetime.now(),
                help="Date when the training session was conducted"
            )
            
            session_type = st.selectbox(
                "Session Type",
                [
                    "Live Traffic Training",
                    "Simulation Exercise",
                    "Emergency Procedures",
                    "Peak Hour Training",
                    "Night Operations",
                    "Weather Operations",
                    "Coordination Training",
                    "Equipment Familiarization"
                ]
            )
            
            training_manager = st.text_input(
                "Training Manager",
                value="Robert Williams",
                help="Name of the supervising training manager"
            )
        
        with col2:
            start_time = st.time_input("Start Time", value=None)
            end_time = st.time_input("End Time", value=None)
            
            # Calculate duration
            if start_time and end_time:
                duration = (datetime.combine(datetime.today(), end_time) - 
                           datetime.combine(datetime.today(), start_time))
                duration_hours = duration.total_seconds() / 3600
                st.info(f"⏱️ Duration: {duration_hours:.2f} hours")
            
            competencies_practiced = st.multiselect(
                "Competencies Practiced",
                [
                    "Communication",
                    "Situational Awareness",
                    "Decision Making",
                    "Workload Management",
                    "Teamwork",
                    "Technical Knowledge",
                    "Procedures",
                    "Problem Solving"
                ],
                default=["Communication", "Situational Awareness"]
            )
        
        session_notes = st.text_area(
            "Session Notes",
            placeholder="Enter observations, challenges faced, achievements, areas for improvement...",
            height=120
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            submitted = st.form_submit_button("💾 Log Training Session", type="primary", use_container_width=True)
        
        with col2:
            if st.form_submit_button("🔄 Clear Form", use_container_width=True):
                st.rerun()
        
        if submitted:
            st.success("✅ Training session logged successfully!")
            st.balloons()
    
    st.markdown("---")
    
    # Training Session History
    st.markdown("## 📋 Training Session History")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_period = st.selectbox(
            "Time Period",
            ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"]
        )
    
    with col2:
        filter_type = st.selectbox(
            "Session Type",
            ["All Types", "Live Traffic Training", "Simulation Exercise", "Emergency Procedures"]
        )
    
    with col3:
        filter_manager = st.selectbox(
            "Training Manager",
            ["All Managers", "Robert Williams", "Sarah Lee", "Michael Brown"]
        )
    
    # Sample session history data
    session_history = {
        'Date': ['Apr 19, 2026', 'Apr 18, 2026', 'Apr 17, 2026', 'Apr 16, 2026', 'Apr 15, 2026', 
                 'Apr 12, 2026', 'Apr 11, 2026', 'Apr 10, 2026'],
        'Session Type': ['Live Traffic Training', 'Simulation Exercise', 'Peak Hour Training', 
                        'Live Traffic Training', 'Weather Operations', 'Emergency Procedures',
                        'Live Traffic Training', 'Coordination Training'],
        'Duration (hrs)': [4.0, 3.5, 4.5, 4.0, 3.0, 2.5, 4.0, 3.5],
        'Training Manager': ['Robert Williams', 'Robert Williams', 'Sarah Lee', 'Robert Williams',
                            'Michael Brown', 'Sarah Lee', 'Robert Williams', 'Sarah Lee'],
        'Competencies': ['Communication, Situational Awareness', 'Problem Solving, Decision Making',
                        'Workload Management, Teamwork', 'Communication, Technical Knowledge',
                        'Procedures, Decision Making', 'Problem Solving, Procedures',
                        'Communication, Teamwork', 'Teamwork, Communication'],
        'Notes': ['Excellent performance', 'Needs improvement on complex scenarios', 'Strong under pressure',
                 'Good progress', 'Handled weather well', 'Quick response to emergencies',
                 'Great team coordination', 'Effective communication']
    }
    
    df_history = pd.DataFrame(session_history)
    
    # Display total hours
    total_hrs_displayed = df_history['Duration (hrs)'].sum()
    st.info(f"📊 Showing {len(df_history)} sessions totaling **{total_hrs_displayed} hours**")
    
    st.dataframe(df_history, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Training Hours Analytics
    st.markdown("## 📈 Training Hours Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Hours Over Time", "By Session Type", "By Competency"])
    
    with tab1:
        # Line chart showing cumulative hours
        hours_data = {
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
            'Hours': [12, 28, 45, 62, 81, 103, 125, 147.5]
        }
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours_data['Week'],
            y=hours_data['Hours'],
            mode='lines+markers',
            name='Cumulative Hours',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        # Add dialogue milestones
        fig.add_hline(y=100, line_dash="dash", line_color="green", 
                     annotation_text="Dialogue #1 (100 hrs)", annotation_position="right")
        fig.add_hline(y=200, line_dash="dash", line_color="orange", 
                     annotation_text="Dialogue #2 (200 hrs)", annotation_position="right")
        
        fig.update_layout(
            title="Cumulative Training Hours Over Time",
            xaxis_title="Week",
            yaxis_title="Total Hours",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Bar chart by session type
        type_data = {
            'Session Type': ['Live Traffic', 'Simulation', 'Peak Hour', 'Emergency', 
                           'Weather Ops', 'Coordination', 'Equipment'],
            'Hours': [45, 32, 28, 15, 12, 10, 5.5]
        }
        
        fig = go.Figure(data=[
            go.Bar(x=type_data['Session Type'], y=type_data['Hours'],
                  marker_color='#2ca02c')
        ])
        
        fig.update_layout(
            title="Training Hours by Session Type",
            xaxis_title="Session Type",
            yaxis_title="Hours",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Radar chart by competency
        competency_data = {
            'Competency': ['Communication', 'Situational Awareness', 'Decision Making', 
                          'Workload Management', 'Teamwork', 'Technical Knowledge',
                          'Procedures', 'Problem Solving'],
            'Hours': [32, 28, 25, 20, 18, 15, 12, 10]
        }
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=competency_data['Competency'],
            y=competency_data['Hours'],
            marker_color='#ff7f0e'
        ))
        
        fig.update_layout(
            title="Training Hours by Competency Area",
            xaxis_title="Competency",
            yaxis_title="Hours",
            height=400,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Export Options
    st.markdown("## 📥 Export Training Records")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.info("PDF generation feature coming soon!")
    
    with col2:
        if st.button("📊 Export to Excel", use_container_width=True):
            csv = df_history.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"training_sessions_{trainee_name.replace(' ', '_')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("📧 Email Summary", use_container_width=True):
            st.info("Email feature coming soon!")


if __name__ == "__main__":
    display_training_session_page()
