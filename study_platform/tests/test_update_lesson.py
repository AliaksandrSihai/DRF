from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from study_platform.models import Lesson
from users.models import User

class TestUpdateLesson(APITestCase):
    """ Тест на проверку обновления """

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@sky.ru',
            first_name='ww',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            password='123qwe456asd'
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

    def test_part_update_lesson(self):
        data = {
            'name': 'name_test'
        }
        response = self.client.patch(reverse('study_platform:lesson_update', args=[self.user.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson = Lesson.objects.first()
        self.assertEqual(lesson.name, 'name_test')
        self.assertEqual(lesson.description, 'test_description')

    def test_full_update_lesson(self):

        data = {
                'name': 'name_test',
                'preview': '',
                'description': 'description_test',
                'url_video': '',
                'owner': ''
            }
        response = self.client.put(reverse('study_platform:lesson_update', args=[self.user.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson = Lesson.objects.first()
        self.assertEqual(lesson.name, 'name_test')
        self.assertEqual(lesson.description, 'description_test')
