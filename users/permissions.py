from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'You are not a member of group "moders".'

    """ Проверяет, является ли пользователь модератором. """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):

    """ Проверяет, является ли пользователь владельцев объекта """

    def has_object_permission(self, request, view, obj):
        # мы проверяем, если владелец объекта равен request юзер, тогда возвращаем True
        if obj.owner == request.user:
            return True
        return False
