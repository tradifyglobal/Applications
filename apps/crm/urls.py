from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'crm'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]

