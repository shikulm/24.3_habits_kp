from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from django.urls import path


urlpatterns = [
    path('docs/', include_docs_urls(title='API Documentation')),
]