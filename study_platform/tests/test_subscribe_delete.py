from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from study_platform.models import Subscribe
from users.models import User


class TestDestroySubscribe(APITestCase):
    """ Тест на удаление подписки """

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

    def test_delete_subcribe(self):
        response = self.client.delete(f'/subscribe/{self.subscribe.id}/', )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        subscribe = Subscribe.objects.all()
        self.assertEqual(subscribe.count(), 0)