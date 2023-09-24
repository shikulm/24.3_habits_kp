from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPagintor
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




