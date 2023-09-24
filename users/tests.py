from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

class RegUserTestCase(APITestCase):
    """Тестирование регистрации пользователя"""

    def setUp(self) -> None:
        pass
    def test_registr(self):
        """Проверка регистрации пользователя"""
        data = {"telegram": "user", "password": "12345", "password2": "12345"}
        response = self.client.post(reverse('users:user-create'), data)
        print(response.json())

        # Прверяем статус
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Проверяем результат
        self.assertEquals(response.json(), {'telegram': 'user'})

    def test_registr_mismatch_pass(self):
        """Проверка на несовпадение паролей"""
        data = {"telegram": "user", "password": "12345", "password2": "123456"}
        response = self.client.post(reverse('users:user-create'), data)
        # print(response.json())

        # Прверяем статус
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверяем результат
        self.assertEquals(response.json(), {'non_field_errors': ['Пароли не совпадают']})

class AuthUserTestCase(TestCase):
    """Проверка получение токена"""

    def test_get_token(self):
        # Создание пользователя
        data = {"telegram": "user", "password": "12345", "password2": "12345"}
        response_user = self.client.post(reverse('users:user-create'), data)

        # Проверка авторизации
        data = {"telegram": "user", "password": "12345"}
        response_token = self.client.post(reverse('users:token_obtain_pair'), data)
        print(response_token.json())
        # Прверяем статус
        self.assertEquals(response_token.status_code, status.HTTP_200_OK)






