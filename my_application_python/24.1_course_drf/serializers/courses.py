from rest_framework import serializers

from courses.models import Course, Lesson, Payment
from serializers.users import UserSerialaizer


class LessonSerialaizer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerialaizer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)

    # Альтернативный способ через SerializerMethodField()
    # lessons_count = serializers.SerializerMethodField()
    #
    # def get_lessons_count(self, instance):
    #     return Lesson.objects.filter(course__id=instance.pk).count()


    lessons = LessonSerialaizer(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerialaizer(serializers.ModelSerializer):

    user = UserSerialaizer()
    course = CourseSerialaizer()
    lesson = LessonSerialaizer()
    class Meta:
        model = Payment
        fields = '__all__'
