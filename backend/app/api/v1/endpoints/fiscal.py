"""
API Router - Fiscal Profile Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.fiscal_profile import FiscalProfile
from app.schemas.fiscal_profile import (
    FiscalProfileCreate,
    FiscalProfileUpdate,
    FiscalProfileResponse,
    RFCValidation,
    CURPLookup
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter(prefix="/fiscal", tags=["Fiscal Profile"])


@router.get("/profile", response_model=FiscalProfileResponse)
async def get_fiscal_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's fiscal profile"""
    
    fiscal_profile = db.query(FiscalProfile).filter(
        FiscalProfile.user_id == current_user.id
    ).first()
    
    if not fiscal_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal profile not found. Please create one first."
        )
    
    return fiscal_profile


@router.post("/profile", response_model=FiscalProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_fiscal_profile(
    profile_data: FiscalProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create fiscal profile for user"""
    
    # Check if profile already exists
    existing_profile = db.query(FiscalProfile).filter(
        FiscalProfile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fiscal profile already exists"
        )
    
    # Check if RFC already exists
    if profile_data.rfc:
        existing_rfc = db.query(FiscalProfile).filter(
            FiscalProfile.rfc == profile_data.rfc
        ).first()
        if existing_rfc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="RFC already registered"
            )
    
    # Create fiscal profile
    fiscal_profile = FiscalProfile(
        user_id=current_user.id,
        rfc=profile_data.rfc,
        curp=profile_data.curp or current_user.curp,
        legal_name=profile_data.legal_name,
        tax_regime=profile_data.tax_regime,
        fiscal_address=profile_data.fiscal_address or {}
    )
    
    db.add(fiscal_profile)
    db.commit()
    db.refresh(fiscal_profile)
    
    return fiscal_profile


@router.put("/profile", response_model=FiscalProfileResponse)
async def update_fiscal_profile(
    profile_update: FiscalProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update fiscal profile"""
    
    fiscal_profile = db.query(FiscalProfile).filter(
        FiscalProfile.user_id == current_user.id
    ).first()
    
    if not fiscal_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal profile not found"
        )
    
    # Update fields
    if profile_update.legal_name is not None:
        fiscal_profile.legal_name = profile_update.legal_name
    if profile_update.tax_regime is not None:
        fiscal_profile.tax_regime = profile_update.tax_regime
    if profile_update.fiscal_address is not None:
        fiscal_profile.fiscal_address = profile_update.fiscal_address
    if profile_update.tax_mailbox_email is not None:
        fiscal_profile.tax_mailbox_email = profile_update.tax_mailbox_email
    
    db.commit()
    db.refresh(fiscal_profile)
    
    return fiscal_profile


@router.post("/validate-rfc")
async def validate_rfc(
    rfc_data: RFCValidation,
    current_user: User = Depends(get_current_user)
):
    """Validate RFC format and check with SAT"""
    
    # TODO: Implement RFC validation logic
    # - Format validation
    # - Check digit validation
    # - SAT API validation (if available)
    
    return {
        "valid": True,
        "rfc": rfc_data.rfc,
        "message": "RFC validation not fully implemented yet"
    }


@router.post("/lookup-curp")
async def lookup_curp(
    curp_data: CURPLookup,
    current_user: User = Depends(get_current_user)
):
    """Lookup RFC by CURP"""
    
    # TODO: Implement CURP lookup
    # - Connect to RENAPO or SAT API
    # - Retrieve RFC if exists
    
    return {
        "curp": curp_data.curp,
        "rfc": None,
        "message": "CURP lookup not fully implemented yet"
    }
