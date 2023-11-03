from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse

from study_platform.models import Subscribe
from users.models import User


class TestSubscribeCreate(APITestCase):
    """ Тест на создание подписки """

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='anonym@sky.ru',
            first_name='ww',
            last_name='SkyPro',
            is_staff=False,
            is_superuser=True,
        )
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.subscribe = Subscribe.objects.create(
            user=self.user,
            status=True
        )

    def test_user_authorization(self):
        response = self.client.get('/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_subscribe(self):
        data = {
            'user': self.user.id,
            'status': True
        }
        response = self.client.post('/subscribe/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        subscribe = Subscribe.objects.first()
        self.assertEqual(subscribe.user.id, self.user.id)
        self.assertTrue(subscribe.status)
        subscribe_all = Subscribe.objects.all()
        self.assertEqual(subscribe_all.count(), 2)