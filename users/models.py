from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager

NULLABLE = {'blank': True, 'null': True}
NOT_NULLABLE = {'blank': False, 'null': False}

# Create your models here.
class User(AbstractUser):
    """Хранит данные о пользователях"""
    objects = UserManager()

    username = None
    telegram = models.CharField(max_length=150, verbose_name='Телеграм', **NOT_NULLABLE, unique=True, help_text="Телеграм пользователя для верификации")


    USERNAME_FIELD = "telegram"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Выводит информацию о пользоавтеле при печати (telegram)"""
        return f"{self.telegram}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('telegram',)