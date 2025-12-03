"""
Celery Worker Configuration
"""
from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "sat_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.workers.tasks.sat_tasks",
        "app.workers.tasks.document_tasks",
        "app.workers.tasks.notification_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Mexico_City',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Scheduled tasks (Celery Beat)
celery_app.conf.beat_schedule = {
    'check-compliance-daily': {
        'task': 'app.workers.tasks.sat_tasks.check_compliance_status',
        'schedule': 86400.0,  # Every 24 hours
    },
    'download-new-cfdi': {
        'task': 'app.workers.tasks.sat_tasks.download_new_cfdi',
        'schedule': 3600.0,  # Every hour
    },
    'check-document-expiry': {
        'task': 'app.workers.tasks.document_tasks.check_expiring_documents',
        'schedule': 86400.0,  # Every 24 hours
    },
}
