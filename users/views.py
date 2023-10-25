from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """ CRUD для модели пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()
