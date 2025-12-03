"""
Database Models - SAT Credentials
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class SATCredentials(Base):
    """Credenciales cifradas del SAT"""
    __tablename__ = "sat_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Contraseña del SAT (cifrada)
    encrypted_password = Column(String, nullable=True)
    
    # e.firma / CSD (Certificado de Sello Digital)
    has_efirma = Column(Boolean, default=False)
    efirma_cer_path = Column(String, nullable=True)  # Ruta al archivo .cer cifrado
    efirma_key_path = Column(String, nullable=True)  # Ruta al archivo .key cifrado
    encrypted_efirma_password = Column(String, nullable=True)  # Contraseña de la llave privada
    efirma_expiry = Column(DateTime(timezone=True), nullable=True)
    
    # Tokens de sesión (cache temporal)
    sat_session_token = Column(String, nullable=True)
    session_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_validated = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sat_credentials")
    
    def __repr__(self):
        return f"<SATCredentials user_id={self.user_id}>"
