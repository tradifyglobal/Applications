from django.db import models
from django.core.validators import MinValueValidator


class ComplianceAudit(models.Model):
    """Compliance audits"""
    STATUS_CHOICES = (
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    
    audit_number = models.CharField(max_length=100, unique=True)
    audit_name = models.CharField(max_length=255)
    audit_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    finding_count = models.IntegerField(default=0)
    completed_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.audit_number


class ComplianceStandard(models.Model):
    """Compliance standards"""
    standard_code = models.CharField(max_length=50, unique=True)
    standard_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requirements = models.JSONField(help_text="Compliance requirements")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.standard_name


class DowntimeRecord(models.Model):
    """Downtime records"""
    equipment_name = models.CharField(max_length=255)
    downtime_start = models.DateTimeField()
    downtime_end = models.DateTimeField(null=True, blank=True)
    downtime_hours = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    impact = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.equipment_name} - {self.downtime_start}"


class MaintenanceAsset(models.Model):
    """Assets under maintenance"""
    asset_code = models.CharField(max_length=50, unique=True)
    asset_name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    acquisition_date = models.DateField()
    last_maintenance_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.asset_name


class MaintenanceCost(models.Model):
    """Maintenance costs"""
    asset_name = models.CharField(max_length=255)
    maintenance_date = models.DateField()
    cost_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    cost_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.asset_name} - {self.cost_amount}"


class MaintenanceTask(models.Model):
    """Maintenance tasks"""
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    task_number = models.CharField(max_length=100, unique=True)
    asset_name = models.CharField(max_length=255)
    task_description = models.TextField()
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    assigned_to = models.CharField(max_length=255)
    
    def __str__(self):
        return self.task_number


class MaintenanceVendor(models.Model):
    """Maintenance service vendors"""
    vendor_code = models.CharField(max_length=50, unique=True)
    vendor_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_types = models.JSONField(help_text="List of service types")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.vendor_name


class SparePart(models.Model):
    """Spare parts inventory"""
    part_code = models.CharField(max_length=50, unique=True)
    part_name = models.CharField(max_length=255)
    applicable_asset_type = models.CharField(max_length=100)
    current_stock = models.IntegerField(validators=[MinValueValidator(0)])
    reorder_level = models.IntegerField(validators=[MinValueValidator(1)])
    unit_cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.part_name


class VendorContract(models.Model):
    """Vendor contracts for maintenance"""
    contract_number = models.CharField(max_length=100, unique=True)
    vendor_name = models.CharField(max_length=255)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    annual_value = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    service_scope = models.TextField()
    
    def __str__(self):
        return self.contract_number


class WorkOrderSparePart(models.Model):
    """Spare parts used in work orders"""
    work_order_number = models.CharField(max_length=100)
    part_code = models.CharField(max_length=50)
    quantity_used = models.IntegerField(validators=[MinValueValidator(1)])
    unit_cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.work_order_number} - {self.part_code}"


class WorkOrder(models.Model):
    """Maintenance work orders"""
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CLOSED', 'Closed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    wo_number = models.CharField(max_length=100, unique=True)
    asset_name = models.CharField(max_length=255)
    work_description = models.TextField()
    created_date = models.DateField()
    required_completion_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    assigned_technician = models.CharField(max_length=255)
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.wo_number
