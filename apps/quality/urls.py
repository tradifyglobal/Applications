from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QualityCheckViewSet

app_name = 'quality'

router = DefaultRouter()
router.register(r'checks', QualityCheckViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
