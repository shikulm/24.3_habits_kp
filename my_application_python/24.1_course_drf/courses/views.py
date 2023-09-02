from django.shortcuts import render
from rest_framework import viewsets, generics

from courses.models import Course, Lesson
from courses.serializers import CourseSerialaizer, LessonSerialaizer


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
