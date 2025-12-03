"""
Database Models - Notifications and Audit
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Text, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class NotificationType(str, enum.Enum):
    """Tipos de notificaciones"""
    OBLIGATION_REMINDER = "obligation_reminder"
    DOCUMENT_EXPIRING = "document_expiring"
    CFDI_RECEIVED = "cfdi_received"
    TAX_ALERT = "tax_alert"
    SYSTEM = "system"
    SECURITY = "security"


class NotificationStatus(str, enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


class Notification(Base):
    """Notificaciones para el usuario"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Notification Info
    type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.UNREAD)
    
    # Action
    action_url = Column(String, nullable=True)
    action_label = Column(String, nullable=True)
    
    # Priority
    is_urgent = Column(Boolean, default=False)
    
    # Metadata
    extra_data = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.title}>"


class AuditAction(str, enum.Enum):
    """Acciones auditables"""
    LOGIN = "login"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    DOCUMENT_UPLOAD = "document_upload"
    DOCUMENT_DOWNLOAD = "document_download"
    DOCUMENT_DELETE = "document_delete"
    SAT_CONNECTION = "sat_connection"
    CFDI_DOWNLOAD = "cfdi_download"
    PROFILE_UPDATE = "profile_update"
    SETTINGS_CHANGE = "settings_change"


class AuditLog(Base):
    """Registro de auditoría"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Action Info
    action = Column(SQLEnum(AuditAction), nullable=False)
    description = Column(Text, nullable=True)
    
    # Context
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Result
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # Metadata
    extra_data = Column(JSON, default={})
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog {self.action} at {self.created_at}>"
