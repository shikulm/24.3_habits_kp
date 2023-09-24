from rest_framework import serializers

from habits.models import Habit


class NextHabitAndAwardValidator:

    """Валидация для исключения одновременного выбора связанной привычки и указания вознаграждения."""
    def __call__(self, value):
        next_habit = bool(dict(value).get('next_habit'))
        award = bool(dict(value).get('award'))
        if next_habit and award:
            raise serializers.ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение!')


class DurationValidator:

    """Валидация, что время выполнения должно быть не больше 120 секунд"""
    def __call__(self, value):
        duration = dict(value).get('duration')
        if isinstance(duration, int) and duration>120:
            raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд!')


class NextHabitIsPleasantValidator:

    """Валидация, что в связанные привычки могут попадать только привычки с признаком приятной привычки."""
    def __call__(self, value):
        next_habit = dict(value).get('next_habit')
        # print('next_habit_id = ', next_habit)

        if next_habit and not next_habit.pleasant:
            raise serializers.ValidationError('В связанные привычки могут попадать только привычки с признаком '
                                              'приятной привычки!')

class PleasantHabitValidator:

    """Валидация, что у приятной привычки не может быть вознаграждения или связанной привычки."""
    def __call__(self, value):
        pleasant = dict(value).get('pleasant')
        next_habit = bool(dict(value).get('next_habit'))
        award = bool(dict(value).get('award'))
        if pleasant and (next_habit or award):
            raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки!')


class FrequencyHabitValidator:

    """Валидация, что нельзя выполнять привычку реже, чем 1 раз в 7 дней."""
    def __call__(self, value):
        frequency = dict(value).get('frequency')
        if isinstance(frequency, int) and frequency>7:
            raise serializers.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней!')
