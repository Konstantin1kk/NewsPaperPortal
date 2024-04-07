import os
import datetime
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaperProject1.settings')

app = Celery('NewsPaperProject1')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'posts_for_the_week_every_monday': {
        'task': 'news.tasks.show_new_post',
        'schedule': crontab(minute='0', hour='8', day_of_week='monday'),
        'args': ()
    }
}
