from rest_framework.permissions import BasePermission

class PermissionMixin:
    """Mixin для классов permission для проверки является ли пользователем модератором и владельцем объекта"""
    def is_owner(self, request, view):
        """Если пользователь владелей объекта, возвращет True, иначе False"""
        return request.user == view.get_object().owner

    def is_moderator(self, request, view):
        """Если пользователь в группе модераторов или владелей объекта, возвращет True, иначе False"""
        return request.user.groups.filter(name = 'moderator').exists()


class IsOwnerOrModerator(PermissionMixin, BasePermission):
    """Класс Permission для предосталения доступа владельам объекта и модераторов"""
    def has_permission(self, request, view):
        """Если пользователь владелец объекта не из группы модераторов, возвращет True, иначе False"""
        return self.is_owner(request, view) or self.is_moderator(request, view)


class IsNotModerator(PermissionMixin, BasePermission):
    """Класс Permission для запрета доступа модераторам"""
    def has_permission(self, request, view):
        """Если пользователь не из группы модераторов, возвращет True, иначе False"""
        return not self.is_moderator(request, view)


class IsOwner(PermissionMixin, BasePermission):
    """Класс Permission для предосталения доступа владельцу объекта"""

    def has_permission(self, request, view):
        """Если пользователь владелей объекта, возвращет True, иначе False"""
        return self.is_owner(request, view)


class IsOwnerAndNotModerator(BasePermission):
    """Класс Permission для предосталения доступа владельам объекта не из группы модераторов"""
    def has_permission(self, request, view):
        """Если пользователь владелец объекта не из группы модераторов, возвращет True, иначе False"""
        return not request.user.groups.filter(name = 'moderator').exists() and request.user == view.get_object().owner



class IsModerator(BasePermission):
    """Класс Permission для предосталения доступа пользователю из группы модераторов"""
    def has_permission(self, request, view):
        """Если пользователь в группе модераторов или владелей объекта, возвращет True, иначе False"""
        return request.user.groups.filter(name = 'moderator').exists()




# class IsOwnerOrModerator(BasePermission):
#     """Класс Permission для предосталения доступа владельцу объекта или пользователю из группы модераторов"""
#     def has_permission(self, request, view):
#         """Если пользователь в группе модераторов или владелей объекта, возвращет True, иначе False"""
#         if request.user.groups.filter(name = 'moderator'):
#             return True
#
#         return request.user == view.get_object().owner
