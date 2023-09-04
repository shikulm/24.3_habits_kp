from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from courses.models import Course, Lesson, Payment
from serializers.courses import CourseSerialaizer, LessonSerialaizer, PaymentSerialaizer


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер для работы с курсом через API (ViewSet)"""
    queryset = Course.objects.all()
    serializer_class = CourseSerialaizer


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока через API (generic).
    Вызывается через POST-запрос
    http://127.0.0.1:8000/lessons/create/"""
    serializer_class = LessonSerialaizer


class LessonListAPIView(generics.ListAPIView):
    """Контроллер для получения списка уроков через API (generic). Вызывается через GET-запрос
    http://127.0.0.1:8000/lessons/
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения описания одного урока через API (generic). Вызывается через GET-запрос
    http://127.0.0.1:8000/lessons/<код урока>"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer

class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для обновления информации по уроку через API (generic). Вызывается через PUT-запрос
    http://127.0.0.1:8000/lessons/update/2/
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer

class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока через API (generic). Вызывается через DELETE-запрос.
    Пример запроса:
    http://127.0.0.1:8000/lessons/delete/2/
    """
    queryset = Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """Контроллер для получения информации по платежам с возможностью поисковых запросов
    Пример запроса:
    http://127.0.0.1:8000/payment?ordering=-payment_amount&lesson=29"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerialaizer
    # filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    # search_fields = ["course", "lesson", "payment_method",] # Для SearchFilter
    filterset_fields = ["course", "lesson", "payment_method",] # Для DjangoFilterBackend
    ordering_fields = ["date_pay", "payment_amount"]
