from django.db import models

NULLABLE = {
    'blank': True,
    'null': True,
            }


class Course(models.Model):
    """Модель курсов"""

    name = models.CharField(max_length=255, verbose_name='название')
    preview = models.ImageField(upload_to='study_platform/course/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание')

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

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

