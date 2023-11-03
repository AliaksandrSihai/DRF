from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse
from study_platform.models import Lesson
from users.models import User


class TestDeleteLesson(APITestCase):
    """ Тест на удаление урока """

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='anonym@sky.ru',
            first_name='ww',
            last_name='SkyPro',
            is_staff=False,
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
        self.assertEqual(response.status_code, 200)

    def test_delete_lesson(self):
        response = self.client.delete(reverse('study_platform:lesson_delete', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        lesson = Lesson.objects.all()
        self.assertEqual(lesson.count(), 0)
