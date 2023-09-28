from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from habits.models import Habit
from habits.paginators import HabitPagintor
from habits.permissions import IsOwnerHabit
from habits.serializers import HabitSerializer


# Create your views here.

class HabitViewSet(ModelViewSet):
    """Оснонвной контроллер для работы со своими привычками"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagintor

    def get_queryset(self):
        """Получение списка привычек авторизованного пользователя"""
        return Habit.objects.filter(user_id=self.request.user.pk)

    def perform_create(self, serializer):
        """Присваивание созданной привычке идентификатора пользователя"""
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

    def get_permissions(self):
        """Определение прав доступа"""
        permission_classes = []
        if self.action not in ('list', 'retrieve', 'create'):
            permission_classes = [IsOwnerHabit,]
        # print("self.action", self.action)
        # print("permission_classes", permission_classes)
        return [permission() for permission in permission_classes]


class HabitPublicListAPIView(generics.ListAPIView):
    """Контроллер для вывода публичных привычек"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagintor

    def get_queryset(self):
        """Получение списка публичных привычек"""
        # print('public habit', Habit.objects.filter(public_habit=True))
        return Habit.objects.filter(public_habit=True)







