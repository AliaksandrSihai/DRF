from users.apps import UsersConfig
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='users')

app_name = UsersConfig.name

urlpatterns = [
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
