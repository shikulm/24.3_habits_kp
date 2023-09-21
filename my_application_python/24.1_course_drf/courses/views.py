from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from courses.models import Course, Lesson, Payment, Subscription
from courses.paginators import CoursePagintor, LessonPagintor
from courses.permissions import IsOwner, IsOwnerOrModerator, IsNotModerator
from serializers.courses import CourseSerialaizer, LessonSerialaizer, PaymentSerialaizer, SubscriptionSerialaizer, \
    PaymentCourseSerialaizer

from rest_framework.permissions import IsAuthenticated

from services import create_price
from services.create_price import retrive_session

from courses.tasks import send_mails


# Create your views here.




class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер для работы с курсом через API (ViewSet)"""
    queryset = Course.objects.all()
    serializer_class = CourseSerialaizer
    pagination_class = CoursePagintor

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

    def perform_update(self, serializer):
        super().perform_update(serializer)
        send_mails.delay()


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
    pagination_class = LessonPagintor

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


class PaymentCourceCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания оплаты курсы через API (generic). Вызывается через POST-запрос
    http://127.0.0.1:8000/course/payment/create/
    """
    serializer_class = PaymentCourseSerialaizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Сохраняем параметры оплаты
        new_payment = serializer.save(user = self.request.user)
        # new_payment.user = self.request.user
        payment_data = create_price(new_payment.course_id)
        new_payment.payment_amount = payment_data.amount_total/100
        new_payment.payment_link = create_price(new_payment.course_id)
        new_payment.payment_url = payment_data.url
        new_payment.session_id = payment_data.id
        new_payment.payment_status = payment_data.payment_status
        new_payment.save()


class PaymentCourceUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для обновления информации о подписке на курсы через API (generic). Вызывается через PUT-запрос
    http://127.0.0.1:8000/course/payment/update/1
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentCourseSerialaizer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Сохраняем параметры оплаты
        pay = self.get_object()
        ses = retrive_session(pay.pk)



class SubscriptionListAPIView(generics.ListAPIView):
    """Контроллер для получения списка подписок на курсы через API (generic). Вызывается через POST-запрос
    http://127.0.0.1:8000/subscripe/create/
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerialaizer
    permission_classes = [IsAuthenticated]

class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения информации о подписке на курсы через API (generic). Вызывается через GET-запрос
    http://127.0.0.1:8000/subscripe/1/
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerialaizer
    permission_classes = [IsAuthenticated]

class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Контроллер для получения информации о подписке на курсы через API (generic). Вызывается через GET-запрос
    http://127.0.0.1:8000/subscripe/1/
    """
    serializer_class = SubscriptionSerialaizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_subscripe = serializer.save()
        new_subscripe.user = self.request.user
        new_subscripe.save()

class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления информации о подписке на курсы через API (generic). Вызывается через DELETE-запрос
    http://127.0.0.1:8000/subscripe/delete/1/
    """
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]