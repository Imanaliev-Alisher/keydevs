import requests
from django.conf import settings

def send_telegram_message(chat_id, message):
    token = settings.TELEGRAM_BOT_API
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    print(chat_id)
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(url, data=payload)
    return response
