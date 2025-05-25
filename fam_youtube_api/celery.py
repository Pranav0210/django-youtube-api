import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fam_youtube_api.settings')

app = Celery('fam_youtube_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
