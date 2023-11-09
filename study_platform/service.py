import json
from datetime import datetime, timedelta

from django.core.mail import send_mail
import requests
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from config import settings


def scheduled(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Check users',
        task='study_platform.tasks.send_update',
        args=['sigai.aleksandr@mail.ru'],
        expires=datetime.utcnow() + timedelta(days=1)
    )


def send_message(subject: str, message: str, recipient_list: list):
    """Функция отправки сообщения"""
    send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list
        )



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
