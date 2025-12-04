"""
Servicio para manejar la e.firma (Firma Electrónica Avanzada) del SAT.

La e.firma consta de:
- Certificado (.cer): Archivo público que identifica al contribuyente
- Llave privada (.key): Archivo privado protegido con contraseña
"""
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import base64
import hashlib

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12


class EfirmaService:
    """Servicio para firmar documentos y solicitudes con e.firma del SAT."""
    
    def __init__(self, cer_path: str, key_path: str, password: str):
        """
        Inicializar servicio de e.firma.
        
        Args:
            cer_path: Ruta al archivo .cer (certificado)
            key_path: Ruta al archivo .key (llave privada)
            password: Contraseña de la llave privada
        """
        self.cer_path = Path(cer_path)
        self.key_path = Path(key_path)
        self.password = password
        
        self._certificate: Optional[x509.Certificate] = None
        self._private_key = None
        self._load_certificate_and_key()
    
    def _load_certificate_and_key(self) -> None:
        """Cargar certificado y llave privada desde archivos."""
        # Cargar certificado (.cer es formato DER)
        with open(self.cer_path, 'rb') as f:
            cert_data = f.read()
            self._certificate = x509.load_der_x509_certificate(cert_data, default_backend())
        
        # Cargar llave privada (.key es formato DER encriptado)
        with open(self.key_path, 'rb') as f:
            key_data = f.read()
            # La llave viene encriptada con la contraseña
            self._private_key = serialization.load_der_private_key(
                key_data,
                password=self.password.encode('utf-8'),
                backend=default_backend()
            )
    
    def get_certificate_serial(self) -> str:
        """Obtener número de serie del certificado."""
        return str(self._certificate.serial_number)
    
    def get_rfc(self) -> str:
        """
        Extraer RFC del certificado.
        
        El RFC viene en el Subject del certificado, generalmente en el campo
        serialNumber o en el commonName.
        """
        subject = self._certificate.subject
        
        # Buscar en serialNumber
        for attr in subject:
            if attr.oid == x509.NameOID.SERIAL_NUMBER:
                return attr.value
        
        # Si no está en serialNumber, buscar en commonName
        for attr in subject:
            if attr.oid == x509.NameOID.COMMON_NAME:
                # El RFC suele estar al inicio del CN
                cn = attr.value
                # Extraer primeros 12-13 caracteres (RFC persona moral o física)
                return cn.split()[0] if cn else ""
        
        return ""
    
    def is_valid(self) -> Tuple[bool, Optional[str]]:
        """
        Verificar si el certificado es válido.
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        now = datetime.utcnow()
        
        # Verificar fechas de validez
        if now < self._certificate.not_valid_before_utc:
            return False, "El certificado aún no es válido"
        
        if now > self._certificate.not_valid_after_utc:
            return False, "El certificado ha expirado"
        
        return True, None
    
    def get_certificate_base64(self) -> str:
        """Obtener certificado en formato Base64 (para SOAP requests)."""
        cert_bytes = self._certificate.public_bytes(serialization.Encoding.DER)
        return base64.b64encode(cert_bytes).decode('utf-8')
    
    def sign_data(self, data: bytes) -> str:
        """
        Firmar datos con la llave privada.
        
        Args:
            data: Datos a firmar (bytes)
            
        Returns:
            Firma digital en Base64
        """
        signature = self._private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')
    
    def sign_string(self, text: str) -> str:
        """
        Firmar una cadena de texto.
        
        Args:
            text: Texto a firmar
            
        Returns:
            Firma digital en Base64
        """
        return self.sign_data(text.encode('utf-8'))
    
    def create_cadena_original(self, xml_string: str) -> str:
        """
        Crear cadena original de un XML para firmarlo.
        
        En el SAT, la cadena original se forma concatenando ciertos campos
        del XML en un orden específico según el tipo de documento.
        
        Para solicitud de descarga, la cadena incluye:
        - RFC Solicitante
        - Fecha Inicial
        - Fecha Final
        - Tipo de Solicitud
        
        Args:
            xml_string: XML de la solicitud
            
        Returns:
            Cadena original para firmar
        """
        # TODO: Implementar parseo según tipo de solicitud
        # Por ahora retornamos el XML completo
        return xml_string
    
    def get_certificate_info(self) -> dict:
        """
        Obtener información del certificado.
        
        Returns:
            Diccionario con datos del certificado
        """
        subject_dict = {}
        for attr in self._certificate.subject:
            subject_dict[attr.oid._name] = attr.value
        
        return {
            'serial_number': self.get_certificate_serial(),
            'rfc': self.get_rfc(),
            'subject': subject_dict,
            'issuer': {attr.oid._name: attr.value for attr in self._certificate.issuer},
            'not_valid_before': self._certificate.not_valid_before_utc.isoformat(),
            'not_valid_after': self._certificate.not_valid_after_utc.isoformat(),
            'is_valid': self.is_valid()[0]
        }
