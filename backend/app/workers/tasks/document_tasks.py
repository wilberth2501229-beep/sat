"""
Celery Tasks - Document Processing
"""
from celery import Task
from app.workers.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.document import Document, DocumentStatus
from app.models.notification import Notification, NotificationType
from datetime import datetime, timedelta


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
def process_uploaded_document(self, document_id: int):
    """Process newly uploaded document (OCR, validation, etc.)"""
    try:
        document = self.db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            return {"success": False, "message": "Document not found"}
        
        # TODO: Run OCR if needed
        # TODO: Extract metadata
        # TODO: Validate document
        
        document.status = DocumentStatus.ACTIVE
        document.is_verified = True
        self.db.commit()
        
        return {"success": True, "message": "Document processed"}
        
    except Exception as e:
        return {"success": False, "message": str(e)}


@celery_app.task(base=DatabaseTask, bind=True)
def check_expiring_documents(self):
    """Check for documents expiring soon and send notifications"""
    try:
        # Find documents expiring in next 30 days
        thirty_days = datetime.utcnow() + timedelta(days=30)
        
        expiring_docs = self.db.query(Document).filter(
            Document.expiry_date.isnot(None),
            Document.expiry_date <= thirty_days,
            Document.expiry_date >= datetime.utcnow(),
            Document.status == DocumentStatus.ACTIVE
        ).all()
        
        # Create notifications
        for doc in expiring_docs:
            days_until_expiry = (doc.expiry_date - datetime.utcnow()).days
            
            notification = Notification(
                user_id=doc.user_id,
                type=NotificationType.DOCUMENT_EXPIRING,
                title=f"Documento por vencer: {doc.title}",
                message=f"Tu documento '{doc.title}' vence en {days_until_expiry} días.",
                is_urgent=days_until_expiry <= 7,
                metadata={"document_id": doc.id}
            )
            self.db.add(notification)
        
        self.db.commit()
        
        return {"success": True, "checked": len(expiring_docs)}
        
    except Exception as e:
        return {"success": False, "message": str(e)}


@celery_app.task(base=DatabaseTask, bind=True)
def encrypt_document(self, document_id: int):
    """Encrypt document file"""
    # TODO: Implement document encryption
    pass
