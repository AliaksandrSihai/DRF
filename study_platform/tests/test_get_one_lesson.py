from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from study_platform.models import Lesson
from users.models import User


class TestGetOneLesson(APITestCase):
    """ Тест на получение одного урока"""

    def setUp(self):
        self.user = User.objects.create(
            email='anonym@sky.ru',
            first_name='ww',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
        )
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.lesson = Lesson.objects.create(
            name='test_name',
            description='test_description',

        )

    def test_successful_authorization(self):
        response = self.client.get(reverse('study_platform:lesson_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_lesson(self):
        response = self.client.get(reverse('study_platform:lesson_one', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson = Lesson.objects.first()
        self.assertEqual(lesson.name, 'test_name')
        self.assertEqual(lesson.description, 'test_description'
                         )