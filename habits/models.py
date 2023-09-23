from datetime import datetime

from django.db import models

from users.models import User, NULLABLE, NOT_NULLABLE



# Create your models here.

class Habit(models.Model):
    """Модель с описанием привычек"""
    user = models.ForeignKey(to=User, related_name='habits', on_delete=models.SET_NULL, verbose_name='пользователь', help_text='Владелец привычки', **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место', help_text='Место выполнения привычки', **NULLABLE)
    # time_habit = models.TimeField(default=datetime.time(12, 00), verbose_name='время', help_text='Время повторения привычки', **NULLABLE)
    time_habit = models.TimeField(default='12:00', verbose_name='время', help_text='Время повторения привычки', **NULLABLE)
    action = models.CharField(max_length=200, verbose_name='действие', help_text='Действие привычки', **NOT_NULLABLE)
    pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки', help_text='Признак приятной привычки', **NOT_NULLABLE)
    next_habit = models.ForeignKey(to='self', related_name='prev_habit', on_delete=models.SET_NULL, verbose_name='Связанная привычка', help_text='Связанная приятная привычка', **NULLABLE)
    frequency = models.IntegerField(default=1, verbose_name='Периодичность ', help_text='Периодичность (в днях)', **NULLABLE)
    award = models.CharField(max_length=150, verbose_name='Вознаграждение ', help_text='Вознаграждение за выполнение привычки', **NULLABLE)
    duration = models.IntegerField(default=60, verbose_name='Время на выполнение ', help_text='Время на выполнение (в секундах)', **NOT_NULLABLE)
    public_habit = models.BooleanField(default=False, verbose_name='Признак публичности', help_text='Признак публичности привычки', **NOT_NULLABLE)

    def __str__(self):
        return f"Я буду {self.action} в {self.time_habit} в {self.place}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'


