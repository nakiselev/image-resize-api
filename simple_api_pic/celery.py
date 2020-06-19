import os  
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_api_pic.settings')
celery_app = Celery('simple_api_pic')  
celery_app.config_from_object('django.conf:settings', namespace='CELERY')  
celery_app.autodiscover_tasks()