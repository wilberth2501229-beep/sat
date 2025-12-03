"""
Celery Tasks - SAT Operations
"""
from celery import Task
from app.workers.celery_app import celery_app
from app.automation.sat_automation import SATAutomation
from app.core.database import SessionLocal
from app.models.sat_credentials import SATCredentials
from app.models.fiscal_profile import FiscalProfile
from datetime import datetime, timedelta
import asyncio


class DatabaseTask(Task):
    """Base task with database session"""
    _db = None
    
    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db
    
    def after_return(self, *args, **kwargs):
        if self._db is not None:
            self._db.close()


@celery_app.task(base=DatabaseTask, bind=True)
def update_fiscal_status(self, user_id: int):
    """Update user's fiscal status from SAT"""
    try:
        # Get credentials
        credentials = self.db.query(SATCredentials).filter(
            SATCredentials.user_id == user_id
        ).first()
        
        if not credentials or not credentials.encrypted_password:
            return {"success": False, "message": "No SAT credentials found"}
        
        # Get fiscal profile
        profile = self.db.query(FiscalProfile).filter(
            FiscalProfile.user_id == user_id
        ).first()
        
        if not profile or not profile.rfc:
            return {"success": False, "message": "No RFC found"}
        
        # Decrypt password
        from app.core.security import decrypt_data
        sat_password = decrypt_data(credentials.encrypted_password)
        
        # Use automation to get status
        async def get_status():
            async with SATAutomation() as sat:
                return await sat.get_fiscal_status(profile.rfc, sat_password)
        
        result = asyncio.run(get_status())
        
        if result["success"]:
            # Update profile
            profile.fiscal_status = result["data"]["status"]
            profile.obligations = result["data"]["obligations"]
            profile.last_compliance_check = datetime.utcnow()
            self.db.commit()
        
        return result
        
    except Exception as e:
        return {"success": False, "message": str(e)}


@celery_app.task(base=DatabaseTask)
def download_constancia(user_id: int):
    """Download Constancia de Situación Fiscal"""
    # TODO: Implement constancia download
    pass


@celery_app.task(base=DatabaseTask)
def download_new_cfdi(user_id: int):
    """Download new CFDI (invoices)"""
    # TODO: Implement CFDI download
    pass


@celery_app.task(base=DatabaseTask)
def check_compliance_status():
    """Periodic task to check compliance for all users"""
    # TODO: Check compliance for users with active profiles
    pass
