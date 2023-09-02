from rest_framework import serializers

from courses.models import Course, Lesson


class CourseSerialaizer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)


    class Meta:
        model = Course
        fields = '__all__'


class LessonSerialaizer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
