"""
Modelo para trackear solicitudes de descarga del SAT Web Service.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

from app.core.database import Base


class EstadoSolicitudSAT(str, Enum):
    """Estados de una solicitud de descarga según el SAT."""
    SOLICITADA = "solicitada"  # Solicitud enviada al SAT
    ACEPTADA = "aceptada"  # SAT aceptó la solicitud
    EN_PROCESO = "en_proceso"  # SAT está procesando
    TERMINADA = "terminada"  # Paquetes listos para descargar
    DESCARGADA = "descargada"  # Paquetes descargados
    ERROR = "error"  # Error en la solicitud
    RECHAZADA = "rechazada"  # SAT rechazó la solicitud
    VENCIDA = "vencida"  # Solicitud expiró


class SolicitudDescargaSAT(Base):
    """
    Registro de solicitudes de descarga al Web Service del SAT.
    
    Cada sync puede generar múltiples solicitudes (emitidos, recibidos, diferentes periodos).
    """
    __tablename__ = "solicitudes_descarga_sat"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    sync_history_id = Column(Integer, ForeignKey("sync_history.id"), nullable=True)
    
    # IDs del SAT
    id_solicitud = Column(String(50), unique=True, index=True)  # UUID de la solicitud
    
    # Parámetros de la solicitud
    tipo_descarga = Column(String(20))  # emitidos/recibidos
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    rfc_emisor = Column(String(13), nullable=True)
    rfc_receptor = Column(String(13), nullable=True)
    
    # Estado
    estado = Column(SQLEnum(EstadoSolicitudSAT), default=EstadoSolicitudSAT.SOLICITADA, index=True)
    codigo_estado_sat = Column(String(10))  # Código numérico del SAT (1-6)
    
    # Resultados
    numero_paquetes = Column(Integer, default=0)
    ids_paquetes = Column(Text)  # JSON array de IDs de paquetes
    mensaje_sat = Column(Text)  # Mensaje del SAT
    
    # Tiempos
    solicitada_at = Column(DateTime, default=datetime.utcnow)
    aceptada_at = Column(DateTime, nullable=True)
    terminada_at = Column(DateTime, nullable=True)
    descargada_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", back_populates="solicitudes_descarga_sat")
    sync_history = relationship("SyncHistory", back_populates="solicitudes_descarga")
