"""
Database Models - Fiscal Profile
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class TaxRegime(str, enum.Enum):
    """Regímenes fiscales del SAT"""
    SUELDOS_SALARIOS = "605"  # Sueldos y Salarios
    RIF = "621"  # Régimen de Incorporación Fiscal (deprecado)
    RESICO = "626"  # Régimen Simplificado de Confianza
    ACTIVIDAD_EMPRESARIAL = "612"  # Personas Físicas con Actividades Empresariales
    ARRENDAMIENTO = "606"  # Arrendamiento
    SERVICIOS_PROFESIONALES = "612"  # Actividad Profesional
    PERSONAS_MORALES = "601"  # General de Ley Personas Morales
    SIN_OBLIGACIONES = "616"  # Sin obligaciones fiscales


class FiscalStatus(str, enum.Enum):
    """Estado fiscal del contribuyente"""
    ACTIVE = "active"  # Al corriente
    PENDING = "pending"  # Pendiente de trámites
    SUSPENDED = "suspended"  # Suspendido por el SAT
    CANCELLED = "cancelled"  # RFC cancelado
    UNKNOWN = "unknown"  # Desconocido


class FiscalProfile(Base):
    """Perfil fiscal del usuario"""
    __tablename__ = "fiscal_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Identificación Fiscal
    rfc = Column(String(13), unique=True, index=True, nullable=True)
    curp = Column(String(18), unique=True, index=True, nullable=True)
    
    # Datos del Contribuyente
    legal_name = Column(String, nullable=True)  # Nombre o razón social
    tax_regime = Column(SQLEnum(TaxRegime), nullable=True)
    fiscal_status = Column(SQLEnum(FiscalStatus), default=FiscalStatus.UNKNOWN)
    
    # Dirección Fiscal
    fiscal_address = Column(JSON, nullable=True)  # {street, number, colony, city, state, zip}
    
    # Obligaciones Fiscales
    obligations = Column(JSON, default=[])  # Lista de obligaciones activas
    
    # Estado del Buzón Tributario
    tax_mailbox_active = Column(Boolean, default=False)
    tax_mailbox_email = Column(String, nullable=True)
    
    # Certificado de Sello Digital (CSD)
    has_efirma = Column(Boolean, default=False)
    efirma_expiry = Column(DateTime(timezone=True), nullable=True)
    
    # Contraseña SAT
    has_sat_password = Column(Boolean, default=False)
    
    # Opinión del Cumplimiento
    compliance_opinion = Column(JSON, nullable=True)  # {status, date, valid_until}
    last_compliance_check = Column(DateTime(timezone=True), nullable=True)
    
    # Constancia de Situación Fiscal
    last_constancia_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="fiscal_profile")
    
    def __repr__(self):
        return f"<FiscalProfile RFC={self.rfc}>"
