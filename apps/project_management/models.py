from django.db import models
from django.core.validators import MinValueValidator


class ProjectBudget(models.Model):
    """Project budgets"""
    project_name = models.CharField(max_length=255)
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    spent_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    budget_variance = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"{self.project_name} - Budget"


class ProjectKPI(models.Model):
    """Project KPIs"""
    METRIC_TYPE = (
        ('SCHEDULE', 'Schedule Performance'),
        ('COST', 'Cost Performance'),
        ('QUALITY', 'Quality'),
        ('SCOPE', 'Scope'),
    )
    
    project_name = models.CharField(max_length=255)
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPE)
    target_value = models.DecimalField(max_digits=15, decimal_places=2)
    actual_value = models.DecimalField(max_digits=15, decimal_places=2)
    measurement_date = models.DateField()
    
    class Meta:
        verbose_name_plural = "Project KPIs"
    
    def __str__(self):
        return f"{self.project_name} - {self.metric_type}"


class ProjectPhase(models.Model):
    """Project phases"""
    phase_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    sequence = models.IntegerField()
    status = models.CharField(max_length=20, choices=(('PLANNED', 'Planned'), ('ACTIVE', 'Active'), ('COMPLETED', 'Completed')))
    
    class Meta:
        verbose_name_plural = "Project Phases"
    
    def __str__(self):
        return self.phase_name


class ProjectSettings(models.Model):
    """Project management module settings"""
    default_project_duration_days = models.IntegerField(default=90)
    auto_resource_allocation = models.BooleanField(default=False)
    time_tracking_enabled = models.BooleanField(default=True)
    budget_tracking_enabled = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Project Settings"
    
    def __str__(self):
        return "Project Management Settings"


class Project(models.Model):
    """Projects"""
    STATUS_CHOICES = (
        ('PLANNED', 'Planned'),
        ('ACTIVE', 'Active'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    project_code = models.CharField(max_length=50, unique=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    project_manager = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.project_name


class ResourceAllocation(models.Model):
    """Resource allocations"""
    project_name = models.CharField(max_length=255)
    resource_name = models.CharField(max_length=255)
    allocation_percentage = models.IntegerField(validators=[MinValueValidator(0)])
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.resource_name} - {self.project_name}"


class Task(models.Model):
    """Project tasks"""
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
        ('CANCELLED', 'Cancelled'),
    )
    
    task_number = models.CharField(max_length=100, unique=True)
    task_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    assigned_to = models.CharField(max_length=255)
    start_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    priority = models.CharField(max_length=20, choices=(('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')))
    completion_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.task_name


class TimeEntry(models.Model):
    """Time entries for tasks"""
    task_number = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=255)
    entry_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.employee_name} - {self.entry_date}"
