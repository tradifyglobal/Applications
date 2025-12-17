from rest_framework import serializers
from .models import (
    Dashboard, DashboardWidget, DashboardKPI, DashboardChartData,
    UserDashboard, DashboardAlert, DashboardReport, DashboardMetric,
    DashboardActivity
)


class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = ['id', 'dashboard', 'title', 'description', 'widget_type', 'chart_type', 
                  'position', 'width', 'height', 'is_visible', 'refresh_interval', 
                  'data_source', 'configuration', 'created_at', 'updated_at']


class DashboardKPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardKPI
        fields = ['id', 'widget', 'metric_name', 'current_value', 'target_value', 
                  'previous_value', 'unit', 'status', 'threshold_warning', 'threshold_critical',
                  'trend', 'trend_percentage', 'last_updated']


class DashboardChartDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardChartData
        fields = ['id', 'widget', 'label', 'value', 'timestamp', 'metadata']


class DashboardAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardAlert
        fields = ['id', 'dashboard', 'alert_type', 'title', 'message', 'is_read',
                  'created_at', 'dismissed_at', 'action_url']


class DashboardReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardReport
        fields = ['id', 'dashboard', 'name', 'description', 'frequency', 'format',
                  'recipients', 'is_active', 'last_generated', 'next_scheduled', 
                  'created_at', 'created_by']


class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = ['id', 'metric_type', 'metric_key', 'metric_name', 'metric_value',
                  'metric_unit', 'timestamp', 'period_start', 'period_end', 'tags', 'metadata']


class DashboardActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardActivity
        fields = ['id', 'user', 'dashboard', 'action', 'widget', 'details', 'timestamp']


class UserDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDashboard
        fields = ['id', 'user', 'primary_dashboard', 'last_accessed_at', 'theme_preference',
                  'notifications_enabled', 'favorite_widgets']


class DashboardDetailSerializer(serializers.ModelSerializer):
    widgets = DashboardWidgetSerializer(many=True, read_only=True)
    alerts = DashboardAlertSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dashboard
        fields = ['id', 'name', 'description', 'is_default', 'layout', 'theme_color',
                  'created_at', 'updated_at', 'created_by', 'widgets', 'alerts']


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ['id', 'name', 'description', 'is_default', 'layout', 'theme_color',
                  'created_at', 'updated_at', 'created_by']
