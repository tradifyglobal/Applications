from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Dashboard, DashboardWidget, DashboardKPI, DashboardChartData,
    UserDashboard, DashboardAlert, DashboardReport, DashboardMetric,
    DashboardActivity
)
from .serializers import (
    DashboardSerializer, DashboardDetailSerializer, DashboardWidgetSerializer,
    DashboardKPISerializer, DashboardChartDataSerializer, UserDashboardSerializer,
    DashboardAlertSerializer, DashboardReportSerializer, DashboardMetricSerializer,
    DashboardActivitySerializer
)


class DashboardViewSet(viewsets.ModelViewSet):
    """Dashboard management"""
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_default', 'theme_color']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DashboardDetailSerializer
        return DashboardSerializer
    
    @action(detail=False, methods=['get'])
    def default_dashboard(self, request):
        """Get default dashboard"""
        dashboard = Dashboard.objects.filter(is_default=True).first()
        if not dashboard:
            dashboard = Dashboard.objects.first()
        
        if dashboard:
            serializer = DashboardDetailSerializer(dashboard)
            return Response(serializer.data)
        return Response({'detail': 'No dashboard found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Get dashboard analytics"""
        dashboard = self.get_object()
        analytics = {
            'total_widgets': dashboard.widgets.count(),
            'active_widgets': dashboard.widgets.filter(is_visible=True).count(),
            'total_alerts': dashboard.alerts.count(),
            'unread_alerts': dashboard.alerts.filter(is_read=False).count(),
            'total_activities': dashboard.activities.count(),
        }
        return Response(analytics)


class DashboardWidgetViewSet(viewsets.ModelViewSet):
    """Dashboard widget management"""
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dashboard', 'widget_type', 'is_visible']
    search_fields = ['title', 'description']
    ordering_fields = ['position', 'created_at']
    
    @action(detail=True, methods=['post'])
    def toggle_visibility(self, request, pk=None):
        """Toggle widget visibility"""
        widget = self.get_object()
        widget.is_visible = not widget.is_visible
        widget.save()
        return Response({'is_visible': widget.is_visible})


class DashboardKPIViewSet(viewsets.ModelViewSet):
    """Dashboard KPI management"""
    queryset = DashboardKPI.objects.all()
    serializer_class = DashboardKPISerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['widget', 'status', 'trend']
    ordering_fields = ['current_value', 'trend_percentage', 'last_updated']
    
    @action(detail=True, methods=['post'])
    def update_value(self, request, pk=None):
        """Update KPI value"""
        kpi = self.get_object()
        previous_value = kpi.current_value
        kpi.previous_value = previous_value
        kpi.current_value = request.data.get('current_value')
        
        # Calculate trend
        if kpi.previous_value:
            percentage_change = ((kpi.current_value - kpi.previous_value) / kpi.previous_value) * 100
            kpi.trend_percentage = percentage_change
            kpi.trend = 'UP' if percentage_change > 0 else ('DOWN' if percentage_change < 0 else 'STABLE')
        
        kpi.save()
        serializer = self.get_serializer(kpi)
        return Response(serializer.data)


class DashboardChartDataViewSet(viewsets.ModelViewSet):
    """Dashboard chart data management"""
    queryset = DashboardChartData.objects.all()
    serializer_class = DashboardChartDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['widget']
    ordering_fields = ['timestamp', 'value']


class UserDashboardViewSet(viewsets.ModelViewSet):
    """User dashboard preferences"""
    queryset = UserDashboard.objects.all()
    serializer_class = UserDashboardSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_dashboard(self, request):
        """Get current user's dashboard"""
        user_dashboard, created = UserDashboard.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(user_dashboard)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def set_primary_dashboard(self, request):
        """Set primary dashboard for current user"""
        user_dashboard, created = UserDashboard.objects.get_or_create(user=request.user)
        dashboard_id = request.data.get('dashboard_id')
        try:
            dashboard = Dashboard.objects.get(id=dashboard_id)
            user_dashboard.primary_dashboard = dashboard
            user_dashboard.save()
            serializer = self.get_serializer(user_dashboard)
            return Response(serializer.data)
        except Dashboard.DoesNotExist:
            return Response({'detail': 'Dashboard not found'}, status=status.HTTP_404_NOT_FOUND)


class DashboardAlertViewSet(viewsets.ModelViewSet):
    """Dashboard alert management"""
    queryset = DashboardAlert.objects.all()
    serializer_class = DashboardAlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['dashboard', 'alert_type', 'is_read']
    ordering_fields = ['created_at']
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark alert as read"""
        alert = self.get_object()
        alert.is_read = True
        alert.save()
        return Response({'is_read': alert.is_read})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all alerts as read"""
        dashboard_id = request.data.get('dashboard_id')
        if dashboard_id:
            DashboardAlert.objects.filter(dashboard_id=dashboard_id, is_read=False).update(is_read=True)
        return Response({'status': 'All alerts marked as read'})


class DashboardReportViewSet(viewsets.ModelViewSet):
    """Dashboard report management"""
    queryset = DashboardReport.objects.all()
    serializer_class = DashboardReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dashboard', 'frequency', 'format', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'last_generated']
    
    @action(detail=True, methods=['post'])
    def generate_report(self, request, pk=None):
        """Generate report immediately"""
        report = self.get_object()
        report.last_generated = __import__('django.utils.timezone', fromlist=['now']).now()
        report.save()
        return Response({
            'status': 'Report generated successfully',
            'last_generated': report.last_generated,
            'format': report.format
        })


class DashboardMetricViewSet(viewsets.ModelViewSet):
    """Dashboard metrics tracking"""
    queryset = DashboardMetric.objects.all()
    serializer_class = DashboardMetricSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['metric_type', 'metric_key']
    search_fields = ['metric_name', 'metric_key']
    ordering_fields = ['timestamp', 'metric_value']
    
    @action(detail=False, methods=['get'])
    def latest_metrics(self, request):
        """Get latest metrics by type"""
        metric_type = request.query_params.get('metric_type', None)
        if metric_type:
            metrics = DashboardMetric.objects.filter(metric_type=metric_type).order_by('-timestamp')[:10]
        else:
            metrics = DashboardMetric.objects.order_by('-timestamp')[:20]
        
        serializer = self.get_serializer(metrics, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def metric_summary(self, request):
        """Get summary of metrics by type"""
        summary = {}
        for metric_type, _ in DashboardMetric.METRIC_TYPE_CHOICES:
            latest = DashboardMetric.objects.filter(metric_type=metric_type).latest('timestamp')
            summary[metric_type] = {
                'metric_name': latest.metric_name,
                'metric_value': str(latest.metric_value),
                'metric_unit': latest.metric_unit,
                'timestamp': latest.timestamp
            }
        return Response(summary)


class DashboardActivityViewSet(viewsets.ModelViewSet):
    """Dashboard activity tracking"""
    queryset = DashboardActivity.objects.all()
    serializer_class = DashboardActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'dashboard', 'action']
    ordering_fields = ['timestamp']
