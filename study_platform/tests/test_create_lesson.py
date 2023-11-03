from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from study_platform.models import Lesson
from users.models import User

class TestCreateLesson(APITestCase):
    """ Тест на создание урока """

    def setUp(self):
        self.user = User.objects.create(
            email='anonym@sky.ru',
            first_name='ww',
            last_name='SkyPro',
            is_staff=False,
            is_superuser=False,
        )
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_successful_authorization(self):
        response = self.client.get(reverse('study_platform:lesson_all'))
        self.assertEqual(response.status_code, 200)

    def test_create_lesson(self):
        data = {
            'name': 'test_name',
            'description': 'test_description',

        }

        response = self.client.post(
            reverse('study_platform:lesson_create'),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        lesson = Lesson.objects.first()
        self.assertEqual(lesson.name, 'test_name')
        self.assertEqual(lesson.description, 'test_description')