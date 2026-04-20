# 🎯 ATC Training Progress Tracker

An AI-powered training management system for Air Traffic Controller trainees. The system provides comprehensive progress tracking, competency monitoring, training plan management, performance analytics, and validation assessments throughout the ATC training journey.

## 🚀 Key Features

### 📊 Dashboard & Progress Tracking
- **Real-Time Monitoring**: Track trainee progress across eight core competency areas
- **Visual Analytics**: Interactive charts and graphs displaying competency trends
- **Progress Timeline**: Historical view of trainee development over time
- **Metrics Overview**: Quick insights into overall competency scores and training status

### 🎯 Core Competency Areas
The system tracks performance across eight essential ATC competencies:
1. **Communication**: Verbal and written communication effectiveness
2. **Situational Awareness**: Ability to maintain awareness of all operational elements
3. **Decision Making**: Quality and speed of operational decisions
4. **Workload Management**: Capacity to handle multiple tasks under pressure
5. **Teamwork**: Collaboration and coordination with colleagues
6. **Technical Knowledge**: Understanding of regulations, procedures, and equipment
7. **Procedures**: Adherence to standard operating procedures
8. **Problem Solving**: Ability to identify and resolve issues effectively

### 📋 Training Plan Management
- **Collaborative Planning**: Discuss and develop training plans with training managers
- **Activity Scheduling**: Plan and schedule training sessions and activities
- **Focus Area Identification**: Identify areas requiring additional training
- **AI-Powered Recommendations**: Get personalized training suggestions based on performance data
- **Meeting Documentation**: Record training plan discussions and action items

### 📈 Performance Summary
- **Comprehensive Analytics**: Detailed performance analysis across all competency areas
- **Trend Analysis**: Track performance improvements and identify patterns
- **Session Tracking**: Monitor performance by training session type
- **Assessment History**: Complete record of all assessments and evaluations
- **Comparative Analysis**: Compare performance against cohort and standards
- **AI-Generated Insights**: Automated performance summaries and recommendations

### ✅ Validation Assessment
- **Assessment Scheduling**: Plan and schedule formal validation assessments
- **Structured Evaluation**: Comprehensive assessment forms for each competency area
- **Certification Tracking**: Monitor progress toward certification requirements
- **Assessment History**: Complete record of all validation assessments
- **AI-Powered Analysis**: Predictive insights for certification readiness

### 🤖 AI-Powered Features
- **Performance Analysis**: AI analyzes trainee data to identify patterns and trends
- **Personalized Recommendations**: Tailored training suggestions based on individual needs
- **Automated Summaries**: AI-generated performance reports and evaluations
- **Predictive Modeling**: Estimate time to certification and competency targets
- **Risk Identification**: Highlight areas requiring immediate attention

## 🏗️ System Requirements

- **Python**: 3.10 or higher
- **Dependencies**: All required packages listed in `requirements.txt`
- **API Access**: OpenAI API key for AI-powered features (GPT-4o recommended)

## ⚙️ Setup Instructions

### 1. AI Service Configuration

The application supports both **OpenAI** and **Azure OpenAI** services for AI-powered insights.

#### OpenAI Configuration (Default)
Add your OpenAI API key using one of these methods:
- **Streamlit Secrets**: Add to `.streamlit/secrets.toml`
  ```toml
  OPENAI_API_KEY = "your-api-key-here"
  ```
- **Environment Variable**: 
  ```bash
  export OPENAI_API_KEY="your-api-key-here"
  ```

#### Azure OpenAI Configuration
To use Azure OpenAI instead:

1. **Add Azure API Key** to `.streamlit/secrets.toml`:
   ```toml
   AZURE_API_KEY = "your-azure-api-key-here"
   ```

2. **Update Configuration**: Edit `config.json` to switch AI source:
   ```json
   {
     "ai_source": "azure",
     "azure_llm": {
       "endpoint": "https://your-resource.openai.azure.com/",
       "model": "gpt-4o",
       "temperature": "0.3",
       "api_version": "2024-08-01-preview"
     }
   }
   ```

### 2. Installation
```bash
# Navigate to the project directory
cd ATCO-training

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application
```bash
streamlit run streamlit_main.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

### Dashboard
1. View trainee overview with key metrics
2. Monitor competency scores across all eight areas
3. Review competency radar chart showing current vs. target levels
4. Track progress timeline over the training period
5. Review recent training sessions

### Training Plan
1. Select trainee from dropdown
2. Review current training plan status
3. Add new training activities to the plan
4. Generate AI-powered training recommendations
5. Document training plan discussion notes

### Performance Summary
1. Select trainee and evaluation period
2. Review overall performance metrics
3. Analyze competency breakdown and trends
4. View performance by session type
5. Generate AI-powered performance analysis
6. Export performance reports

### Validation Assessment
1. Schedule new assessments
2. Conduct assessments using structured evaluation forms
3. Rate competencies and document observations
4. Generate AI-powered assessment insights
5. Review assessment history
6. Track certification progress

## 🎓 Competency Scoring Framework

### Proficient (80-100%)
- Consistently meets or exceeds standards
- Demonstrates mastery of competency
- Requires minimal guidance
- Ready for independent operation

### Developing (70-79%)
- Generally meets standards
- Shows ongoing progress
- Requires some supervision
- On track for proficiency

### Needs Improvement (<70%)
- Below expected standards
- Requires focused training
- Needs close supervision
- Improvement plan required

### Target Performance
All trainees must achieve **85% or higher** across all eight competency areas for certification.

## 🔧 Configuration

### AI Rules
The system uses AI prompts defined in `config.json`:
- **Performance Analysis Rules**: Guide AI in analyzing trainee performance data
- **Training Recommendation Rules**: Define how AI generates training suggestions
- **Assessment Evaluation Rules**: Structure AI-powered assessment insights
- **ATC Competency Framework**: Define standards and requirements for each competency

### Customization
You can customize the rules in `config.json` to:
- Adjust AI analysis prompts
- Modify competency framework definitions
- Change target performance thresholds
- Add new competency areas
- Customize assessment criteria

## 🛠️ Technical Architecture

### Core Components
- **streamlit_main.py**: Main application entry point and page routing
- **dashboard_page.py**: Main dashboard with progress tracking and metrics
- **training_plan_page.py**: Training plan management and discussions
- **performance_summary_page.py**: Detailed performance analytics
- **validation_assessment_page.py**: Assessment scheduling and evaluation
- **ui_components.py**: Reusable UI components and navigation
- **config_manager.py**: Configuration management and API key handling
- **about_page.py**: Project information and overview
- **methodology_page.py**: System methodology and best practices
- **config.json**: AI prompts, rules, and system configuration

### Page Structure
1. **Dashboard**: Overview and real-time progress tracking
2. **Training Plan**: Collaborative planning and AI recommendations
3. **Performance Summary**: Comprehensive analytics and insights
4. **Validation Assessment**: Formal assessments and certification tracking
5. **About Us**: Project information and objectives
6. **Methodology**: System processes and best practices

### Data Visualization
- **Plotly**: Interactive charts and graphs
- **Pandas**: Data processing and analytics
- **Streamlit**: Modern web interface and components

## 🔒 Privacy and Security

- **Session-Based Data**: Data exists only during browser session
- **API Security**: Use environment variables or Streamlit secrets for API keys
- **Secure Transmission**: All API calls use HTTPS encryption
- **No External Storage**: Training data remains within your environment

## 📝 Best Practices

### For Training Managers
- Conduct weekly training plan reviews
- Use AI recommendations as guidance, not directives
- Document all assessment observations thoroughly
- Provide timely, constructive feedback
- Monitor trends across multiple trainees

### For Trainees
- Review dashboard regularly to track progress
- Be proactive in identifying focus areas
- Engage actively in training plan discussions
- Prepare for assessments by reviewing history
- Use AI insights for self-directed learning

### For Administrators
- Ensure data accuracy and completeness
- Conduct regular system configuration reviews
- Monitor AI model performance
- Generate periodic effectiveness reports
- Maintain certification standards

## 🚀 Future Enhancements

### Planned Features
- **Database Integration**: Persistent data storage
- **Multi-Trainee Comparison**: Cohort analysis and benchmarking
- **Email Notifications**: Automated alerts and reminders
- **Report Generation**: PDF export for assessments and summaries
- **Mobile Optimization**: Responsive design for mobile devices
- **Advanced Analytics**: Machine learning for performance prediction
- **Integration APIs**: Connect with existing training management systems

### AI Enhancements
- Real-time performance analysis during training sessions
- Automated competency gap detection
- Dynamic training path optimization
- Predictive certification timeline modeling
- Natural language query interface

## 🚧 Current Status

This is an active development project. The current version includes:
- ✅ Complete dashboard with competency tracking
- ✅ Training plan management interface
- ✅ Performance summary and analytics
- ✅ Validation assessment system
- ✅ AI integration placeholders for future enhancement
- ✅ Modern, intuitive UI design

### Note on AI Features
AI-powered features currently show placeholder content demonstrating the intended functionality. Future versions will integrate with actual AI models for:
- Real-time performance analysis
- Dynamic training recommendations
- Automated summary generation
- Predictive modeling

## 📞 Support

For questions, issues, or feature requests:
- Review the methodology page within the application
- Check configuration settings in `config.json`
- Consult your training administrator
- Contact system support team

## 📄 License

This project is developed for Air Traffic Controller training management purposes.

---

**Powered by OpenAI GPT-4o | Built with Streamlit**


**Disclaimer**: This tool provides AI-assisted analysis and recommendations for ATC training progress tracking. Always verify training requirements with your ATC training organization and use official records for certification and licensing purposes. The tool is for informational and planning purposes only.
