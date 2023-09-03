from rest_framework import viewsets

from users.models import User
from serializers.users import UserSerialaizer


# Create your views here.

class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerialaizer
    queryset = User.objects.all()
