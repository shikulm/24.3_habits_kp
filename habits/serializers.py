from rest_framework import serializers

from habits.models import Habit
from habits.validators import NextHabitAndAwardValidator, DurationValidator, NextHabitIsPleasantValidator, \
    PleasantHabitValidator, FrequencyHabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода привычек"""
    class Meta:
        model = Habit
        fields = '__all__'

        validators = [NextHabitAndAwardValidator(), DurationValidator(), NextHabitIsPleasantValidator(),
                      PleasantHabitValidator(), FrequencyHabitValidator()]