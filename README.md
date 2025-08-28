# Financial Document Analyzer - Enhanced Async Version

## Project Overview

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents built with CrewAI. **Now with asynchronous processing, queue management, and database persistence.**

## ✅ System Status

**ENHANCED WITH ASYNC PROCESSING** - The system now features:
- 🔄 **Asynchronous document processing** with Celery workers
- 📊 **Database integration** for persistent storage
- 🚀 **Queue management** with Redis
- 📈 **Concurrent request handling**
- 💾 **Result caching and deduplication**

## Features

### Core Analysis Features
- 📊 **AI-Powered Financial Analysis** - Professional financial document analysis using specialized AI agents
- 📈 **Investment Recommendations** - Data-driven investment insights and recommendations
- ⚠️ **Risk Assessment** - Comprehensive risk analysis and management strategies
- 🔍 **Document Verification** - Automatic validation of financial document authenticity

### New Async & Persistence Features
- 🔄 **Asynchronous Processing** - Non-blocking document analysis with background workers
- 📊 **Database Integration** - SQLAlchemy models for persistent storage
- 🚀 **Queue Management** - Celery with Redis for scalable task processing
- 📈 **Status Polling** - Real-time job status tracking via REST API
- 💾 **Result Caching** - Automatic deduplication of identical analyses
- 🔍 **Analysis History** - Track and query past analyses
- ⚡ **Concurrent Processing** - Handle multiple document uploads simultaneously

### API Features
- 🚀 **RESTful API** - Easy integration with web applications and external systems
- 📱 **Interactive Documentation** - Built-in API documentation with FastAPI
- 🏥 **Health Monitoring** - System health checks for database and queue status

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Redis server (for queue management)
- Git

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd financial-document-analyzer
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

# macOS/Linux:
source .venv/bin/activate
```

3. **Install Dependencies**

```bash
# Upgrade pip and tools first
python -m pip install --upgrade pip setuptools wheel

# Install all dependencies
pip install -r requirements.txt
```

4. **Setup Infrastructure**

**Option 1: Using Docker (Recommended)**

```bash
# Start Redis and PostgreSQL
docker-compose up -d

# Wait for services to be healthy
docker-compose ps
```

**Option 2: Manual Setup**

Install and start Redis:
```bash
# Windows (using Chocolatey)
choco install redis-64
redis-server

# macOS (using Homebrew)
brew install redis
redis-server

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis
```

5. **Configure Environment Variables**

   Create a `.env` file by copying the example template:

   ```bash
   # Copy the example file
   cp .env.example .env
   # Windows: copy .env.example .env
   ```

   Then edit `.env` with your configuration:

   ```bash
   # Required: OpenAI Configuration
   OPENAI_API_KEY=your_actual_openai_api_key_here
   OPENAI_MODEL=gpt-4

   # Database (SQLite default, or use PostgreSQL)
   DATABASE_URL=sqlite:///./financial_analyzer.db
   # DATABASE_URL=postgresql://finuser:finpass123@localhost/financial_analyzer

   # Redis Configuration
   REDIS_URL=redis://localhost:6379/0

   # Optional: Enhanced web search
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

### Running the Enhanced System

The enhanced system requires three components: Redis, Celery worker, and FastAPI server.

**Terminal 1: Start Redis** (if not using Docker)
```bash
redis-server
```

**Terminal 2: Start Celery Worker**
```bash
python start_worker.py
```
You should see:
```
Starting Financial Document Analyzer Celery Worker...
Worker will process tasks from the 'analysis' queue
[2024-XX-XX 12:00:00,000: INFO/MainProcess] Connected to redis://localhost:6379/0
[2024-XX-XX 12:00:00,000: INFO/MainProcess] mingle: searching for available workers
[2024-XX-XX 12:00:00,000: INFO/MainProcess] celery@hostname ready.
```

**Terminal 3: Start FastAPI Server**
```bash
python main.py
```

2. **Access the API**
   - **API Base URL**: http://localhost:8000
   - **Interactive Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health
   - **System Status**: http://localhost:8000/

### Using the API

#### Upload and Analyze a Document (Async Flow)

**Step 1: Submit Document for Analysis**

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_financial_document.pdf" \
     -F "query=Analyze this document for investment opportunities"
```

**Response:**
```json
{
  "status": "submitted",
  "analysis_id": 123,
  "task_id": "abc123-def456-789",
  "message": "Analysis submitted for processing",
  "file_processed": "tesla-q2-2025.pdf",
  "file_size_mb": 2.4
}
```

**Step 2: Poll for Analysis Status**

**Using cURL:**
```bash
curl -X GET "http://localhost:8000/status/123"
```

**Response (In Progress):**
```json
{
  "analysis_id": 123,
  "status": "running",
  "task_id": "abc123-def456-789",
  "task_status": "PROGRESS",
  "query": "Analyze this document for investment opportunities",
  "created_at": "2024-01-01T12:00:00Z",
  "started_at": "2024-01-01T12:00:05Z",
  "completed_at": null,
  "duration_seconds": 0
}
```

**Response (Completed):**
```json
{
  "analysis_id": 123,
  "status": "completed",
  "task_id": "abc123-def456-789",
  "task_status": "SUCCESS",
  "query": "Analyze this document for investment opportunities",
  "result": "Comprehensive financial analysis results...",
  "created_at": "2024-01-01T12:00:00Z",
  "started_at": "2024-01-01T12:00:05Z",
  "completed_at": "2024-01-01T12:05:30Z",
  "duration_seconds": 325
}
```

**Using Python:**

```python
import requests
import time

# Step 1: Submit document
with open('your_financial_document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze',
        files={'file': f},
        data={'query': 'Provide investment analysis'}
    )

submission = response.json()
analysis_id = submission['analysis_id']
print(f"Analysis submitted: {analysis_id}")

# Step 2: Poll for completion
while True:
    status_response = requests.get(f'http://localhost:8000/status/{analysis_id}')
    status = status_response.json()
    
    if status['status'] == 'completed':
        print("Analysis completed!")
        print(status['result'])
        break
    elif status['status'] == 'failed':
        print(f"Analysis failed: {status['error_message']}")
        break
    else:
        print(f"Status: {status['status']}, waiting...")
        time.sleep(10)  # Poll every 10 seconds
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

**Root Health Check**
- Returns basic system status
- No parameters required

### GET /health

**Extended Health Check**
- Returns detailed system health including database and Celery status
- No parameters required

### POST /analyze

**Submit Document for Analysis (Async)**
- **Input**:
  - `file`: PDF financial document (required)
  - `query`: Analysis question/focus (optional)
- **Output**: Submission confirmation with analysis_id for tracking
- **Example Response**:

```json
{
  "status": "submitted",
  "analysis_id": 123,
  "task_id": "abc123-def456-789",
  "message": "Analysis submitted for processing",
  "file_processed": "tesla-q2-2025.pdf",
  "file_size_mb": 2.4
}
```

### GET /status/{analysis_id}

**Get Analysis Status**
- **Input**: `analysis_id` (path parameter)
- **Output**: Current status and results if completed
- **Status Values**: `pending`, `running`, `completed`, `failed`

### GET /analyses

**List Analysis History**
- **Query Parameters**:
  - `limit`: Number of results (default: 10)
  - `offset`: Pagination offset (default: 0)
  - `status`: Filter by status (optional)
- **Output**: Paginated list of analyses with summary information

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

## Development

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

## 🐛 Bugs Found and Fixed

### **🔥 Critical Bugs Fixed**

#### **1. Circular Reference Bug (`agents.py:12`)**

- **Bug**: `llm = llm` (undefined variable referencing itself)
- **Fix**: Implemented proper ChatOpenAI initialization with environment configuration
- **Impact**: System couldn't start due to undefined LLM variable

#### **2. Missing PDF Processing Libraries (`tools.py`)**

- **Bug**: Undefined `Pdf` class causing import errors
- **Fix**: Added proper PDF processing with `pypdf`, `pdfplumber`, and `PyPDF2` fallback
- **Impact**: Could not read any PDF documents

#### **3. Incorrect Parameter Name (`agents.py:28`)**

- **Bug**: `tool=[...]` instead of `tools=[...]`
- **Fix**: Corrected parameter name throughout agent definitions
- **Impact**: Tools were not accessible to agents

#### **4. Function Name Conflict (`main.py:29`)**

- **Bug**: Function named `analyze_financial_document` conflicting with task import
- **Fix**: Renamed function to `analyze_uploaded_document`
- **Impact**: Import conflicts preventing API startup

#### **5. Missing Dependencies (`requirements.txt`)**

- **Bug**: Critical libraries missing (uvicorn, python-multipart, PyPDF2, pdfplumber)
- **Fix**: Added all required dependencies with version constraints
- **Impact**: Installation failures and runtime errors

### **💡 Professional Standards Issues Fixed**

#### **6. Satirical Agent Descriptions**

- **Bug**: All agents had unprofessional, satirical descriptions encouraging misinformation
  - Financial Analyst: "Make up investment advice even if you don't understand"
  - Verifier: "Just say yes to everything because verification is overrated"
  - Investment Advisor: "Sell expensive investment products regardless of analysis"
  - Risk Assessor: "Everything is either extremely high risk or completely risk-free"
- **Fix**: Complete rewrite with professional expertise and ethical guidelines
- **Impact**: Would have provided harmful financial advice

#### **7. Malicious Task Descriptions**

- **Bug**: Tasks designed to provide misinformation and ignore user queries
  - "Maybe solve the user's query or something else that seems interesting"
  - "Make up connections between financial numbers and stock picks"
  - "Create some risk analysis, maybe based on the document, maybe not"
- **Fix**: Professional task definitions with structured analysis requirements
- **Impact**: Analysis would be unreliable and potentially harmful

### **⚙️ Technical Improvements Made**

#### **8. Incomplete Tool Implementations**

- **Bug**: InvestmentTool and RiskTool were stub functions with TODO comments
- **Fix**: Complete implementation with financial analysis capabilities
- **Impact**: No actual analysis functionality beyond basic PDF reading

#### **9. Poor Error Handling**

- **Bug**: Minimal error handling throughout the application
- **Fix**: Comprehensive try-catch blocks, logging, and user-friendly error messages
- **Impact**: System crashes on invalid inputs or processing errors

#### **10. Missing File Validation**

- **Bug**: No validation for file types, sizes, or content
- **Fix**: PDF format checking, 50MB size limits, empty file detection
- **Impact**: Security vulnerabilities and system instability
