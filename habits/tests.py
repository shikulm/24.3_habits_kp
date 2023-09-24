from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APITestCase

from habits.models import Habit
from users.managers import UserManager
from users.models import User


class CreateHabitTestCase(APITestCase):
    """Тест создания привычки"""
    def setUp(self) -> None:
        """Подготовка данных для тестирования"""
        obj = UserManager()
        self.user = User.objects.create(telegram='test', is_staff=True, is_superuser=True)
        # print(vars(self.user))
        # self.user = obj.create_superuser(telegram='test', password='123')
        self.client.force_authenticate(self.user)
        # # Создание приятной привычки
        # self.data = {"place": "дома","action": "Есть мороженое","pleasant": True,"duration": 60}
        # self.pleasent_habit = Habit.objects.create(**self.data)
        # # Создание полезной привычки
        # self.data = {"place": "дома", "time_habit": "11:00", "action": "сделать зарядку", "pleasant": False,
        #              "next_habit": 2, "frequency": 1, "duration": 60, "public_habit": True }


    def test_create_habit(self):
        """Тестирование создания привычки с корректными параметрами"""
        data = {"place": "дома", "action": "Есть мороженое", "pleasant": True, "duration": 60}
        response = self.client.post("/habit/", data)
        new_habit = response.json()
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)

        #  Проверка корректности данных

        self.assertEquals({'place': new_habit['place'], 'action': new_habit['action'],
                           'pleasant': new_habit['pleasant'],'duration': new_habit['duration'],
                           'user': new_habit['user']},
                          {'place': 'дома',
                           'action': 'Есть мороженое',
                           'pleasant': True,
                           'duration': 60,
                           'user': self.user.pk})

    def test_next_and_award_valid(self):

        """Тестирование валидатора для исключения одновременного выбора связанной привычки и вознаграждения"""
        # Создание приятной привычки
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое","pleasant": True,"duration": 60}
        self.pleasent_habit = self.client.post("/habit/", data).json()
        # print("self.pleasent_habit = ", self.pleasent_habit)

        # Создание связанной привычки со ссылкой на приятную и указанием вознаграждения
        data = {"place": "дома", "time_habit": "11:00", "action": "тест", "pleasant": False,
                     "next_habit": self.pleasent_habit.get('id'), "award": "вознаграждение",
                    "frequency": 1, "duration": 60, "public_habit": True }
        response = self.client.post("/habit/", data)

        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        # Проверка сообщения с ошибкой
        self.assertEquals(response.json(),
                          {'non_field_errors': ['Нельзя одновременно указывать связанную привычку и вознаграждение!']})


    def test_duration_valid(self):
        """Тестирование валидатора для проверки, что время выполнения должно быть не больше 120 секунд"""
        # Создание привычки
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое", "pleasant": True, "duration": 200}
        response = self.client.post("/habit/", data)
        # print("response.json() = ", response.json())

        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        # Проверка сообщения с ошибкой
        self.assertEquals(response.json(),
                          {'non_field_errors': ['Время выполнения должно быть не больше 120 секунд!']})


    def test_next_habit_pleasant_valid(self):

        """Тестирование валидатора, что в связанными могут быть только приятной привычки"""
        # Создание приятной привычки
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое","pleasant": False, "duration": 60}
        self.pleasent_habit = self.client.post("/habit/", data).json()
        print("self.pleasent_habit = ", self.pleasent_habit)

        # Создание связанной привычки со ссылкой на приятную и указанием вознаграждения
        data = {"place": "дома", "time_habit": "11:00", "action": "тест", "pleasant": False,
                     "next_habit": self.pleasent_habit.get('id'),
                    "frequency": 1, "duration": 60, "public_habit": True }
        response = self.client.post("/habit/", data)

        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        # Проверка сообщения с ошибкой
        self.assertEquals(response.json(),
                          {'non_field_errors': ['В связанные привычки могут попадать только привычки с признаком '
                                              'приятной привычки!']})


    def test_pleas_habit_has_not_nxt_habit_valid(self):

        """Тестирование валидатора, что у приятной привычки не может быть связанной"""
        # Создание приятной привычки 1
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое","pleasant": True, "duration": 60}
        self.pleasent_habit = self.client.post("/habit/", data).json()
        # print("self.pleasent_habit = ", self.pleasent_habit)

        # Создание приятной привычки со ссылкой на другую привычку
        data = {"place": "дома", "time_habit": "11:00", "action": "тест", "pleasant": True,
                     "next_habit": self.pleasent_habit.get('id'),
                    "frequency": 1, "duration": 60, "public_habit": True }
        response = self.client.post("/habit/", data)

        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        # Проверка сообщения с ошибкой
        self.assertEquals(response.json(),
                          {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки!']})


    def test_pleas_habit_has_not_award_valid(self):

        """Тестирование валидатора, что у приятной привычки не может быть вознаграждения"""
        # Создание приятной привычки с вознаграждением
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое","pleasant": True, "award": "+++"}
        response = self.client.post("/habit/", data)
        # print("self.pleasent_habit = ", self.pleasent_habit)

        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        # Проверка сообщения с ошибкой
        self.assertEquals(response.json(),
                          {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки!']})


    def test_frequency_valid(self):

        """Тестирование валидатора, что нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
        # Создание приятной привычки с вознаграждением
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое","pleasant": True, "frequency": 10}
        response = self.client.post("/habit/", data)
        # print("self.pleasent_habit = ", self.pleasent_habit)

        # Проверяем статус создания привычки
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        # Проверка сообщения с ошибкой
        self.assertEquals(response.json(),
                          {'non_field_errors': ['Нельзя выполнять привычку реже, чем 1 раз в 7 дней!']})


class ReadHabitTestCase(APITestCase):
    """Тест просмотра списка привычек"""
    def setUp(self) -> None:
        """Подготовка данных для тестирования"""
        # obj = UserManager()
        self.user = User.objects.create(telegram='test', is_staff=True, is_superuser=True)
        # print(vars(self.user))
        # self.user = obj.create_superuser(telegram='test', password='123')
        self.client.force_authenticate(self.user)


        # Создание приятной привычки
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое","pleasant": True,"duration": 60}
        self.pleasent_habit = self.client.post("/habit/", data).json()
        print("self.pleasent_habit = ", self.pleasent_habit)
        # self.pleasent_habit = Habit.objects.create(**data)
        # self.pleasent_habit = Habit.objects.create(place="дома", action="Есть мороженое",
        #                                            pleasant = True, duration = 60)
        # self.pleasent_habit.save()
        # print(self.pleasent_habit)
        # print(self.pleasent_habit.pk)
        # Создание полезной привычки
        data = {"place": "дома", "time_habit": "11:00", "action": "сделать зарядку", "pleasant": False,
                     "next_habit": self.pleasent_habit.get('id'), "frequency": 1, "duration": 60, "public_habit": True }
        self.main_habit = self.client.post("/habit/", data).json()
        print("self.main_habit ", self.main_habit)

        # data = {"place": "дома", "time_habit": "11:00", "action": "сделать зарядку", "pleasant": False,
        #              "frequency": 1, "duration": 60, "public_habit": True }
        #
        # self.main_habit = Habit.objects.create(**data)
        # print(self.main_habit)


    def test_list_habit(self):
        """Тестировние вывода списка привычек"""
        response = self.client.get("/habit/")
        # print("response.json(): ", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        # Проверяем наличие всех добавленных привычек
        self.assertEquals(len(response.json().get('results')), 2)

    def test_retrive_habit(self):
        response = self.client.get(f"/habit/{self.pleasent_habit.get('id')}/")
        # print("response.json() = ", response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          {'id': self.pleasent_habit.get('id'),
                            'place': self.pleasent_habit.get('place'),
                            'time_habit': self.pleasent_habit.get('time_habit'),
                            'action': self.pleasent_habit.get('action'),
                            'pleasant': self.pleasent_habit.get('pleasant'),
                            'frequency': self.pleasent_habit.get('frequency'),
                            'award': self.pleasent_habit.get('award'),
                            'duration': self.pleasent_habit.get('duration'),
                            'public_habit': self.pleasent_habit.get('public_habit'),
                            'user': self.user.pk,
                            'next_habit': self.pleasent_habit.get('next_habit')})


class UpdateHabitTestCase(APITestCase):
    """Тест обновления списка привычек"""
    def setUp(self) -> None:
        """Подготовка данных для тестирования"""
        self.user = User.objects.create(telegram='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)

        # Создание приятной привычки
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое","pleasant": True,"duration": 60}
        self.pleasent_habit = self.client.post("/habit/", data).json()

    def test_update_habit(self):
        """Тестировние обновления привычек"""
        data = {"pleasant": False}
        response = self.client.patch(f"/habit/{self.pleasent_habit.get('id')}/", data=data)
        print("response.json() = ", response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json().get('pleasant'), False)

class DeleteHabitTestCase(APITestCase):
    """Тест удаления списка привычек"""
    def setUp(self) -> None:
        """Подготовка данных для тестирования"""
        self.user = User.objects.create(telegram='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)

        # Создание привычки
        data = {"place": "дома", "time_habit": "12:00", "action": "Есть мороженое","pleasant": True,"duration": 60}
        self.pleasent_habit = self.client.post("/habit/", data).json()

    def test_delete_habit(self):
        """Тестировние удаления привычки"""
        response = self.client.delete(f"/habit/{self.pleasent_habit.get('id')}/")
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_204_NO_CONTENT)
        #  Проверка корректности данных
        self.assertEquals(Habit.objects.all().count(), 0)








