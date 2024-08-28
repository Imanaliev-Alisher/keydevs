import random
import string
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from .models import User
import requests

TELEGRAM_API_URL = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_API}/getUpdates'


def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def create_verification_code(user):
    code = generate_verification_code()
    user.verification_code = code
    user.code_expiration = timezone.now() + timedelta(minutes=10)  # Код действителен 10 минут
    user.save()
    return code


def check_telegram_updates():
    response = requests.get(TELEGRAM_API_URL)
    updates = response.json().get('result', [])

    for update in updates:
        message = update.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if chat_id and text:
            handle_verification_code(chat_id, text)


def handle_verification_code(chat_id, text):
    try:
        user = User.objects.get(verification_code=text, code_expiration__gt=timezone.now())
        if user:
            if User.objects.filter(telegram_chat_id=str(chat_id)).exists():
                print(f"Error: Chat ID {chat_id} is already taken.")
                return False

            user.telegram_chat_id = str(chat_id)
            user.verification_code = None
            user.code_expiration = None
            user.save()
            return True
    except User.DoesNotExist:
        pass
    return False
