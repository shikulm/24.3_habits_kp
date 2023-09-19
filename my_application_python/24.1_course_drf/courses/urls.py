from django.urls import path
from rest_framework.routers import DefaultRouter
from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonListAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionListAPIView, \
    SubscriptionRetrieveAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView, PaymentCourceCreateAPIView, \
    PaymentCourceUpdateAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name = 'lesson-one'),
    path('lessons/create/', LessonCreateAPIView.as_view(),name = 'lesson-create'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(),name = 'lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(),name = 'lesson-delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('course/payment/create/', PaymentCourceCreateAPIView.as_view(), name='payment-course-create'),
    path('course/payment/update/<int:pk>/', PaymentCourceUpdateAPIView.as_view(), name='payment-course-update'),

    path('subscripe/', SubscriptionListAPIView.as_view(), name='subscripe-list'),
    path('subscripe/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscripe-one'),
    path('subscripe/create/', SubscriptionCreateAPIView.as_view(), name='subscripe-create'),
    path('subscripe/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscripe-delete'),
] + router.urls