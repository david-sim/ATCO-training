"""
Main Dashboard page for Air Traffic Controller Training Progress Tracker.
Displays trainee overview, competency metrics, and progress charts.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_timeline import timeline


def display_dashboard():
    """Display the main ATC trainee progress dashboard."""
    
    st.title("🎯 ATC Trainee Progress Dashboard")
    
    # Trainee Overview Section
    st.markdown("## 👤 Trainee Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Trainee Name",
            value="John Smith",
            help="Current trainee being tracked"
        )
    
    with col2:
        st.metric(
            label="Training Start Date",
            value="Jan 15, 2026",
            help="Date when training commenced"
        )
    
    with col3:
        st.metric(
            label="Training Duration",
            value="95 Days",
            delta="65% Complete",
            help="Time elapsed in training program"
        )
    
    with col4:
        st.metric(
            label="Overall Competency",
            value="72%",
            delta="+5%",
            help="Overall competency score"
        )
    
    st.markdown("---")
    
    # Training Journey Timeline
    st.markdown("## 📅 Training Journey Timeline")
    
    # Create timeline data
    timeline_data = {
        "title": {
            "text": {
                "headline": "ATC Training Journey",
                "text": "Key milestones and achievements in John Smith's training program"
            }
        },
        "events": [
            {
                "start_date": {
                    "year": "2026",
                    "month": "1",
                    "day": "15"
                },
                "text": {
                    "headline": "Training Program Started",
                    "text": "John Smith commenced ATC training program. Initial assessment conducted and baseline competencies established."
                },
                "media": {
                    "url": "",
                    "caption": ""
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "1",
                    "day": "22"
                },
                "text": {
                    "headline": "Foundation Phase Completed",
                    "text": "Successfully completed foundational training covering basic ATC procedures and communication protocols."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "2",
                    "day": "5"
                },
                "text": {
                    "headline": "First Simulation Session",
                    "text": "Completed first simulation exercise in tower operations. Score: 68% - Good performance for first attempt."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "2",
                    "day": "15"
                },
                "text": {
                    "headline": "Initial Assessment Passed",
                    "text": "Successfully passed initial competency assessment with score of 65%. Cleared to proceed to intermediate phase."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "3",
                    "day": "1"
                },
                "text": {
                    "headline": "Intermediate Phase Started",
                    "text": "Began intermediate training focusing on traffic management and decision making under realistic conditions."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "3",
                    "day": "18"
                },
                "text": {
                    "headline": "Practical Assessment - Good Performance",
                    "text": "Completed practical assessment in live traffic scenarios. Score: 76% - Demonstrated strong procedural knowledge."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "4",
                    "day": "1"
                },
                "text": {
                    "headline": "Theory Assessment - Excellent",
                    "text": "Achieved excellent score of 82% in theory assessment covering regulations and technical knowledge."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "4",
                    "day": "15"
                },
                "text": {
                    "headline": "Mid-term Evaluation",
                    "text": "Mid-term evaluation completed. Overall competency: 71%. On track for certification target."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "4",
                    "day": "20"
                },
                "text": {
                    "headline": "Current Position",
                    "text": "Currently at 72% overall competency. Recommended focus: Problem Solving and Workload Management."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "4",
                    "day": "25"
                },
                "text": {
                    "headline": "Upcoming: Quarterly Validation",
                    "text": "Scheduled quarterly validation assessment to evaluate progress across all competency areas."
                }
            },
            {
                "start_date": {
                    "year": "2026",
                    "month": "5",
                    "day": "14"
                },
                "text": {
                    "headline": "Target: Final Certification",
                    "text": "Target date for final certification assessment. Required competency: 85% across all areas."
                }
            }
        ]
    }
    
    # Display timeline
    timeline(timeline_data, height=500)
    
    st.markdown("---")
    
    # Competency Metrics Section
    st.markdown("## 📊 Competency Metrics")
    
    # Sample competency data
    competencies = {
        "Communication": 85,
        "Situational Awareness": 78,
        "Decision Making": 70,
        "Workload Management": 68,
        "Teamwork": 82,
        "Technical Knowledge": 75,
        "Procedures": 80,
        "Problem Solving": 65
    }
    
    # Create competency metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    competency_items = list(competencies.items())
    for idx, (competency, score) in enumerate(competency_items):
        col = [col1, col2, col3, col4][idx % 4]
        with col:
            # Color based on score
            if score >= 80:
                delta_color = "normal"
                emoji = "✅"
            elif score >= 70:
                delta_color = "normal"
                emoji = "🟡"
            else:
                delta_color = "inverse"
                emoji = "🔴"
            
            st.metric(
                label=f"{emoji} {competency}",
                value=f"{score}%",
                help=f"Current proficiency in {competency}"
            )
    
    st.markdown("---")
    
    # Competency Radar Chart
    st.markdown("### 📈 Competency Profile")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=list(competencies.values()),
            theta=list(competencies.keys()),
            fill='toself',
            name='Current Level',
            line_color='#1f77b4'
        ))
        
        # Add target level (85%)
        target_values = [85] * len(competencies)
        fig.add_trace(go.Scatterpolar(
            r=target_values,
            theta=list(competencies.keys()),
            fill='toself',
            name='Target Level',
            line_color='#2ca02c',
            opacity=0.3
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Competency Summary")
        st.markdown(f"""
        **Strengths:**
        - Communication ({competencies['Communication']}%)
        - Teamwork ({competencies['Teamwork']}%)
        - Procedures ({competencies['Procedures']}%)
        
        **Areas for Improvement:**
        - Problem Solving ({competencies['Problem Solving']}%)
        - Workload Management ({competencies['Workload Management']}%)
        - Decision Making ({competencies['Decision Making']}%)
        
        **Overall Progress:** 72%
        
        **Target:** 85% across all competencies
        """)
    
    st.markdown("---")
    
    # Progress Timeline
    st.markdown("### 📅 Training Progress Timeline")
    
    # Sample timeline data
    timeline_data = {
        'Date': pd.date_range(start='2026-01-15', periods=13, freq='W'),
        'Overall Competency': [45, 48, 52, 55, 58, 62, 65, 67, 68, 69, 70, 71, 72]
    }
    
    df_timeline = pd.DataFrame(timeline_data)
    
    # Create line chart
    fig_timeline = px.line(
        df_timeline, 
        x='Date', 
        y='Overall Competency',
        title='Overall Competency Progress Over Time',
        labels={'Overall Competency': 'Competency Score (%)'},
        markers=True
    )
    
    # Add target line
    fig_timeline.add_hline(
        y=85, 
        line_dash="dash", 
        line_color="green",
        annotation_text="Target (85%)",
        annotation_position="right"
    )
    
    fig_timeline.update_layout(height=400)
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.markdown("---")
    
    # Training Sessions Summary
    st.markdown("## 📚 Recent Training Sessions")
    
    # Sample training sessions data
    sessions_data = {
        'Date': ['Apr 18, 2026', 'Apr 15, 2026', 'Apr 12, 2026', 'Apr 10, 2026', 'Apr 8, 2026'],
        'Session Type': ['Simulation', 'Theory', 'Practical', 'Simulation', 'Assessment'],
        'Duration (hrs)': [2.5, 1.5, 3.0, 2.0, 1.5],
        'Focus Area': ['Emergency Procedures', 'Regulations', 'Tower Operations', 'Traffic Management', 'Mid-term Assessment'],
        'Performance': ['Good', 'Excellent', 'Good', 'Fair', 'Good']
    }
    
    df_sessions = pd.DataFrame(sessions_data)
    
    # Style the performance column
    def highlight_performance(val):
        if val == 'Excellent':
            return 'background-color: #90EE90'
        elif val == 'Good':
            return 'background-color: #FFFFE0'
        elif val == 'Fair':
            return 'background-color: #FFE4B5'
        else:
            return ''
    
    styled_df = df_sessions.style.map(highlight_performance, subset=['Performance'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Upcoming Milestones
    st.markdown("## 🎯 Upcoming Milestones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📅 Next Assessment: Apr 25, 2026**
        - Type: Quarterly Validation Assessment
        - Focus: All competency areas
        - Duration: 4 hours
        """)
    
    with col2:
        st.info("""
        **🎓 Training Completion Target: May 14, 2026**
        - Total Days: 120 days
        - Remaining: 25 days
        - Required Competency: 85%
        """)
    
    # Quick Actions
    st.markdown("---")
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Schedule Training Session", use_container_width=True):
            st.info("Training session scheduling feature coming soon!")
    
    with col2:
        if st.button("📊 Generate Progress Report", use_container_width=True):
            st.info("Progress report generation feature coming soon!")
    
    with col3:
        if st.button("💬 Request Feedback", use_container_width=True):
            st.info("Feedback request feature coming soon!")
