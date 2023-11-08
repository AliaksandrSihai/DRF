from django.core.mail import send_mail
import requests
from config import settings


def send_message(subject: str, message: str, recipient_list: list):
    """Функция отправки сообщения"""
    send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list
        )
    return True


def create_payment(instance):
    """ Создание платежа """
    """ Создание платежа на strip.com """
    url = 'https://api.stripe.com/v1/payment_intents'
    headers = {
        'Authorization': f'Bearer {settings.STRIPE_SECRET_KEY}'
    }
    data = {
        'amount': instance,
        'currency': 'eur',
        'automatic_payment_methods[enabled]': True,
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['id']


def get_payment(instance):
    """ Получение данных от stripe.com """
    url = 'https://api.stripe.com/v1/payment_intents'
    headers = {
        'Authorization': f'Bearer {settings.STRIPE_SECRET_KEY}'
    }

    response = requests.get(f'{url}/{instance}', headers=headers)
    return response.json()
