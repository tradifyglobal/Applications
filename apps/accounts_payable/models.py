from django.db import models
from django.core.validators import MinValueValidator


class APAging(models.Model):
    """Accounts Payable aging report"""
    vendor_name = models.CharField(max_length=255)
    total_outstanding = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    amount_30_days = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    amount_60_days = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    amount_90_days = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    amount_over_90_days = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    report_date = models.DateField()
    
    class Meta:
        verbose_name_plural = "AP Agings"
    
    def __str__(self):
        return f"AP Aging - {self.vendor_name}"


class APDiscount(models.Model):
    """AP discount policies"""
    DISCOUNT_TYPE = (
        ('EARLY_PAYMENT', 'Early Payment'),
        ('VOLUME', 'Volume'),
        ('PROMOTIONAL', 'Promotional'),
    )
    
    discount_code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    applicable_to = models.CharField(max_length=255)
    effective_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.discount_code} - {self.discount_type}"


class APReconciliation(models.Model):
    """AP reconciliation"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RECONCILED', 'Reconciled'),
    )
    
    reconciliation_period = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_bills = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_payments = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    difference_amount = models.DecimalField(max_digits=15, decimal_places=2)
    reconciled_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"AP Reconciliation - {self.reconciliation_period}"


class APSettings(models.Model):
    """AP module settings"""
    auto_bill_matching_enabled = models.BooleanField(default=True)
    default_payment_terms_days = models.IntegerField(default=30)
    early_payment_discount_days = models.IntegerField(default=10)
    early_payment_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=2)
    required_approval_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    auto_duplicate_invoice_check = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "AP Settings"
    
    def __str__(self):
        return "AP Module Settings"


class VendorBill(models.Model):
    """Vendor bills"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('RECEIVED', 'Received'),
        ('APPROVED', 'Approved'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    
    bill_number = models.CharField(max_length=100, unique=True)
    vendor_name = models.CharField(max_length=255)
    bill_date = models.DateField()
    due_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    description = models.TextField(blank=True)
    received_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.bill_number} - {self.vendor_name}"


class VendorBillLineItem(models.Model):
    """Vendor bill line items"""
    vendor_bill = models.ForeignKey(VendorBill, on_delete=models.CASCADE, related_name='line_items')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    line_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.vendor_bill.bill_number} - {self.description}"


class VendorPayment(models.Model):
    """Vendor payments"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    payment_number = models.CharField(max_length=100, unique=True)
    vendor_bill = models.ForeignKey(VendorBill, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50)
    processed_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.payment_number}"
