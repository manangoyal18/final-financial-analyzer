## Fixed imports and added proper error handling imports
## Old code was missing import for all agents and tasks, plus logging
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import sys, asyncio
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import logging
from typing import Dict, Any

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, verification, investment_analysis, risk_assessment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Financial Document Analyzer")

## Enhanced crew function with all agents and comprehensive task flow
## Old code only used one agent and one task, missing comprehensive analysis
def run_crew(query: str, file_path: str = "data/sample.pdf") -> Dict[str, Any]:
    """Run the complete financial analysis crew with all agents and tasks"""
    try:
        # Create comprehensive crew with all agents
        financial_crew = Crew(
            agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
            tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
            process=Process.sequential,
            verbose=True
        )
        
        # Prepare inputs with both query and file path
        crew_inputs = {
            'query': query,
            'file_path': file_path
        }
        
        logger.info(f"Starting financial analysis for query: {query}")
        logger.info(f"Processing file: {file_path}")
        
        result = financial_crew.kickoff(crew_inputs)
        
        logger.info("Financial analysis completed successfully")
        return {
            "status": "success",
            "analysis_result": str(result),
            "query_processed": query,
            "file_analyzed": file_path
        }
        
    except Exception as e:
        logger.error(f"Error in crew execution: {str(e)}")
        return {
            "status": "error",
            "error_message": str(e),
            "query_processed": query,
            "file_analyzed": file_path
        }

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

## Fixed function name conflict and enhanced error handling
## Old code had function name conflict with imported task 'analyze_financial_document'
@app.post("/analyze")
async def analyze_uploaded_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
## Enhanced file processing with better validation and error handling
## Old code had minimal error handling and file validation
    # Input validation
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
        
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        logger.info(f"Processing uploaded file: {file.filename}")
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file with size validation
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
            
        if len(content) > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(status_code=400, detail="File too large (max 50MB)")
            
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
            
        query = query.strip()
        
        # Process the financial document with all analysts
        logger.info(f"Starting analysis with query: {query}")
        response = run_crew(query=query, file_path=file_path)
        
        # Check if analysis was successful
        if response.get("status") == "error":
            raise HTTPException(
                status_code=500, 
                detail=f"Analysis failed: {response.get('error_message', 'Unknown error')}"
            )
        
        return {
            "status": "success",
            "query": query,
            "analysis": response.get("analysis_result", "Analysis completed"),
            "file_processed": file.filename,
            "file_size_mb": round(len(content) / (1024 * 1024), 2)
        }
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Unexpected error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup file {file_path}: {str(cleanup_error)}")

## Enhanced server startup with better configuration
## Old code had basic uvicorn configuration without proper error handling
if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Financial Document Analyzer API...")
    logger.info("API will be available at: http://localhost:8000")
    logger.info("API documentation available at: http://localhost:8000/docs")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info" 
            #reload=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise