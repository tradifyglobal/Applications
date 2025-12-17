from django.db import models
from django.core.validators import MinValueValidator


class ARaging(models.Model):
    """Accounts Receivable aging report"""
    customer_name = models.CharField(max_length=255)
    total_outstanding = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    amount_30_days = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    amount_60_days = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    amount_90_days = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    amount_over_90_days = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    report_date = models.DateField()
    
    class Meta:
        verbose_name_plural = "AR Agings"
    
    def __str__(self):
        return f"AR Aging - {self.customer_name}"


class ARDiscount(models.Model):
    """AR discount policies"""
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


class ARReconciliation(models.Model):
    """AR reconciliation"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RECONCILED', 'Reconciled'),
    )
    
    reconciliation_period = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_invoices = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_payments = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    difference_amount = models.DecimalField(max_digits=15, decimal_places=2)
    reconciled_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"AR Reconciliation - {self.reconciliation_period}"


class ARSettings(models.Model):
    """AR module settings"""
    auto_invoice_enabled = models.BooleanField(default=True)
    default_payment_terms_days = models.IntegerField(default=30)
    early_payment_discount_days = models.IntegerField(default=10)
    early_payment_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=2)
    late_payment_charge_enabled = models.BooleanField(default=True)
    late_payment_charge_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    auto_dunning_enabled = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "AR Settings"
    
    def __str__(self):
        return "AR Module Settings"


class CustomerInvoice(models.Model):
    """Customer invoices"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('ISSUED', 'Issued'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    
    invoice_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    invoice_date = models.DateField()
    due_date = models.DateField()
    invoice_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    description = models.TextField(blank=True)
    issued_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"


class CustomerPayment(models.Model):
    """Customer payments"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
    )
    
    payment_number = models.CharField(max_length=100, unique=True)
    customer_invoice = models.ForeignKey(CustomerInvoice, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50)
    received_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.payment_number}"


class InvoiceLineItem(models.Model):
    """Invoice line items"""
    customer_invoice = models.ForeignKey(CustomerInvoice, on_delete=models.CASCADE, related_name='line_items')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    line_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.customer_invoice.invoice_number} - {self.description}"
