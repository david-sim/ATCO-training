"""
Performance Summary page for ATC Training Progress Tracker.
Displays detailed performance analytics and evaluation summaries.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


def display_performance_summary_page():
    """Display the performance summary page."""
    
    st.title("📊 Performance Summary")
    
    st.markdown("""
    Comprehensive performance analysis and evaluation summaries for ATC trainees. 
    This page provides detailed insights into trainee performance across all competency areas.
    """)
    
    st.markdown("---")
    
    # Trainee Selection and Period
    col1, col2, col3 = st.columns(3)
    
    with col1:
        trainee_name = st.selectbox(
            "Select Trainee",
            ["John Smith", "Sarah Johnson", "Michael Chen", "Emily Davis"]
        )
    
    with col2:
        evaluation_period = st.selectbox(
            "Evaluation Period",
            ["Current Month", "Last Month", "Last Quarter", "Year to Date", "All Time"]
        )
    
    with col3:
        report_type = st.selectbox(
            "Report Type",
            ["Comprehensive", "Competency Focus", "Session Summary", "Comparison"]
        )
    
    st.markdown("---")
    
    # Performance Summary Cards
    st.markdown("## 📈 Performance Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Overall Score", "72%", "+5%", help="Overall competency score")
    
    with col2:
        st.metric("Sessions Completed", "24", "+3", help="Training sessions completed")
    
    with col3:
        st.metric("Avg Session Score", "75%", "+2%", help="Average score per session")
    
    with col4:
        st.metric("Assessments Passed", "8/9", "89%", help="Assessments passed")
    
    with col5:
        st.metric("Training Hours", "87.5", "+12.5", help="Total training hours")
    
    st.markdown("---")
    
    # Detailed Competency Breakdown
    st.markdown("## 🎯 Competency Performance Breakdown")
    
    # Sample detailed competency data
    competency_details = {
        'Competency Area': [
            'Communication', 'Situational Awareness', 'Decision Making', 'Workload Management',
            'Teamwork', 'Technical Knowledge', 'Procedures', 'Problem Solving'
        ],
        'Current Score': [85, 78, 70, 68, 82, 75, 80, 65],
        'Previous Period': [82, 75, 68, 66, 80, 72, 78, 62],
        'Target': [85, 85, 85, 85, 85, 85, 85, 85],
        'Status': ['✅ Met', '🟡 Near', '🟡 Near', '🔴 Below', '✅ Met', '🟡 Near', '✅ Met', '🔴 Below']
    }
    
    df_competency = pd.DataFrame(competency_details)
    df_competency['Change'] = df_competency['Current Score'] - df_competency['Previous Period']
    
    st.dataframe(df_competency, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Performance Trends
    st.markdown("## 📉 Performance Trends")
    
    tab1, tab2, tab3 = st.tabs(["📊 By Competency", "📅 Over Time", "🎓 By Session Type"])
    
    with tab1:
        # Bar chart comparing current vs. target
        fig_competency = go.Figure()
        
        fig_competency.add_trace(go.Bar(
            name='Current Score',
            x=competency_details['Competency Area'],
            y=competency_details['Current Score'],
            marker_color='lightblue'
        ))
        
        fig_competency.add_trace(go.Bar(
            name='Target',
            x=competency_details['Competency Area'],
            y=competency_details['Target'],
            marker_color='lightgreen',
            opacity=0.5
        ))
        
        fig_competency.update_layout(
            title='Current Performance vs. Target by Competency',
            xaxis_title='Competency Area',
            yaxis_title='Score (%)',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_competency, use_container_width=True)
    
    with tab2:
        # Line chart showing progress over time for selected competencies
        time_data = {
            'Week': list(range(1, 14)),
            'Communication': [60, 63, 66, 69, 72, 75, 77, 78, 80, 81, 83, 84, 85],
            'Decision Making': [55, 56, 58, 60, 62, 63, 64, 65, 66, 67, 68, 69, 70],
            'Problem Solving': [50, 52, 54, 55, 56, 58, 59, 60, 61, 62, 63, 64, 65]
        }
        
        df_time = pd.DataFrame(time_data)
        
        fig_time = px.line(
            df_time,
            x='Week',
            y=['Communication', 'Decision Making', 'Problem Solving'],
            title='Competency Progress Over Time',
            labels={'value': 'Score (%)', 'variable': 'Competency'},
            markers=True
        )
        
        fig_time.add_hline(y=85, line_dash="dash", line_color="green", 
                          annotation_text="Target (85%)", annotation_position="right")
        
        fig_time.update_layout(height=400)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with tab3:
        # Performance by session type
        session_type_data = {
            'Session Type': ['Simulation', 'Theory', 'Practical', 'Assessment', 'Mentoring'],
            'Avg Score': [74, 82, 76, 71, 78],
            'Sessions': [12, 6, 8, 4, 3]
        }
        
        df_session = pd.DataFrame(session_type_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_session_score = px.bar(
                df_session,
                x='Session Type',
                y='Avg Score',
                title='Average Score by Session Type',
                color='Avg Score',
                color_continuous_scale='RdYlGn'
            )
            fig_session_score.update_layout(height=350)
            st.plotly_chart(fig_session_score, use_container_width=True)
        
        with col2:
            fig_session_count = px.pie(
                df_session,
                values='Sessions',
                names='Session Type',
                title='Training Sessions Distribution'
            )
            fig_session_count.update_layout(height=350)
            st.plotly_chart(fig_session_count, use_container_width=True)
    
    st.markdown("---")
    
    # AI-Powered Performance Analysis
    st.markdown("## 🤖 AI-Powered Performance Analysis")
    
    st.info("""
    **Note:** This feature uses generative AI to analyze performance data and generate 
    comprehensive evaluation summaries, identifying patterns, strengths, and areas for improvement.
    """)
    
    if st.button("🚀 Generate AI Performance Summary", type="primary"):
        with st.spinner("Analyzing performance data and generating summary..."):
            # Placeholder for AI-generated summary
            st.markdown("### 📝 AI-Generated Performance Summary")
            
            st.markdown("""
            **Overall Performance Assessment:**
            
            The trainee has demonstrated consistent progress over the evaluation period, showing 
            particular strength in communication and teamwork competencies. The overall competency 
            score of 72% reflects a solid foundation with clear trajectory toward the target of 85%.
            
            **Key Strengths:**
            
            1. **Communication (85%)**: Exceptional verbal and written communication skills. 
               Consistently demonstrates clear, concise, and professional communication in all 
               scenarios, including high-pressure situations.
            
            2. **Teamwork (82%)**: Strong collaborative abilities. Works effectively with team 
               members, shares information proactively, and contributes positively to team dynamics.
            
            3. **Procedures (80%)**: Solid understanding and application of standard operating 
               procedures. Demonstrates consistency in following established protocols.
            
            **Areas Requiring Development:**
            
            1. **Problem Solving (65%)**: While showing improvement, the trainee needs additional 
               practice in identifying and resolving complex, non-standard situations. Recommend 
               increased exposure to scenario-based training focusing on creative problem-solving.
            
            2. **Workload Management (68%)**: Performance varies under high workload conditions. 
               Suggest targeted training in prioritization techniques and stress management during 
               peak traffic periods.
            
            3. **Decision Making (70%)**: Decision quality is generally good, but speed and 
               confidence need improvement. Recommend time-pressured simulation exercises.
            
            **Performance Trends:**
            
            - Positive upward trajectory in all competency areas
            - Rate of improvement is consistent with training program expectations
            - Most significant gains observed in Communication (+3% month-over-month)
            - Slower progress in Problem Solving and Workload Management areas
            
            **Recommendations:**
            
            1. Continue current training approach for strong competency areas
            2. Increase simulation time focusing on complex scenarios
            3. Implement weekly problem-solving workshops
            4. Schedule additional mentoring sessions with senior controllers
            5. Consider peer learning opportunities in workload management techniques
            
            **Projected Timeline to Target:**
            
            Based on current progress rate, the trainee is on track to achieve the 85% target 
            across all competencies within 3-4 weeks, aligning with the planned training completion 
            timeline.
            """)
            
            st.success("✅ AI performance summary generated successfully!")
            
            st.info("🔮 **Future Enhancement:** This will integrate with actual AI models for dynamic analysis and personalized insights.")
    
    st.markdown("---")
    
    # Recent Assessment Results
    st.markdown("## 📋 Recent Assessment Results")
    
    assessment_data = {
        'Date': ['Apr 15, 2026', 'Apr 8, 2026', 'Apr 1, 2026', 'Mar 25, 2026', 'Mar 18, 2026'],
        'Assessment Type': ['Mid-term', 'Practical', 'Theory', 'Simulation', 'Practical'],
        'Score': [71, 74, 82, 69, 76],
        'Status': ['Pass', 'Pass', 'Pass', 'Pass', 'Pass'],
        'Evaluator': ['R. Williams', 'S. Lee', 'R. Williams', 'M. Anderson', 'S. Lee'],
        'Notes': [
            'Good overall performance',
            'Strong procedural knowledge',
            'Excellent theoretical understanding',
            'Needs work on emergency scenarios',
            'Improved from last assessment'
        ]
    }
    
    df_assessments = pd.DataFrame(assessment_data)
    st.dataframe(df_assessments, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Export Options
    st.markdown("## 📥 Export Performance Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.info("PDF generation feature coming soon!")
    
    with col2:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.info("Excel export feature coming soon!")
    
    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("Email feature coming soon!")
    
    st.markdown("---")
    
    # Declaration Checkbox
    st.markdown("## ✍️ Performance Summary Declaration")
    
    st.markdown("""
    The following declaration confirms that the performance summary has been reviewed and 
    verified by the training manager.
    """)
    
    st.markdown("### 👨‍💼 Training Manager Declaration")
    manager_declares = st.checkbox(
        "I confirm that I have reviewed the performance data and assessments, and certify that this summary accurately reflects the trainee's performance during the evaluation period.",
        key="manager_declaration_ps"
    )
    
    if manager_declares:
        col1, col2 = st.columns(2)
        
        with col1:
            manager_signature = st.text_input("Training Manager Name", value="Robert Williams", disabled=True)
        
        with col2:
            manager_date = st.date_input("Date", value=datetime.now(), key="manager_date_ps")
        
        st.success("✅ Performance summary has been verified and signed off by the training manager.")
    else:
        st.info("ℹ️ Please confirm the declaration to complete the performance summary verification.")
