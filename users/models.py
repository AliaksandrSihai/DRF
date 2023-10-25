from django.contrib.auth.models import AbstractUser
from django.db import models

from study_platform.models import NULLABLE


class User(AbstractUser):
    """Модель для пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=135, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватарка', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
