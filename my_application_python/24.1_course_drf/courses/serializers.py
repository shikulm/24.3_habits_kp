from rest_framework import serializers

from courses.models import Course, Lesson


class CourseSerialaizer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerialaizer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
