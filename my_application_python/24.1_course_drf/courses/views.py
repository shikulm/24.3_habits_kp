from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from courses.models import Course, Lesson, Payment
from serializers.courses import CourseSerialaizer, LessonSerialaizer, PaymentSerialaizer


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerialaizer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerialaizer


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer

class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """Информация по платежам с возможностью поисковых запросов
    Пример запроса:
    http://127.0.0.1:8000/payment?ordering=-payment_amount&lesson=29"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerialaizer
    # filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    # search_fields = ["course", "lesson", "payment_method",] # Для SearchFilter
    filterset_fields = ["course", "lesson", "payment_method",] # Для DjangoFilterBackend
    ordering_fields = ["date_pay", "payment_amount"]
