"""
OCR Service for document processing (INE, CURP, etc.)
"""
import pytesseract
from PIL import Image
import re
from typing import Dict, Optional


class OCRService:
    """OCR service for extracting data from documents"""
    
    @staticmethod
    def extract_text_from_image(image_path: str, lang: str = 'spa') -> str:
        """Extract text from image using Tesseract"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""
    
    @staticmethod
    def extract_ine_data(image_path: str) -> Dict[str, Optional[str]]:
        """
        Extract data from INE (Mexican ID card)
        Returns: {name, curp, address, birth_date, etc.}
        """
        text = OCRService.extract_text_from_image(image_path)
        
        data = {
            "name": None,
            "curp": None,
            "address": None,
            "birth_date": None,
            "ine_number": None
        }
        
        # Extract CURP (18 characters)
        curp_match = re.search(r'\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b', text)
        if curp_match:
            data["curp"] = curp_match.group(0)
        
        # Extract INE number
        ine_match = re.search(r'\b\d{13}\b', text)
        if ine_match:
            data["ine_number"] = ine_match.group(0)
        
        # Extract birth date (various formats)
        date_match = re.search(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', text)
        if date_match:
            data["birth_date"] = date_match.group(0)
        
        # TODO: Improve name extraction (complex due to INE format)
        
        return data
    
    @staticmethod
    def extract_rfc_from_document(image_path: str) -> Optional[str]:
        """Extract RFC from any document"""
        text = OCRService.extract_text_from_image(image_path)
        
        # RFC pattern: 12 or 13 characters
        rfc_match = re.search(r'\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b', text)
        if rfc_match:
            return rfc_match.group(0)
        
        return None
    
    @staticmethod
    def extract_curp_from_document(image_path: str) -> Optional[str]:
        """Extract CURP from any document"""
        text = OCRService.extract_text_from_image(image_path)
        
        # CURP pattern: 18 characters
        curp_match = re.search(r'\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b', text)
        if curp_match:
            return curp_match.group(0)
        
        return None
