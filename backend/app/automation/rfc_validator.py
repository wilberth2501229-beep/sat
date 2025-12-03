"""
RFC Validation Utilities
"""
import re
from datetime import datetime


def validate_rfc_format(rfc: str) -> bool:
    """
    Validate RFC format (Mexican tax ID)
    Personas Físicas: 13 caracteres (XEXX010101000)
    Personas Morales: 12 caracteres (XXX010101000)
    """
    rfc = rfc.upper().strip()
    
    # Check length
    if len(rfc) not in [12, 13]:
        return False
    
    # Personas Morales (12 chars)
    if len(rfc) == 12:
        pattern = r'^[A-ZÑ&]{3}\d{6}[A-Z0-9]{3}$'
    # Personas Físicas (13 chars)
    else:
        pattern = r'^[A-ZÑ&]{4}\d{6}[A-Z0-9]{3}$'
    
    return bool(re.match(pattern, rfc))


def validate_curp_format(curp: str) -> bool:
    """
    Validate CURP format (Mexican national ID)
    Format: 18 caracteres
    """
    curp = curp.upper().strip()
    
    if len(curp) != 18:
        return False
    
    pattern = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$'
    return bool(re.match(pattern, curp))


def extract_info_from_rfc(rfc: str) -> dict:
    """Extract information from RFC"""
    rfc = rfc.upper().strip()
    
    if not validate_rfc_format(rfc):
        return {"valid": False}
    
    # Extract date
    if len(rfc) == 13:
        # Persona Física
        date_str = rfc[4:10]  # YYMMDD
        person_type = "física"
    else:
        # Persona Moral
        date_str = rfc[3:9]  # YYMMDD
        person_type = "moral"
    
    # Parse date
    try:
        year = int(date_str[0:2])
        # Assume 1900s if year > current year's last 2 digits, else 2000s
        current_year_short = datetime.now().year % 100
        if year > current_year_short:
            year += 1900
        else:
            year += 2000
        
        month = int(date_str[2:4])
        day = int(date_str[4:6])
        
        registration_date = datetime(year, month, day)
    except:
        registration_date = None
    
    return {
        "valid": True,
        "person_type": person_type,
        "registration_date": registration_date,
        "rfc": rfc
    }


def extract_info_from_curp(curp: str) -> dict:
    """Extract information from CURP"""
    curp = curp.upper().strip()
    
    if not validate_curp_format(curp):
        return {"valid": False}
    
    # Extract data
    date_str = curp[4:10]  # YYMMDD
    gender = "Masculino" if curp[10] == "H" else "Femenino"
    state = curp[11:13]
    
    # Parse date
    try:
        year = int(date_str[0:2])
        current_year_short = datetime.now().year % 100
        if year > current_year_short:
            year += 1900
        else:
            year += 2000
        
        month = int(date_str[2:4])
        day = int(date_str[4:6])
        
        birth_date = datetime(year, month, day)
    except:
        birth_date = None
    
    return {
        "valid": True,
        "curp": curp,
        "birth_date": birth_date,
        "gender": gender,
        "state_code": state
    }


# Estado codes for CURP
CURP_STATES = {
    "AS": "Aguascalientes",
    "BC": "Baja California",
    "BS": "Baja California Sur",
    "CC": "Campeche",
    "CL": "Coahuila",
    "CM": "Colima",
    "CS": "Chiapas",
    "CH": "Chihuahua",
    "DF": "Ciudad de México",
    "DG": "Durango",
    "GT": "Guanajuato",
    "GR": "Guerrero",
    "HG": "Hidalgo",
    "JC": "Jalisco",
    "MC": "México",
    "MN": "Michoacán",
    "MS": "Morelos",
    "NT": "Nayarit",
    "NL": "Nuevo León",
    "OC": "Oaxaca",
    "PL": "Puebla",
    "QT": "Querétaro",
    "QR": "Quintana Roo",
    "SP": "San Luis Potosí",
    "SL": "Sinaloa",
    "SR": "Sonora",
    "TC": "Tabasco",
    "TS": "Tamaulipas",
    "TL": "Tlaxcala",
    "VZ": "Veracruz",
    "YN": "Yucatán",
    "ZS": "Zacatecas",
    "NE": "Nacido en el Extranjero"
}
