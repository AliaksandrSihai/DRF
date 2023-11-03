import re
from rest_framework.validators import ValidationError

ALLOW_URL = 'www.youtube.com'


def lesson_url_validator(value):
    if ALLOW_URL not in value.lower():
        raise ValidationError(f'Разрешено добавлять видео только с {ALLOW_URL} ')
