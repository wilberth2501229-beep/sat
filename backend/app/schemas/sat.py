"""
Pydantic Schemas - SAT Integration
"""
from typing import Optional, Dict, List
from datetime import datetime, date
from pydantic import BaseModel, Field


# SAT Credentials
class SATCredentialsCreate(BaseModel):
    sat_password: str = Field(..., description="Contraseña del SAT")
    rfc: Optional[str] = Field(None, min_length=12, max_length=13)


class SATCredentialsUpdate(BaseModel):
    sat_password: Optional[str] = None


# e.firma Upload
class EfirmaUpload(BaseModel):
    efirma_password: str = Field(..., description="Contraseña de la llave privada (.key)")


# SAT Connection Test
class SATConnectionTest(BaseModel):
    success: bool
    message: str
    last_connection: Optional[datetime]


# CFDI (Factura Electrónica)
class CFDIFilter(BaseModel):
    start_date: date
    end_date: date
    type: str = Field(..., description="emitido o recibido")
    rfc_emisor: Optional[str] = None
    rfc_receptor: Optional[str] = None
    status: Optional[str] = None  # vigente, cancelado


class CFDIResponse(BaseModel):
    uuid: str
    tipo: str  # ingreso, egreso, traslado, nomina, pago
    fecha: datetime
    rfc_emisor: str
    nombre_emisor: str
    rfc_receptor: str
    nombre_receptor: str
    subtotal: float
    total: float
    moneda: str
    status: str
    xml_url: Optional[str]
    pdf_url: Optional[str]


# Declaraciones
class DeclaracionResponse(BaseModel):
    tipo: str  # anual, mensual, informativa
    periodo: str  # 2023, 2023-01
    fecha_presentacion: Optional[datetime]
    status: str  # presentada, pendiente, extemporanea
    folio: Optional[str]
    impuesto_pagar: Optional[float]
    impuesto_favor: Optional[float]


# Obligaciones Fiscales
class ObligacionResponse(BaseModel):
    clave: str
    descripcion: str
    periodicidad: str  # mensual, bimestral, anual
    fecha_inicio: Optional[date]
    status: str  # activa, suspendida
    proxima_declaracion: Optional[date]
