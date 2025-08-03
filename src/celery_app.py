from celery import Celery

from src.config import settings


celery_app = Celery(
    settings.celery_settings.celery_app_name,
    broker=settings.celery_settings.celery_broker_url,
    backend=settings.celery_settings.celery_backend_url,
)
