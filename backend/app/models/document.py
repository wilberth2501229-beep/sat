"""
Database Models - Documents
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Text, BigInteger, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class DocumentType(str, enum.Enum):
    """Tipos de documentos fiscales"""
    # Identificación oficial
    INE = "ine"
    PASSPORT = "passport"
    
    # Documentos fiscales
    RFC_CEDULA = "rfc_cedula"
    CONSTANCIA_SITUACION = "constancia_situacion"
    OPINION_CUMPLIMIENTO = "opinion_cumplimiento"
    
    # e.firma / CSD
    EFIRMA_CER = "efirma_cer"
    EFIRMA_KEY = "efirma_key"
    
    # CFDI
    CFDI_EMITIDO = "cfdi_emitido"
    CFDI_RECIBIDO = "cfdi_recibido"
    
    # Declaraciones
    DECLARACION_ANUAL = "declaracion_anual"
    DECLARACION_MENSUAL = "declaracion_mensual"
    DECLARACION_INFORMATIVA = "declaracion_informativa"
    
    # Comprobantes
    COMPROBANTE_DOMICILIO = "comprobante_domicilio"
    ESTADO_CUENTA = "estado_cuenta"
    
    # Otros
    CURP = "curp"
    ACTA_NACIMIENTO = "acta_nacimiento"
    PODER_NOTARIAL = "poder_notarial"
    OTHER = "other"


class DocumentStatus(str, enum.Enum):
    """Estado del documento"""
    ACTIVE = "active"
    EXPIRED = "expired"
    PENDING_VERIFICATION = "pending_verification"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class Document(Base):
    """Documentos del usuario"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Document Info
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # File Info
    file_path = Column(String, nullable=False)  # Ruta en storage
    file_name = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)  # bytes
    mime_type = Column(String, nullable=False)
    is_encrypted = Column(Boolean, default=True)
    
    # Document Status
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.ACTIVE)
    issue_date = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    doc_metadata = Column(JSON, default={})  # Info adicional específica del documento
    tags = Column(JSON, default=[])  # Tags para búsqueda
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="documents")
    
    def __repr__(self):
        return f"<Document {self.title} ({self.document_type})>"


from sqlalchemy import Boolean, JSON
