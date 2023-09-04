from rest_framework import viewsets

from users.models import User
from serializers.users import UserSerialaizer


# Create your views here.

class UserModelViewSet(viewsets.ModelViewSet):
    """Контроллер для работы с пользователями через API (ViewSet)"""
    serializer_class = UserSerialaizer
    queryset = User.objects.all()
