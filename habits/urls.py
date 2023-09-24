from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, HabitPublicListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns = [
    path('habit/public/', HabitPublicListAPIView.as_view(), name = 'habit-public'),
    ] + router.urls