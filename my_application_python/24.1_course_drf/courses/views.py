from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from courses.models import Course, Lesson, Payment
from courses.permissions import IsOwner, IsModerator, IsOwnerOrModerator, IsNotModerator
from serializers.courses import CourseSerialaizer, LessonSerialaizer, PaymentSerialaizer

from rest_framework.permissions import IsAuthenticated


# Create your views here.




class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер для работы с курсом через API (ViewSet)"""
    queryset = Course.objects.all()
    serializer_class = CourseSerialaizer

    def get_permissions(self):
        """Определение прав доступа"""
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action in ('retrieve', 'update'):
            permission_classes = [IsOwnerOrModerator]
        else: # destroy
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Назначение владельца при создании куурса"""
        new_сourse = serializer.save()
        new_сourse.owner = self.request.user
        new_сourse.save()

    def get_queryset(self):
        """Для пользователей не из группы модераторов получаем только список принадлежащих им курсов.
        Для модераторов выводим полный список"""
        if self.request.user.groups.filter(name = 'moderator').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока через API (generic).
    Вызывается через POST-запрос
    http://127.0.0.1:8000/lessons/create/"""
    serializer_class = LessonSerialaizer
    # permission_classes = [IsAuthenticated, IsOwner]
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Контроллер для получения списка уроков через API (generic). Вызывается через GET-запрос
    http://127.0.0.1:8000/lessons/
    """
    # queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer
    # permission_classes = [IsAuthenticated, IsOwner, IsModerator]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Для пользователей не из группы модераторов получаем только список принадлежащих им уроков.
        Для модераторов выводим полный список"""
        if self.request.user.groups.filter(name = 'moderator').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения описания одного урока через API (generic). Вызывается через GET-запрос
    http://127.0.0.1:8000/lessons/<код урока>"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer
    # permission_classes = [IsAuthenticated, IsOwner, IsModerator]
    permission_classes = [IsOwnerOrModerator]

class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для обновления информации по уроку через API (generic). Вызывается через PUT-запрос
    http://127.0.0.1:8000/lessons/update/2/
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerialaizer
    permission_classes = [IsOwnerOrModerator]

class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока через API (generic). Вызывается через DELETE-запрос.
    Пример запроса:
    http://127.0.0.1:8000/lessons/delete/2/
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


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
    permission_classes = [IsAuthenticated]
