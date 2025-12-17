from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'site_maintenance'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]

