from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkOrderViewSet

app_name = 'production'

router = DefaultRouter()
router.register(r'work-orders', WorkOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
