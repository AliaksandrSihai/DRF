from django.core.mail import send_mail

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
