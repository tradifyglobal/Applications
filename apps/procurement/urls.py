from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet

app_name = 'procurement'

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
