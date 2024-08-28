from celery import shared_task
from .utils import check_telegram_updates

@shared_task
def check_telegram_updates_task():
    check_telegram_updates()
