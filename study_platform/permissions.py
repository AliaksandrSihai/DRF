from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """ Разрешения для модераторов """

    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE'] and request.user.is_staff:
            return False
        else:
            return request.user.is_staff


class IsOwner(BasePermission):
    """ Разрешение для владельца """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
