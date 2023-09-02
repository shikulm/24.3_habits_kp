from django.shortcuts import render
from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerialaizer


# Create your views here.

class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerialaizer
    queryset = User.objects.all()
