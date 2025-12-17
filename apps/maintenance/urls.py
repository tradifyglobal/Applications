from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, MaintenanceRequestViewSet

app_name = 'maintenance'

router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet)
router.register(r'requests', MaintenanceRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
