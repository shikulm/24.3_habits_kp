from rest_framework.permissions import BasePermission


class IsOwnerHabit(BasePermission):
    """Класс Permission для предосталения доступа владельам к своим привычкам"""
    def has_permission(self, request, view):
        """Пользователь может изменять только свои привычки"""
        return request.user == view.get_object().user

