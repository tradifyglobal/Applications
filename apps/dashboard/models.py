from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Dashboard(models.Model):
    """Main dashboard configuration"""
    LAYOUT_CHOICES = (
        ('1', '1 Column'),
        ('2', '2 Columns'),
        ('3', '3 Columns'),
        ('4', '4 Columns'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    layout = models.CharField(max_length=10, choices=LAYOUT_CHOICES, default='2')
    theme_color = models.CharField(max_length=20, default='blue')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class DashboardWidget(models.Model):
    """Dashboard widgets configuration"""
    WIDGET_TYPE_CHOICES = (
        ('CARD', 'Card'),
        ('CHART', 'Chart'),
        ('TABLE', 'Table'),
        ('GAUGE', 'Gauge'),
        ('STAT', 'Statistic'),
        ('TIMELINE', 'Timeline'),
        ('MAP', 'Map'),
        ('CALENDAR', 'Calendar'),
    )
    
    CHART_TYPE_CHOICES = (
        ('LINE', 'Line Chart'),
        ('BAR', 'Bar Chart'),
        ('PIE', 'Pie Chart'),
        ('DOUGHNUT', 'Doughnut Chart'),
        ('AREA', 'Area Chart'),
        ('SCATTER', 'Scatter Plot'),
    )
    
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPE_CHOICES)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPE_CHOICES, null=True, blank=True)
    position = models.IntegerField(default=0)
    width = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    height = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    is_visible = models.BooleanField(default=True)
    refresh_interval = models.IntegerField(default=300, help_text="Refresh interval in seconds")
    data_source = models.CharField(max_length=255, blank=True)
    configuration = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return f"{self.title} ({self.widget_type})"


class DashboardKPI(models.Model):
    """Key Performance Indicators"""
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    )
    
    widget = models.OneToOneField(DashboardWidget, on_delete=models.CASCADE, related_name='kpi')
    metric_name = models.CharField(max_length=255)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    target_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    previous_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    threshold_warning = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    threshold_critical = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    trend = models.CharField(max_length=10, choices=[('UP', 'Up'), ('DOWN', 'Down'), ('STABLE', 'Stable')], default='STABLE')
    trend_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_updated']
    
    def __str__(self):
        return f"{self.metric_name} - {self.current_value}{self.unit}"


class DashboardChartData(models.Model):
    """Store chart data points"""
    widget = models.ForeignKey(DashboardWidget, on_delete=models.CASCADE, related_name='chart_data')
    label = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.label}: {self.value}"


class UserDashboard(models.Model):
    """User personalized dashboard"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_preference')
    primary_dashboard = models.ForeignKey(Dashboard, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_users')
    last_accessed_at = models.DateTimeField(auto_now=True)
    theme_preference = models.CharField(max_length=50, choices=[
        ('LIGHT', 'Light'),
        ('DARK', 'Dark'),
        ('AUTO', 'Auto'),
    ], default='AUTO')
    notifications_enabled = models.BooleanField(default=True)
    favorite_widgets = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = "User Dashboard"
        verbose_name_plural = "User Dashboards"
    
    def __str__(self):
        return f"{self.user.username}'s Dashboard"


class DashboardAlert(models.Model):
    """Dashboard alerts and notifications"""
    ALERT_TYPE_CHOICES = (
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('SUCCESS', 'Success'),
    )
    
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    action_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type}: {self.title}"


class DashboardReport(models.Model):
    """Scheduled dashboard reports"""
    FREQUENCY_CHOICES = (
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    )
    
    FORMAT_CHOICES = (
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('CSV', 'CSV'),
        ('EMAIL', 'Email'),
    )
    
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='reports')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    recipients = models.JSONField(default=list, help_text="List of email recipients")
    is_active = models.BooleanField(default=True)
    last_generated = models.DateTimeField(null=True, blank=True)
    next_scheduled = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.frequency})"


class DashboardMetric(models.Model):
    """Track system-wide metrics"""
    METRIC_TYPE_CHOICES = (
        ('REVENUE', 'Revenue'),
        ('EXPENSES', 'Expenses'),
        ('USERS', 'Users'),
        ('ORDERS', 'Orders'),
        ('PRODUCTS', 'Products'),
        ('INVENTORY', 'Inventory'),
        ('PERFORMANCE', 'Performance'),
        ('CUSTOM', 'Custom'),
    )
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPE_CHOICES)
    metric_key = models.CharField(max_length=255, unique=True)
    metric_name = models.CharField(max_length=255)
    metric_value = models.DecimalField(max_digits=15, decimal_places=2)
    metric_unit = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    period_start = models.DateTimeField(null=True, blank=True)
    period_end = models.DateTimeField(null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metric_type', '-timestamp']),
            models.Index(fields=['metric_key', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.metric_name}: {self.metric_value}{self.metric_unit}"


class DashboardActivity(models.Model):
    """Track dashboard user activity"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_activities')
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50)
    widget = models.ForeignKey(DashboardWidget, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Dashboard Activities"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.action}"
