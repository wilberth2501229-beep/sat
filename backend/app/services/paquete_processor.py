"""
Servicio para procesar paquetes de CFDIs descargados del SAT.

Los paquetes vienen en formato ZIP y contienen archivos XML de CFDIs.
"""
import zipfile
import io
from typing import List, Dict, Any
from pathlib import Path
import logging

from lxml import etree

logger = logging.getLogger(__name__)


class PaqueteProcessor:
    """Procesador de paquetes ZIP de CFDIs del SAT."""
    
    # Namespaces comunes en CFDIs
    CFDI_NAMESPACES = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'cfdi3': 'http://www.sat.gob.mx/cfd/3',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    
    @staticmethod
    def extract_xmls_from_zip(zip_bytes: bytes) -> List[bytes]:
        """
        Extraer todos los XMLs de un archivo ZIP.
        
        Args:
            zip_bytes: Contenido del archivo ZIP en bytes
            
        Returns:
            Lista de contenidos XML en bytes
        """
        xmls = []
        
        try:
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zip_file:
                # Iterar sobre archivos en el ZIP
                for file_name in zip_file.namelist():
                    if file_name.lower().endswith('.xml'):
                        xml_content = zip_file.read(file_name)
                        xmls.append(xml_content)
                        logger.debug(f"Extraído: {file_name}")
            
            logger.info(f"Extraídos {len(xmls)} XMLs del paquete")
            return xmls
            
        except zipfile.BadZipFile as e:
            logger.error(f"Error al procesar ZIP: {e}")
            raise ValueError("Archivo ZIP inválido")
    
    @staticmethod
    def parse_cfdi_xml(xml_bytes: bytes) -> Dict[str, Any]:
        """
        Parsear un XML de CFDI y extraer información clave.
        
        Args:
            xml_bytes: Contenido del XML en bytes
            
        Returns:
            Diccionario con datos del CFDI
        """
        try:
            # Parsear XML
            root = etree.fromstring(xml_bytes)
            
            # Detectar versión del CFDI (3.3 o 4.0)
            version = root.get('Version')
            
            # Determinar namespace
            ns = PaqueteProcessor.CFDI_NAMESPACES.get('cfdi' if version == '4.0' else 'cfdi3')
            
            # Extraer datos básicos del comprobante
            comprobante_data = {
                'version': version,
                'serie': root.get('Serie', ''),
                'folio': root.get('Folio', ''),
                'fecha': root.get('Fecha'),
                'tipo_comprobante': root.get('TipoDeComprobante'),
                'forma_pago': root.get('FormaPago', ''),
                'metodo_pago': root.get('MetodoPago', ''),
                'moneda': root.get('Moneda', 'MXN'),
                'tipo_cambio': root.get('TipoCambio', '1'),
                'subtotal': float(root.get('SubTotal', 0)),
                'descuento': float(root.get('Descuento', 0)),
                'total': float(root.get('Total', 0)),
                'lugar_expedicion': root.get('LugarExpedicion', '')
            }
            
            # Extraer Emisor
            emisor = root.find(f'.//{{{ns}}}Emisor')
            if emisor is not None:
                comprobante_data['emisor'] = {
                    'rfc': emisor.get('Rfc'),
                    'nombre': emisor.get('Nombre', ''),
                    'regimen_fiscal': emisor.get('RegimenFiscal', '')
                }
            
            # Extraer Receptor
            receptor = root.find(f'.//{{{ns}}}Receptor')
            if receptor is not None:
                comprobante_data['receptor'] = {
                    'rfc': receptor.get('Rfc'),
                    'nombre': receptor.get('Nombre', ''),
                    'uso_cfdi': receptor.get('UsoCFDI', ''),
                    'domicilio_fiscal': receptor.get('DomicilioFiscalReceptor', ''),
                    'regimen_fiscal': receptor.get('RegimenFiscalReceptor', '')
                }
            
            # Extraer UUID del Timbre Fiscal Digital
            tfd_ns = PaqueteProcessor.CFDI_NAMESPACES['tfd']
            timbre = root.find(f'.//{{{tfd_ns}}}TimbreFiscalDigital')
            if timbre is not None:
                comprobante_data['uuid'] = timbre.get('UUID')
                comprobante_data['fecha_timbrado'] = timbre.get('FechaTimbrado')
                comprobante_data['rfc_proveedor_cert'] = timbre.get('RfcProvCertif', '')
                comprobante_data['sello_sat'] = timbre.get('SelloSAT', '')
                comprobante_data['no_certificado_sat'] = timbre.get('NoCertificadoSAT', '')
            
            # Extraer Conceptos
            conceptos = []
            for concepto in root.findall(f'.//{{{ns}}}Concepto'):
                conceptos.append({
                    'clave_prod_serv': concepto.get('ClaveProdServ', ''),
                    'no_identificacion': concepto.get('NoIdentificacion', ''),
                    'cantidad': float(concepto.get('Cantidad', 0)),
                    'clave_unidad': concepto.get('ClaveUnidad', ''),
                    'unidad': concepto.get('Unidad', ''),
                    'descripcion': concepto.get('Descripcion', ''),
                    'valor_unitario': float(concepto.get('ValorUnitario', 0)),
                    'importe': float(concepto.get('Importe', 0)),
                    'descuento': float(concepto.get('Descuento', 0))
                })
            
            comprobante_data['conceptos'] = conceptos
            
            # Extraer Impuestos
            impuestos_data = {
                'total_traslados': 0.0,
                'total_retenciones': 0.0,
                'traslados': [],
                'retenciones': []
            }
            
            impuestos = root.find(f'.//{{{ns}}}Impuestos')
            if impuestos is not None:
                impuestos_data['total_traslados'] = float(impuestos.get('TotalImpuestosTrasladados', 0))
                impuestos_data['total_retenciones'] = float(impuestos.get('TotalImpuestosRetenidos', 0))
                
                # Traslados (IVA, IEPS, etc.)
                for traslado in impuestos.findall(f'.//{{{ns}}}Traslado'):
                    impuestos_data['traslados'].append({
                        'impuesto': traslado.get('Impuesto', ''),
                        'tipo_factor': traslado.get('TipoFactor', ''),
                        'tasa_o_cuota': float(traslado.get('TasaOCuota', 0)),
                        'importe': float(traslado.get('Importe', 0))
                    })
                
                # Retenciones (ISR, IVA, etc.)
                for retencion in impuestos.findall(f'.//{{{ns}}}Retencion'):
                    impuestos_data['retenciones'].append({
                        'impuesto': retencion.get('Impuesto', ''),
                        'importe': float(retencion.get('Importe', 0))
                    })
            
            comprobante_data['impuestos'] = impuestos_data
            
            # Guardar XML completo (para almacenar en DB)
            comprobante_data['xml_content'] = xml_bytes.decode('utf-8', errors='ignore')
            
            return comprobante_data
            
        except Exception as e:
            logger.error(f"Error al parsear CFDI XML: {e}")
            # Retornar estructura mínima con error
            return {
                'error': str(e),
                'xml_content': xml_bytes.decode('utf-8', errors='ignore')
            }
    
    @staticmethod
    def process_paquete(zip_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Procesar un paquete completo: extraer y parsear todos los CFDIs.
        
        Args:
            zip_bytes: Contenido del archivo ZIP
            
        Returns:
            Lista de diccionarios con datos de CFDIs
        """
        # Extraer XMLs
        xmls = PaqueteProcessor.extract_xmls_from_zip(zip_bytes)
        
        # Parsear cada XML
        cfdis = []
        for xml_bytes in xmls:
            cfdi_data = PaqueteProcessor.parse_cfdi_xml(xml_bytes)
            cfdis.append(cfdi_data)
        
        logger.info(f"Procesados {len(cfdis)} CFDIs del paquete")
        return cfdis
    
    @staticmethod
    def save_zip_to_disk(zip_bytes: bytes, output_path: Path) -> Path:
        """
        Guardar paquete ZIP en disco.
        
        Args:
            zip_bytes: Contenido del ZIP
            output_path: Ruta donde guardar
            
        Returns:
            Path del archivo guardado
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(zip_bytes)
        
        logger.info(f"Paquete guardado en {output_path}")
        return output_path
