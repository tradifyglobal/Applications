from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'sites'

router = DefaultRouter()
router.register(r'sites', views.SiteViewSet, basename='site')

urlpatterns = [
    path('', include(router.urls)),
]
