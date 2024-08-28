from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keydevs.settings')

app = Celery('keydevs')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'check-telegram-updates-every-5-minutes': {
        'task': 'users.tasks.check_telegram_updates_task',
        'schedule': crontab(minute='*/5'),
    },
}

app.autodiscover_tasks()
