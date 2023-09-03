from rest_framework import serializers

from courses.models import Course, Lesson

class LessonSerialaizer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerialaizer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    lessons = LessonSerialaizer(many=True)

    class Meta:
        model = Course
        fields = '__all__'



