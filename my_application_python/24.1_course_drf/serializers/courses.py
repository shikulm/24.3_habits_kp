from rest_framework import serializers

from courses.models import Course, Lesson, Payment, Subscription
from courses.validators import UrlValidate
from serializers.users import UserSerialaizer


class LessonSerialaizer(serializers.ModelSerializer):
    """Сериалайзер для уроков. Выводит все поля из модели с уроками (Lesson)"""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidate(field='video_url')]

class CourseSerialaizer(serializers.ModelSerializer):
    """Сериалайзер для курсов.
    Выводит все поля из модели с курсами (Course), количество уроков в курсе и вложенный список входящих в курс уроков"""
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    is_subscripe = serializers.SerializerMethodField(read_only=True)

    # Альтернативный способ через SerializerMethodField()
    # lessons_count = serializers.SerializerMethodField()
    #
    # def get_lessons_count(self, instance):
    #     return Lesson.objects.filter(course__id=instance.pk).count()

    def get_is_subscripe(self, instance):
        """Проверяет есть ли у пользователя подписка на курс"""
        request = self.context.get('request', None)
        if request:
            return Subscription.objects.filter(course__id=instance.pk, user=request.user).exists()
        return False


    lessons = LessonSerialaizer(many=True, read_only=True)

    class Meta:
        model = Course
        # fields = '__all__'
        fields = ('id', 'title', 'preview', 'description', 'is_subscripe', 'lessons_count', 'lessons')


class PaymentSerialaizer(serializers.ModelSerializer):
    """Сериалайзер по оплате за курсы или уроки.
    Выводит все поля из модели с оплатой (Payment), данные по пользователям, курсам и урокам"""

    user = UserSerialaizer()
    course = CourseSerialaizer()
    lesson = LessonSerialaizer()
    class Meta:
        model = Payment
        fields = '__all__'

class SubscriptionSerialaizer(serializers.ModelSerializer):
    """Сериалайзер по подписке на курсы и уроки.
    Выводит все поля из модели с подпиской (Subscription)"""

    class Meta:
        model = Subscription
        fields = '__all__'
