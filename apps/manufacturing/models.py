from django.db import models
from django.core.validators import MinValueValidator


class AfterSalesService(models.Model):
    """After-sales services"""
    service_name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=100)
    duration_days = models.IntegerField(validators=[MinValueValidator(1)])
    cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name_plural = "After Sales Services"
    
    def __str__(self):
        return self.service_name


class BillOfMaterial(models.Model):
    """Bill of materials (BOM)"""
    bom_code = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Bills of Material"
    
    def __str__(self):
        return self.bom_code


class Courier(models.Model):
    """Courier services"""
    courier_name = models.CharField(max_length=255)
    courier_code = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.courier_name


class DistributorContact(models.Model):
    """Distributor contacts"""
    contact_name = models.CharField(max_length=255)
    distributor_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    designation = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.contact_name} - {self.distributor_name}"


class DistributorOrder(models.Model):
    """Distributor orders"""
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    )
    
    order_number = models.CharField(max_length=100, unique=True)
    distributor_name = models.CharField(max_length=255)
    order_date = models.DateField()
    order_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    
    def __str__(self):
        return self.order_number


class DistributorPerformance(models.Model):
    """Distributor performance metrics"""
    distributor_name = models.CharField(max_length=255)
    period_month = models.IntegerField()
    period_year = models.IntegerField()
    sales_volume = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    order_fulfillment_rate = models.DecimalField(max_digits=5, decimal_places=2)
    quality_rating = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.distributor_name} - {self.period_year}-{self.period_month}"


class Distributor(models.Model):
    """Distributors"""
    distributor_code = models.CharField(max_length=50, unique=True)
    distributor_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    territory = models.CharField(max_length=255)
    payment_terms = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.distributor_name


class Equipment(models.Model):
    """Manufacturing equipment"""
    equipment_code = models.CharField(max_length=50, unique=True)
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    acquisition_date = models.DateField()
    capacity = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.equipment_name


class OrderShipment(models.Model):
    """Order shipments"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
    )
    
    shipment_number = models.CharField(max_length=100, unique=True)
    order_number = models.CharField(max_length=100)
    shipment_date = models.DateField()
    courier = models.CharField(max_length=255)
    tracking_number = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    expected_delivery_date = models.DateField()
    
    def __str__(self):
        return self.shipment_number


class ProductCategory(models.Model):
    """Product categories"""
    category_code = models.CharField(max_length=50, unique=True)
    category_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Product Categories"
    
    def __str__(self):
        return self.category_name


class ProductionOrder(models.Model):
    """Production orders"""
    STATUS_CHOICES = (
        ('PLANNED', 'Planned'),
        ('RELEASED', 'Released'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    order_number = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    
    def __str__(self):
        return self.order_number


class Product(models.Model):
    """Products in manufacturing"""
    product_code = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.product_name


class QualityInspection(models.Model):
    """Quality inspections"""
    STATUS_CHOICES = (
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    )
    
    inspection_date = models.DateField()
    product_name = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=100)
    inspection_result = models.CharField(max_length=20, choices=STATUS_CHOICES)
    defects_found = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product_name} - {self.batch_number}"


class RawMaterial(models.Model):
    """Raw materials"""
    material_code = models.CharField(max_length=50, unique=True)
    material_name = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=20)
    reorder_level = models.IntegerField(validators=[MinValueValidator(1)])
    current_stock = models.IntegerField(validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.material_name


class Routing(models.Model):
    """Product routings (manufacturing process)"""
    routing_code = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=255)
    sequence = models.IntegerField()
    work_center = models.CharField(max_length=100)
    operation_time_hours = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.routing_code


class ServiceActivity(models.Model):
    """Service activities"""
    activity_date = models.DateField()
    customer_name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=100)
    duration_hours = models.DecimalField(max_digits=10, decimal_places=2)
    service_cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name_plural = "Service Activities"
    
    def __str__(self):
        return f"{self.customer_name} - {self.activity_date}"


class WarrantyRegistration(models.Model):
    """Warranty registrations"""
    registration_number = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100)
    warranty_start_date = models.DateField()
    warranty_end_date = models.DateField()
    customer_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.registration_number


class WorkCenter(models.Model):
    """Work centers in manufacturing"""
    work_center_code = models.CharField(max_length=50, unique=True)
    work_center_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity_per_hour = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return self.work_center_name
