"""
Database models for financial document analyzer
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import hashlib

Base = declarative_base()

class Document(Base):
    """Document model for storing uploaded files metadata"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)  # Path where file is stored
    file_hash = Column(String(64), nullable=False, index=True)  # SHA-256 hash
    file_size = Column(Integer, nullable=False)  # File size in bytes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to analyses
    analyses = relationship("Analysis", back_populates="document")
    
    @classmethod
    def create_hash(cls, content: bytes) -> str:
        """Create SHA-256 hash from file content"""
        return hashlib.sha256(content).hexdigest()

class Analysis(Base):
    """Analysis model for storing analysis results and status"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    task_id = Column(String(255), nullable=False, index=True)  # Celery task ID
    query = Column(Text, nullable=False)  # User query
    status = Column(String(50), nullable=False, default="pending")  # pending, running, completed, failed
    result = Column(Text, nullable=True)  # JSON serialized analysis result
    error_message = Column(Text, nullable=True)  # Error details if failed
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationship to document
    document = relationship("Document", back_populates="analyses")
    
    @property
    def duration_seconds(self) -> float:
        """Calculate analysis duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0