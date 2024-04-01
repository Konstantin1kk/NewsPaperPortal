import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaperProject1')

app = Celery('NewsPaperProject1')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
