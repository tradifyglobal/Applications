from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'employee_expenses'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]

