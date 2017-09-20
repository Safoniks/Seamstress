import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seamstress.settings')

app = Celery('seamstress')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear-photos-every-single-minute': {
        'task': 'product.tasks.clear_photos',
        'schedule': crontab(),  # crontab(minute=0, hour=0) daily at midnight
    },
}
