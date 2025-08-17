from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Модератор").exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        else:
            return False


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        else:
            return False
