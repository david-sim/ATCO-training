# ✈️ Pilot Licensing Assessment Tool

An AI-powered pilot licensing assessment system that analyzes pilot logbooks to extract flight data and assess eligibility for various pilot licenses. The tool uses advanced vision AI to read handwritten logbook entries and automatically evaluates license requirements.

## 🚀 Key Features

### 📸 Logbook Image Processing
- **Image Upload**: Upload clear scans or photos of pilot logbook pages
- **AI Vision Analysis**: Automatic extraction of flight data from handwritten entries
- **Multi-Format Support**: Accepts PNG, JPG, JPEG, and PDF formats
- **Smart Data Recognition**: Interprets aviation abbreviations and logbook conventions

### 🤖 AI-Powered Data Extraction
- **Flight Entry Parsing**: Extracts individual flight records including:
  - Date of Flight
  - Aircraft Type and Registration
  - Departure and Arrival Locations
  - Number of Landings
  - Flight Time (Total, PIC, Dual, Cross Country, Night, Instrument)
  - Remarks and Notes
- **Handwriting Recognition**: Handles variations in handwriting styles
- **Abbreviation Interpretation**: Understands common aviation abbreviations (PIC, XC, IFR, etc.)

### 📊 Comprehensive Flight Hour Analysis
- **Automatic Summaries**: Calculates total hours across all categories
- **Hour Breakdown**: Detailed statistics for:
  - Total Flight Time
  - Pilot in Command (PIC) Hours
  - Dual Instruction Hours
  - Cross Country Hours
  - Night Flight Hours
  - Instrument Flight Hours
- **Aircraft Type Tracking**: Identifies unique aircraft types flown
- **Date Range Analysis**: Tracks flight experience timeline

### 🎓 License Eligibility Assessment
- **Multi-License Evaluation**: Assesses eligibility for:
  - **Private Pilot License (PPL)**
  - **Commercial Pilot License (CPL)**
  - **Instrument Rating (IR)**
  - **Airline Transport Pilot License (ATPL)**
- **Requirement Matching**: Compares flight hours against regulatory requirements
- **Gap Analysis**: Identifies missing requirements and hours needed
- **Actionable Recommendations**: Suggests next steps for license attainment

### 📋 Data Export and Reporting
- **Structured Data Export**: Download extracted flight data as CSV
- **Visual Display**: Interactive tables showing all flight entries
- **Summary Statistics**: Clear display of total hours in each category
- **Assessment Reports**: Detailed eligibility status for each license type

## 🏗️ System Requirements

- **Python**: 3.10 or higher
- **Dependencies**: All required packages listed in `requirements.txt`
- **API Access**: OpenAI API key required for AI vision processing (GPT-4o or GPT-4 Vision)

## ⚙️ Setup Instructions

### 1. AI Service Configuration

The application supports both **OpenAI** and **Azure OpenAI** services for vision-based logbook analysis.

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

3. **Configuration Parameters**:
   - `ai_source`: Set to `"azure"` for Azure OpenAI or `"trial"` for regular OpenAI
   - `endpoint`: Your Azure OpenAI resource endpoint URL
   - `model`: Your deployment name (must support vision - gpt-4o recommended)
   - `temperature`: Lower values (0.2-0.3) for more consistent extraction
   - `api_version`: Azure API version (recommended: "2024-08-01-preview")

#### Model Requirements
- **Vision Capability Required**: The model must support image input (GPT-4o, GPT-4 Vision, or equivalent)
- **Recommended Model**: GPT-4o for best performance with handwritten text recognition

### 2. Installation
```bash
# Clone the repository
cd "Pilot Licensing"

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application
```bash
streamlit run streamlit_main.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Upload Logbook Image
1. Take a clear photo or scan of your pilot logbook page(s)
2. Ensure the image is well-lit and text is legible
3. Upload the image using the file uploader (supports PNG, JPG, JPEG, PDF)

### Step 2: Analyze Logbook
1. Click the "🚀 Analyze Logbook" button
2. The AI will process the image and extract flight data
3. Progress updates will appear during processing

### Step 3: Review Results
- **Flight Hours Summary**: View total hours in each category
- **Individual Flight Entries**: See extracted data in tabular format
- **License Assessment**: Review eligibility for different license types
- **Download Data**: Export flight data as CSV for your records

## 📚 Understanding Pilot License Requirements

### Private Pilot License (PPL)
- Minimum 40-50 hours total flight time
- At least 10 hours solo (PIC) time
- At least 5 hours solo cross-country
- At least 3 hours night flight
- At least 3 hours instrument training

### Commercial Pilot License (CPL)
- Minimum 200-250 hours total flight time
- At least 100 hours as PIC
- At least 20 hours cross-country as PIC
- At least 10 hours instrument training
- At least 5 hours night flight

### Instrument Rating (IR)
- Minimum 50 hours cross-country as PIC
- At least 40 hours instrument time
- At least 15 hours with authorized instructor

### Airline Transport Pilot License (ATPL)
- Minimum 1,500 hours total flight time
- At least 500 hours cross-country
- At least 100 hours night flight
- At least 75 hours instrument time
- At least 250 hours as PIC

*Note: Requirements may vary by jurisdiction (FAA, EASA, CAAS, etc.). Always verify with your local aviation authority.*

## 🔧 Configuration

### Logbook Extraction Rules
The system uses AI prompts defined in `config.json` under `logbook_extraction_rules` to:
- Identify logbook columns and structure
- Extract data from handwritten entries
- Interpret aviation abbreviations
- Handle unclear or illegible entries
- Calculate summary statistics

### License Assessment Rules
Assessment logic is defined in `license_assessment_rules` in `config.json`:
- Defines requirements for each license type
- Compares pilot hours against standards
- Generates eligibility status and recommendations

### Customization
You can customize the rules in `config.json` to:
- Adjust extraction prompts for different logbook formats
- Modify license requirements for specific jurisdictions
- Add new license types or ratings
- Change assessment criteria

## 🛠️ Technical Architecture

### Core Components
- **streamlit_main.py**: Main application entry point and UI orchestration
- **logbook_processor.py**: Image processing and data extraction logic
- **ui_components.py**: Reusable UI components and display functions
- **config_manager.py**: Configuration management and API key handling
- **config.json**: AI prompts, rules, and system configuration

### AI Processing Flow
1. User uploads logbook image
2. Image is validated and encoded to base64
3. Vision-enabled LLM analyzes the image
4. AI extracts structured flight data (JSON format)
5. Summary statistics are calculated
6. License assessment LLM evaluates eligibility
7. Results are displayed and available for download

### Data Structure
Extracted flight data includes:
- Individual flight entries (array of objects)
- Summary statistics (totals across categories)
- Raw AI response (for debugging)
- License assessment results

## 🔒 Privacy and Security

- **Local Processing**: Image analysis happens via secure API calls
- **No Data Storage**: Images and results are not permanently stored
- **Session-Based**: Data exists only during your browser session
- **API Security**: Use environment variables or Streamlit secrets for API keys
- **Secure Transmission**: All API calls use HTTPS encryption

## 📝 Tips for Best Results

### Image Quality
- Use good lighting when photographing logbook pages
- Ensure text is in focus and legible
- Avoid shadows or glare on the page
- Higher resolution images yield better results

### Logbook Standards
- Standard aviation logbook formats work best
- Clearly written entries improve accuracy
- Common abbreviations are recognized automatically
- If extraction fails, try a clearer image

### Verification
- Always verify extracted data against your original logbook
- Check summary totals for accuracy
- Cross-reference with any digital logging systems
- Use extracted data as a starting point, not final authority

## 🚧 Limitations

- **Handwriting Variability**: Very poor handwriting may reduce accuracy
- **Image Quality**: Blurry or low-resolution images may not process well
- **Non-Standard Formats**: Custom logbook layouts may need manual review
- **Aviation Authority**: Requirements are general - verify with your specific authority
- **Vision API Dependency**: Requires internet connection and API access

## 🤝 Contributing

Based on the SCOUT (Smart Compliance Operations Unit Tool) framework. This pilot licensing variant demonstrates the versatility of AI-powered document analysis.

## 📞 Support

For technical issues:
1. Check that your API keys are correctly configured
2. Verify image quality and format
3. Review error messages in the application
4. Check the "Debug Info" expander for detailed logs

## 📜 License

This tool is adapted from the SCOUT framework for pilot licensing assessment purposes.

## 🙏 Acknowledgments

- Built with Streamlit for rapid web application development
- Powered by OpenAI GPT-4o for vision and language understanding
- Based on SCOUT compliance checking framework
- Aviation regulations knowledge from FAA, EASA, and ICAO standards

---

**Disclaimer**: This tool provides estimates and assessments based on AI analysis of logbook images. Always verify requirements with your aviation authority and use official records for license applications. The tool is for informational and planning purposes only.
