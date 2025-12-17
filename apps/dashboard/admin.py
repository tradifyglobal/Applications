from django.contrib import admin
from .models import (
    Dashboard, DashboardWidget, DashboardKPI, DashboardChartData,
    UserDashboard, DashboardAlert, DashboardReport, DashboardMetric,
    DashboardActivity
)


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_default', 'layout', 'theme_color', 'created_at']
    list_filter = ['is_default', 'theme_color', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'dashboard', 'widget_type', 'position', 'is_visible', 'created_at']
    list_filter = ['widget_type', 'is_visible', 'dashboard']
    search_fields = ['title', 'description']
    ordering = ['dashboard', 'position']


@admin.register(DashboardKPI)
class DashboardKPIAdmin(admin.ModelAdmin):
    list_display = ['metric_name', 'widget', 'current_value', 'status', 'trend', 'trend_percentage']
    list_filter = ['status', 'trend', 'widget__dashboard']
    search_fields = ['metric_name']
    ordering = ['-last_updated']


@admin.register(DashboardChartData)
class DashboardChartDataAdmin(admin.ModelAdmin):
    list_display = ['label', 'widget', 'value', 'timestamp']
    list_filter = ['widget', 'timestamp']
    search_fields = ['label']
    ordering = ['-timestamp']


@admin.register(UserDashboard)
class UserDashboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'primary_dashboard', 'theme_preference', 'notifications_enabled', 'last_accessed_at']
    list_filter = ['theme_preference', 'notifications_enabled']
    search_fields = ['user__username']
    ordering = ['-last_accessed_at']


@admin.register(DashboardAlert)
class DashboardAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'dashboard', 'alert_type', 'is_read', 'created_at']
    list_filter = ['alert_type', 'is_read', 'dashboard', 'created_at']
    search_fields = ['title', 'message']
    ordering = ['-created_at']


@admin.register(DashboardReport)
class DashboardReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'dashboard', 'frequency', 'format', 'is_active', 'last_generated']
    list_filter = ['frequency', 'format', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_name', 'metric_type', 'metric_key', 'metric_value', 'metric_unit', 'timestamp']
    list_filter = ['metric_type', 'timestamp']
    search_fields = ['metric_name', 'metric_key']
    ordering = ['-timestamp']


@admin.register(DashboardActivity)
class DashboardActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'dashboard', 'action', 'widget', 'timestamp']
    list_filter = ['action', 'dashboard', 'timestamp']
    search_fields = ['user__username', 'action']
    ordering = ['-timestamp']
