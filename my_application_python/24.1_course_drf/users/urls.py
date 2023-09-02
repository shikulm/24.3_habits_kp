from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserModelViewSet

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r'users', UserModelViewSet, basename='users')

urlpatterns = [

] + router.urls

