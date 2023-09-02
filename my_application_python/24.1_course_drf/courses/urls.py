from django.urls import path
from rest_framework.routers import DefaultRouter
from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonListAPIView, LessonUpdateAPIView, LessonDestroyAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name = 'lesson-one'),
    path('lessons/create/', LessonCreateAPIView.as_view(),name = 'lesson-create'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(),name = 'lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(),name = 'lesson-delete'),
] + router.urls