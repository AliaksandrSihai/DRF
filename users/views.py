from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, UserShortSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """ CRUD для модели пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user:
            return super().update(request, *args, **kwargs)
        return PermissionDenied()

    def retrieve(self, request, *args, **kwargs):
        instance = super().retrieve(request, *args, **kwargs)
        if request.user:
            serializer = UserShortSerializer(instance)
            return Response(serializer.data)
        return PermissionDenied()

    def list(self, request, *args, **kwargs):
        instance = super().list(request, *args, **kwargs)
        if request.user:
            serializer = UserShortSerializer(instance, many=True)
            return Response(serializer.data)
        return PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        if request.user:
            return super().destroy(request, *args, **kwargs)
        return PermissionDenied()

