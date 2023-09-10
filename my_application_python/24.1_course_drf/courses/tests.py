from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APITestCase

from courses.models import Course, Lesson
from users.managers import UserManager
from users.models import User


# Create your tests here.

class LessonTestCase(APITestCase):
    """Тестирование CRUD уроков"""
    def setUp(self) -> None:
        """Подготовка данных для тестирования"""
        obj = UserManager()
        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        # print(vars(self.user))
        # self.user = obj.create_superuser(email='test@mail.ru', password='123')
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(title='test', owner=self.user)
        self.lesson = Lesson.objects.create(title='test', course= self.course, owner=self.user)


    def test_list_lesson(self):
        """Тестировние вывода списка уроков"""
        response = self.client.get(reverse('courses:lesson-list'))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          {'count': 1, 'next': None, 'previous': None,
                           'results': [
                               {'id': self.lesson.pk,
                                'title': self.lesson.title,
                                'description': None,
                                'preview': None,
                                'video_url': None,
                                'course': self.course.pk,
                                'owner': self.user.pk}
                           ]})

    def test_retrive_lesson(self):
        """Тестировние вывода данных по отдельному уроку"""
        response = self.client.get(reverse('courses:lesson-one', args=[self.lesson.pk]))
        print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          {'id': self.lesson.pk,
                           'title': self.lesson.title,
                           'description': None,
                           'preview': None,
                           'video_url': None,
                           'course': self.course.pk,
                           'owner': self.user.pk})


    def test_create_lesson(self):
        """Тестировние создания урока"""
        data = {"title": 'test2', "course": self.course.pk}
        response = self.client.post(reverse('courses:lesson-create'), data)
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        #  Проверка корректности данных
        # print(Lesson.objects.all())
        # print(Lesson.objects.all().count())
        self.assertEquals(Lesson.objects.all().count(), 2)

        # Проверка подставновки по умолчанию текущего пользователя
        self.assertEquals(response.json().get("owner"), self.user.pk)

    def test_update_lesson(self):
        """Тестировние обновления урока"""
        data = {"title": 'test3'}
        response = self.client.patch(reverse('courses:lesson-update', args=[self.lesson.pk]), data)
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        # print(Lesson.objects.all())
        # print(Lesson.objects.all().count())
        # self.assertEquals(Lesson.objects.all().count(), 2)

        # Проверка подставновки по умолчанию текущего пользователя
        self.assertEquals(response.json().get("title"), "test3")


    def test_delete_lesson(self):
        """Тестировние удаления урока"""
        # data = {"title": 'test3'}
        # response = self.client.patch(reverse('courses:lesson-update', args=[self.lesson.pk]), data)
        response = self.client.delete(reverse('courses:lesson-delete', args=[self.lesson.pk]))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_204_NO_CONTENT)
        #  Проверка корректности данных
        # print(Lesson.objects.all())
        # print(Lesson.objects.all().count())
        self.assertEquals(Lesson.objects.all().count(), 0)


class CorseTestCase(APITestCase):
    """Тестирование CRUD курсов"""
    def setUp(self) -> None:
        """Подготовка данных для тестирования"""
        # obj = UserManager()
        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(title='test', owner=self.user)
        # self.course = Course.objects.create(title='test')


    def test_list_course(self):
        """Тестировние вывода списка курсов"""
        response = self.client.get("/courses/")
        print("response.json() = ", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          {'count': 1, 'next': None, 'previous': None,
                           'results': [
                              {'id': self.course.pk,
                               'title': self.course.title,
                               'preview': None,
                               'description': None,
                               'is_subscripe': False,
                               'lessons_count': 0,
                               'lessons': []}
                          ]})

    def test_retrive_course(self):
        """Тестировние вывода данных по отдельному курсу"""
        # response = self.client.get('/courses/1/')
        response = self.client.get(f'/courses/{self.course.pk}/')
        # print(response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          {'id': self.course.pk,
                            'title': self.course.title,
                            'preview': None,
                            'description': None,
                            'is_subscripe': False,
                            'lessons_count': 0,
                            'lessons': []})


    def test_create_course(self):
        """Тестировние создания курса"""
        data = {"title": 'test2'}
        response = self.client.post("/courses/", data)
        # print("response.json() = ", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        #  Проверка корректности данных
        # courses = Course.objects.all()[1].owner
        courses = Course.objects.all()
        # print("Course.objects.all() = ", Course.objects.all()[1].owner)
        # print("Course.objects.all().count() = ", Course.objects.all().count())
        self.assertEquals(courses.count(), 2)

        # Проверка подставновки по умолчанию текущего пользователя
        self.assertEquals(courses[1].owner, self.user)

    def test_update_course(self):
        """Тестировние обновления курса"""
        data = {"title": 'test3'}
        response = self.client.patch(f'/courses/{self.course.pk}/', data)
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        # print(Lesson.objects.all())
        # print(Lesson.objects.all().count())
        # self.assertEquals(Lesson.objects.all().count(), 2)

        # Проверка подставновки по умолчанию текущего пользователя
        self.assertEquals(response.json().get("title"), "test3")


    def test_delete_course(self):
        """Тестировние удаления курса"""
        response = self.client.delete(f'/courses/{self.course.pk}/')
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_204_NO_CONTENT)
        #  Проверка корректности данных
        # print(Lesson.objects.all())
        # print(Lesson.objects.all().count())
        self.assertEquals(Course.objects.all().count(), 0)
