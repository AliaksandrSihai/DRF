import datetime

from celery import shared_task

from study_platform.service import send_message
from users.models import User


@shared_task
def send_update(email):
    """ Отправка сообщения об обновлении"""
    send_message(subject="Обновление курса",
                 message="Курс был обновлен",
                 recipient_list=[email]
                 )


@shared_task
def check_user():
    """ Проверка пользователя """
    users = User.objects.all()
    now = datetime.date.today()
    for user in users:
        if now - user.last_login > 30:
            user.is_active = False
            user.save()
