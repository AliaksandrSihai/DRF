from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Класс для создания админа"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@sky.ru',
            first_name='ww',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('123qwe456asd')
        user.save()