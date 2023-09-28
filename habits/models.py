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


class MailingLog(models.Model):
    """Журнал рассылки информации об отправки сообщений в telegram"""
    datetime_mailing = models.DateTimeField(auto_now_add=True, verbose_name='дата и время рассылки', **NOT_NULLABLE)
    habit = models.ForeignKey(to=Habit, on_delete=models.CASCADE, verbose_name='привычка', **NOT_NULLABLE, related_name='mailing_log')
    ok = models.BooleanField(default=True, verbose_name='статус', **NOT_NULLABLE, help_text="успешная или нет отправка")
    result = models.CharField(max_length=500, verbose_name='результат', **NULLABLE, help_text="информация о пересланном сообщении или ошибке")
    error_code = models.PositiveIntegerField(verbose_name='код ошибки', **NULLABLE, help_text="код ошибки. Заполняется, если возникла ошибка")

    def __str__(self):
        return f'{self.datetime_mailing} {self.habit} {self.ok}'

    class Meta:
        verbose_name = 'Запись журнала рассылки'
        verbose_name_plural = 'Журнал рассылок'
        ordering = ['-datetime_mailing',]

