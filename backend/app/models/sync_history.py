"""
Database Models - Sync History
Tracks SAT data synchronization operations
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class SyncStatus(str, enum.Enum):
    """Estado de la sincronización"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SyncType(str, enum.Enum):
    """Tipo de sincronización"""
    FULL = "full"  # Sincronización completa (varios meses)
    QUICK = "quick"  # Sincronización rápida (últimos días)
    MANUAL = "manual"  # Sincronización manual de archivo específico


class SyncHistory(Base):
    """Historial de sincronizaciones del SAT"""
    __tablename__ = "sync_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Sync Info
    sync_type = Column(SQLEnum(SyncType), default=SyncType.FULL)
    status = Column(SQLEnum(SyncStatus), default=SyncStatus.PENDING)
    
    # Timing
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)  # Calculated when completed
    
    # Parameters
    months_back = Column(Integer, nullable=True)  # For full sync
    days_back = Column(Integer, nullable=True)  # For quick sync
    
    # Results (stored as JSON)
    results = Column(JSON, default={})
    # Expected structure:
    # {
    #   "cfdis_downloaded": 0,
    #   "cfdis_processed": 0, 
    #   "cfdis_skipped": 0,
    #   "cfdis_emitidos": 0,
    #   "cfdis_recibidos": 0,
    #   "total_ingresos": 0.0,
    #   "total_egresos": 0.0,
    #   "errors": []
    # }
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="sync_history")
    
    def __repr__(self):
        return f"<SyncHistory {self.id} - {self.status} at {self.started_at}>"
