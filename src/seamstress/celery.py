import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seamstress.settings.main')

celery = Celery('seamstress')
celery.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
celery.autodiscover_tasks(settings.INSTALLED_APPS)

celery.conf.beat_schedule = {
    'clear-photos-every-midnight': {
        'task': 'product.tasks.clear_photos',
        'schedule': crontab(minute=0, hour=0),
    },
    'reset-daily-timing-every-midnight': {
        'task': 'public.tasks.reset_daily_timing',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}
