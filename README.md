## Updated README.md with complete instructions and system status
## Old README had debug instructions and broken setup information
# Financial Document Analyzer

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents built with CrewAI.

## ✅ System Status
**FULLY FUNCTIONAL** - All bugs have been fixed and the system is ready for production use.

## Features
- 📊 **AI-Powered Financial Analysis** - Professional financial document analysis using specialized AI agents
- 📈 **Investment Recommendations** - Data-driven investment insights and recommendations
- ⚠️ **Risk Assessment** - Comprehensive risk analysis and management strategies
- 🔍 **Document Verification** - Automatic validation of financial document authenticity
- 🚀 **RESTful API** - Easy integration with web applications and external systems
- 📱 **Interactive Documentation** - Built-in API documentation with FastAPI

## Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Git

## Updated installation with optimized approach for better reliability
## Old installation method had timeout issues with large dependency list
### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd financial-document-analyzer-debug
```

2. **Create Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows Git Bash:
source .venv/Scripts/activate

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt:
.venv\Scripts\activate.bat
```

3. **Install Required Libraries (Optimized)**
```bash
# Upgrade pip and tools first
python -m pip install --upgrade pip setuptools wheel

# Install core dependencies in chunks (faster and more reliable)
pip install crewai==0.130.0 crewai-tools==0.47.1
pip install fastapi==0.110.3 uvicorn==0.29.0
pip install langchain-community==0.2.14 pypdf==4.2.0
pip install python-dotenv==1.0.1 openai==1.30.5

# Install remaining dependencies
pip install PyPDF2==3.0.1 pdfplumber==0.10.0 python-multipart==0.0.9
pip install pandas==2.2.2 numpy==1.26.4 scikit-learn==1.4.2
```

4. **Alternative: Install All at Once**
```bash
pip install -r requirements.txt
```

5. **Configure Environment Variables**
   
   Create a `.env` file by copying the example template:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit the .env file with your API keys
   # Windows users can use: copy .env.example .env
   ```
   
   Then edit `.env` and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_actual_openai_api_key_here
   OPENAI_MODEL=gpt-4
   
   # Optional: Add Serper API key for enhanced web search
   SERPER_API_KEY=your_serper_api_key_here
   ```
   
   **Get your OpenAI API key**: https://platform.openai.com/api-keys

### Sample Document
The system analyzes financial documents like Tesla's Q2 2025 financial update (included in the `data/` folder).

**Supported Document Types:**
- Annual Reports (10-K)
- Quarterly Reports (10-Q)  
- Earnings Reports
- Financial Statements
- Investment Prospectuses
- Corporate Financial Updates

**Document Requirements:**
- PDF format only
- Maximum file size: 50MB
- Must contain readable financial data

## 🚀 Quick Start

### Running the Application

1. **Start the server**
```bash
python main.py
```

2. **Access the API**
   - **API Base URL**: http://localhost:8000
   - **Interactive Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/

### Using the API

#### Upload and Analyze a Document

**Option 1: Using the Web Interface**
1. Go to http://localhost:8000/docs
2. Click on the `POST /analyze` endpoint
3. Click "Try it out"
4. Upload your PDF file
5. Enter your analysis query (optional)
6. Click "Execute"

**Option 2: Using cURL**
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_financial_document.pdf" \
     -F "query=Analyze this document for investment opportunities"
```

**Option 3: Using Python**
```python
import requests

with open('your_financial_document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze',
        files={'file': f},
        data={'query': 'Provide investment analysis'}
    )
    
analysis = response.json()
print(analysis['analysis'])
```

## System Capabilities

### ✅ Core Features
- ✅ **Upload financial documents** (PDF format)
- ✅ **AI-powered financial analysis** using GPT-4
- ✅ **Investment recommendations** with valuation metrics
- ✅ **Risk assessment** with quantitative scoring
- ✅ **Market insights** and professional analysis
- ✅ **Document verification** and quality validation
- ✅ **Multi-agent analysis** with specialized expertise

### 🤖 AI Agents

1. **Financial Analyst** - Comprehensive financial analysis and metrics evaluation
2. **Investment Advisor** - Investment recommendations and portfolio guidance  
3. **Risk Assessor** - Risk quantification and mitigation strategies
4. **Document Verifier** - Document validation and quality assessment

### 📊 Analysis Output

The system provides structured analysis including:
- **Executive Summary** with key findings
- **Financial Performance Analysis** with trends and ratios
- **Investment Thesis** with recommendations
- **Risk Assessment** with scoring and mitigation
- **Professional Insights** based on industry standards

## API Endpoints

### GET /
**Health Check**
- Returns system status
- No parameters required

### POST /analyze
**Document Analysis**
- **Input**: 
  - `file`: PDF financial document (required)
  - `query`: Analysis question/focus (optional)
- **Output**: Comprehensive financial analysis JSON response
- **Example Response**:
```json
{
  "status": "success",
  "query": "Analyze investment opportunities",
  "analysis": "Comprehensive analysis report...",
  "file_processed": "tesla-q2-2025.pdf",
  "file_size_mb": 2.4
}
```

## Configuration

### Environment Variables (.env)
```bash
# OpenAI Configuration (already configured)
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4

# Optional: Web Search API
SERPER_API_KEY=your_serper_api_key_here
```

### Customizing Analysis

You can customize your analysis by providing specific queries:

- **Investment Focus**: "Analyze this company for long-term investment potential"
- **Risk Focus**: "What are the primary risk factors for this investment?"
- **Performance Focus**: "Evaluate the financial performance trends"
- **Valuation Focus**: "Is this stock overvalued or undervalued?"
- **Comparison Focus**: "How does this company compare to industry peers?"

## Troubleshooting

### Common Issues

**1. API Key Error**
```
Error: OpenAI API key not found
```
**Solution**: Check that your `.env` file contains a valid `OPENAI_API_KEY`

**2. PDF Processing Error**
```
Error: Could not extract text from PDF
```
**Solution**: Ensure the PDF contains readable text (not just images) and isn't corrupted

**3. File Too Large**
```
Error: File too large (max 50MB)
```
**Solution**: Compress your PDF or split large documents into smaller sections

**4. Invalid File Format**
```
Error: Only PDF files are supported
```
**Solution**: Convert your document to PDF format before uploading

### Getting Help

1. **Check the logs**: The application provides detailed logging for debugging
2. **Verify dependencies**: Ensure all packages in `requirements.txt` are installed
3. **Test with sample**: Try the included sample document first
4. **API Documentation**: Visit http://localhost:8000/docs for interactive testing

## Project Structure

```
financial-document-analyzer-debug/
├── main.py              # FastAPI application and server
├── agents.py            # AI agent definitions
├── task.py             # Analysis task definitions  
├── tools.py            # Document processing and analysis tools
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration
├── data/              # Document storage directory
│   └── TSLA-Q2-2025-Update.pdf
├── outputs/           # Analysis output directory
├── README.md          # This file
├── CHANGES.md         # Complete change documentation
└── PROJECT_OVERVIEW.md # System architecture guide
```

## Development

### Adding New Features

1. **New Analysis Agents**: Add to `agents.py`
2. **Custom Tools**: Extend `tools.py`
3. **Additional Tasks**: Define in `task.py`
4. **API Endpoints**: Add to `main.py`

### Testing

Test the system with various financial documents:
```bash
# Start the server
python main.py

# Test with cURL
curl -X POST "http://localhost:8000/analyze" \
     -F "file=@data/TSLA-Q2-2025-Update.pdf" \
     -F "query=Investment analysis"
```

## License

This project is for educational and research purposes. Please ensure compliance with all applicable financial regulations when using for commercial purposes.

## Disclaimer

This system provides educational analysis only and should not be considered as professional financial advice. Always consult with qualified financial advisors for investment decisions.
