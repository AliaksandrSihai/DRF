from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from study_platform.models import Lesson
from users.models import User


class TestListLesson(APITestCase):
    """ Тест на получение списка уроков """

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

        self.lesson_1 = Lesson.objects.create(
            name='test_name',
            description='test_description',

        )
        self.lesson_2 = Lesson.objects.create(
            name='test_name_2',
            description='test_description_2',

        )

    def test_successful_authorization(self):
        response = self.client.get(reverse('study_platform:lesson_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lesson(self):
        response = self.client.get(reverse('study_platform:lesson_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.count(), 2)
        lesson = Lesson.objects.last()
        self.assertEqual(lesson.name, 'test_name_2')
        self.assertEqual(lesson.description, 'test_description_2')