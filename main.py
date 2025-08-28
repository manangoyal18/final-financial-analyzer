## Enhanced imports for async processing with Celery and database
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import uuid
import sys
import asyncio
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

# Database and task imports
from database import get_db, init_db
from models import Document, Analysis
from tasks import analyze_document
from celery_app import celery_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Financial Document Analyzer - Async Version")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    init_db()
    logger.info("Database initialized successfully")

def find_existing_analysis(db: Session, file_hash: str, query: str) -> Optional[Analysis]:
    """Check if identical analysis already exists"""
    document = db.query(Document).filter(Document.file_hash == file_hash).first()
    if document:
        analysis = db.query(Analysis).filter(
            Analysis.document_id == document.id,
            Analysis.query == query,
            Analysis.status == "completed"
        ).first()
        return analysis
    return None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_uploaded_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    db: Session = Depends(get_db)
):
    """
    Submit financial document for asynchronous analysis
    Returns immediately with analysis_id for status polling
    """
    # Input validation
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
        
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        logger.info(f"Processing uploaded file: {file.filename}")
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Read and validate file content
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
            
        if len(content) > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(status_code=400, detail="File too large (max 50MB)")
        
        # Calculate file hash for deduplication
        file_hash = Document.create_hash(content)
        
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
        query = query.strip()
        
        # Check for existing analysis
        existing_analysis = find_existing_analysis(db, file_hash, query)
        if existing_analysis:
            logger.info(f"Returning existing analysis: {existing_analysis.id}")
            return {
                "status": "completed",
                "analysis_id": existing_analysis.id,
                "task_id": existing_analysis.task_id,
                "message": "Analysis already exists",
                "cached": True
            }
        
        # Create unique file path
        file_id = str(uuid.uuid4())
        file_path = f"data/financial_document_{file_id}.pdf"
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Create or get document record
        document = db.query(Document).filter(Document.file_hash == file_hash).first()
        if not document:
            document = Document(
                filename=file.filename,
                file_path=file_path,
                file_hash=file_hash,
                file_size=len(content)
            )
            db.add(document)
            db.commit()
            db.refresh(document)
        
        # Create analysis record
        analysis = Analysis(
            document_id=document.id,
            query=query,
            status="pending"
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Submit task to Celery
        task = analyze_document.delay(analysis.id, file_path, query)
        
        # Update analysis with task_id
        analysis.task_id = task.id
        db.commit()
        
        logger.info(f"Analysis {analysis.id} submitted with task {task.id}")
        
        return {
            "status": "submitted",
            "analysis_id": analysis.id,
            "task_id": task.id,
            "message": "Analysis submitted for processing",
            "file_processed": file.filename,
            "file_size_mb": round(len(content) / (1024 * 1024), 2)
        }
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Unexpected error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error submitting analysis: {str(e)}")

@app.get("/status/{analysis_id}")
async def get_analysis_status(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get the status of an analysis job
    Returns current status and results if completed
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Get Celery task status if available
    task_status = None
    if analysis.task_id:
        try:
            celery_task = celery_app.AsyncResult(analysis.task_id)
            task_status = celery_task.status
        except Exception as e:
            logger.warning(f"Could not get Celery task status: {str(e)}")
    
    response = {
        "analysis_id": analysis.id,
        "status": analysis.status,
        "task_id": analysis.task_id,
        "task_status": task_status,
        "query": analysis.query,
        "created_at": analysis.created_at.isoformat(),
        "started_at": analysis.started_at.isoformat() if analysis.started_at else None,
        "completed_at": analysis.completed_at.isoformat() if analysis.completed_at else None,
        "duration_seconds": analysis.duration_seconds
    }
    
    if analysis.status == "completed":
        response["result"] = analysis.result
    elif analysis.status == "failed":
        response["error_message"] = analysis.error_message
    
    return response

@app.get("/analyses")
async def list_analyses(
    limit: int = 10,
    offset: int = 0,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List recent analyses with optional filtering"""
    query = db.query(Analysis)
    
    if status:
        query = query.filter(Analysis.status == status)
    
    analyses = query.order_by(Analysis.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "analyses": [
            {
                "analysis_id": a.id,
                "status": a.status,
                "query": a.query[:100] + "..." if len(a.query) > 100 else a.query,
                "created_at": a.created_at.isoformat(),
                "duration_seconds": a.duration_seconds
            }
            for a in analyses
        ],
        "total": query.count(),
        "limit": limit,
        "offset": offset
    }

@app.get("/health")
async def health_check():
    """Extended health check including Celery and database status"""
    try:
        # Check database
        db = next(get_db())
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    try:
        # Check Celery
        celery_inspect = celery_app.control.inspect()
        active_workers = celery_inspect.active()
        celery_status = "healthy" if active_workers else "no workers"
    except Exception as e:
        celery_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "celery": celery_status,
        "timestamp": datetime.utcnow().isoformat()
    }

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