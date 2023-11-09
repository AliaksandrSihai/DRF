from django.db import models

import users.models
from config import settings

NULLABLE = {
    'blank': True,
    'null': True,
            }


class Course(models.Model):
    """Модель курсов"""

    name = models.CharField(max_length=255, verbose_name='название')
    preview = models.ImageField(upload_to='study_platform/course/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    lessons = models.ManyToManyField(to='Lesson', related_name='lessons')
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                              **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='стоимость', default=0, **NULLABLE)
    last_update = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='последнее обновление')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Модель уроков"""

    name = models.CharField(max_length=255, verbose_name='название')
    preview = models.ImageField(upload_to='study_platform/lesson/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    url_video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                              **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='стоимость', default=0, **NULLABLE)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    """  Модель платежей """

    ways_to_payment = [
        ('наличные', 'наличные'),
        ('перевод на счет', 'перевод на счет'),
    ]

    user = models.ForeignKey(to=users.models.User, on_delete=models.DO_NOTHING, **NULLABLE, verbose_name='пользователь',
                             related_name='user')
    payments_date = models.DateField(auto_now_add=True, verbose_name='дата платежа')
    payed_lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок',
                                     related_name='lesson', **NULLABLE)
    payed_course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name='оплаченный курс',
                                     related_name='course', **NULLABLE)
    payments_ways = models.CharField(max_length=30, choices=ways_to_payment, verbose_name='способ оплаты')
    stripe_id = models.CharField(max_length=40, verbose_name='id платежа на stripe.com', **NULLABLE)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'


class Subscribe(models.Model):
    """ Класс подписки на курс """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    course_subscribe = models.ForeignKey(to=Course, on_delete=models.SET_NULL, **NULLABLE,
                                         verbose_name='подписка на курс', related_name='subscribe')
    status = models.BooleanField(default=False, verbose_name='статус подписки')

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
