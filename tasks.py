"""
Background tasks for financial document analysis
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any
from celery import current_task
from celery_app import celery_app
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Analysis, Document

# Import analysis components
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, verification, investment_analysis, risk_assessment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_crew_analysis(query: str, file_path: str) -> Dict[str, Any]:
    """
    Run the complete financial analysis crew with all agents
    This is a stateless function that creates fresh agents and crew for each task
    """
    try:
        logger.info(f"Creating new crew for analysis - Query: {query[:100]}...")
        
        # Create fresh crew instance to avoid state contamination
        financial_crew = Crew(
            agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
            tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
            process=Process.sequential,
            verbose=True
        )
        
        # Prepare inputs
        crew_inputs = {
            'query': query,
            'file_path': file_path
        }
        
        logger.info(f"Starting CrewAI analysis for file: {file_path}")
        result = financial_crew.kickoff(crew_inputs)
        
        logger.info("CrewAI analysis completed successfully")
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

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def analyze_document(self, analysis_id: int, document_path: str, query: str):
    """
    Background task to analyze financial documents
    
    Args:
        analysis_id: ID of the analysis record in database
        document_path: Path to the uploaded document
        query: User query for analysis
    """
    db: Session = SessionLocal()
    task_id = current_task.request.id
    
    try:
        # Get analysis record
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            logger.error(f"Analysis {analysis_id} not found in database")
            raise ValueError(f"Analysis {analysis_id} not found")
        
        # Update status to running
        analysis.status = "running"
        analysis.started_at = datetime.utcnow()
        analysis.task_id = task_id
        db.commit()
        
        logger.info(f"Task {task_id}: Starting analysis {analysis_id}")
        
        # Check if file exists
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document not found at path: {document_path}")
        
        # Run the analysis
        result = run_crew_analysis(query=query, file_path=document_path)
        
        if result.get("status") == "error":
            # Analysis failed
            analysis.status = "failed"
            analysis.error_message = result.get("error_message", "Unknown analysis error")
            analysis.completed_at = datetime.utcnow()
            db.commit()
            logger.error(f"Task {task_id}: Analysis failed: {analysis.error_message}")
            raise Exception(analysis.error_message)
        else:
            # Analysis succeeded
            analysis.status = "completed"
            analysis.result = str(result.get("analysis_result", ""))
            analysis.completed_at = datetime.utcnow()
            db.commit()
            logger.info(f"Task {task_id}: Analysis completed successfully")
            
            return {
                "analysis_id": analysis_id,
                "status": "completed",
                "result": result
            }
    
    except Exception as e:
        # Update analysis status to failed
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if analysis:
            analysis.status = "failed"
            analysis.error_message = str(e)
            analysis.completed_at = datetime.utcnow()
            db.commit()
        
        logger.error(f"Task {task_id}: Analysis {analysis_id} failed with error: {str(e)}")
        raise e
    
    finally:
        db.close()
        
        # Clean up document file after analysis
        try:
            if os.path.exists(document_path):
                os.remove(document_path)
                logger.info(f"Cleaned up document file: {document_path}")
        except Exception as cleanup_error:
            logger.warning(f"Failed to cleanup file {document_path}: {str(cleanup_error)}")

# Health check task
@celery_app.task
def health_check():
    """Simple health check task for monitoring"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}