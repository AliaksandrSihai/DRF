import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from study_platform.models import Lesson
from users.models import User


# Create your tests here.


class LessonCreateTestCase(APITestCase):
    """ Тестирование создания собаки"""
    def setUp(self):
        self.user = User.objects.create(
            email='anonym@sky.ru',
            first_name='ww',
            last_name='SkyPro',
            is_staff=False,
            is_superuser=False,
        )
        self.access_token = str(AccessToken.for_user(self.user))

        self.lesson = Lesson.objects.create(
            name='test_name',
            description='test_description',

        )

    def test_successful_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(reverse('study_platform:lesson_all'))
        self.assertEqual(response.status_code, 200)
    def test_create_lesson(self):
        data = {
            'name': 'test_name',
            'description': 'test_description',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.post(
            reverse('study_platform:lesson_create'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        lesson = Lesson.objects.first()
        self.assertEqual(lesson.name, 'test_name')
        self.assertEqual(lesson.description, 'test_description')

    def test_list_lesson(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(reverse('study_platform:lesson_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.count(), 1)
        lesson = Lesson.objects.first()
        self.assertEqual(lesson.name, 'test_name')
        self.assertEqual(lesson.description, 'test_description')

