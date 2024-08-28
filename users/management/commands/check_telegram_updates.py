from django.core.management.base import BaseCommand
from users.utils import check_telegram_updates


class Command(BaseCommand):
    help = 'Check Telegram updates'

    def handle(self, *args, **kwargs):
        check_telegram_updates()