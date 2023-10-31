from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study_platform.permissions import IsModerator, IsOwner
from users.models import User
from users.serializers import UserSerializer, UserShortSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """ CRUD для модели пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user.is_staff:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            serializer = UserShortSerializer(queryset, many=True)
            return Response(serializer.data)



