from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardViewSet, DashboardWidgetViewSet, DashboardKPIViewSet,
    DashboardChartDataViewSet, UserDashboardViewSet, DashboardAlertViewSet,
    DashboardReportViewSet, DashboardMetricViewSet, DashboardActivityViewSet
)

router = DefaultRouter()
router.register(r'dashboards', DashboardViewSet, basename='dashboard')
router.register(r'widgets', DashboardWidgetViewSet, basename='widget')
router.register(r'kpis', DashboardKPIViewSet, basename='kpi')
router.register(r'chart-data', DashboardChartDataViewSet, basename='chart-data')
router.register(r'user-dashboards', UserDashboardViewSet, basename='user-dashboard')
router.register(r'alerts', DashboardAlertViewSet, basename='alert')
router.register(r'reports', DashboardReportViewSet, basename='report')
router.register(r'metrics', DashboardMetricViewSet, basename='metric')
router.register(r'activities', DashboardActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
]
