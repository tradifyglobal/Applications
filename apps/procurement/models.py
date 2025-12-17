from django.db import models
from django.core.validators import MinValueValidator


class GoodsReceiptLineItem(models.Model):
    """Goods receipt line items"""
    goods_receipt_number = models.CharField(max_length=100)
    item_description = models.CharField(max_length=255)
    ordered_quantity = models.IntegerField(validators=[MinValueValidator(1)])
    received_quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.goods_receipt_number} - {self.item_description}"


class GoodsReceipt(models.Model):
    """Goods receipts"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('REJECTED', 'Rejected'),
    )
    
    receipt_number = models.CharField(max_length=100, unique=True)
    purchase_order_number = models.CharField(max_length=100)
    receipt_date = models.DateField()
    total_items = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    received_by = models.CharField(max_length=255)
    
    def __str__(self):
        return self.receipt_number


class PoLineItem(models.Model):
    """PO line items"""
    purchase_order_number = models.CharField(max_length=100)
    item_description = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    line_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.purchase_order_number} - {self.item_description}"


class ProcurementSettings(models.Model):
    """Procurement module settings"""
    auto_po_generation = models.BooleanField(default=False)
    three_way_matching_required = models.BooleanField(default=True)
    approval_threshold_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    default_payment_terms_days = models.IntegerField(default=30)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Procurement Settings"
    
    def __str__(self):
        return "Procurement Settings"


class PurchaseOrder(models.Model):
    """Purchase orders"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RECEIVED', 'Received'),
        ('INVOICED', 'Invoiced'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    
    po_number = models.CharField(max_length=100, unique=True)
    vendor_name = models.CharField(max_length=255)
    po_date = models.DateField()
    delivery_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    def __str__(self):
        return self.po_number


class RequestForQuotation(models.Model):
    """Requests for quotations (RFQ)"""
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('QUOTED', 'Quoted'),
        ('AWARDED', 'Awarded'),
        ('CLOSED', 'Closed'),
    )
    
    rfq_number = models.CharField(max_length=100, unique=True)
    rfq_date = models.DateField()
    items_description = models.TextField()
    required_delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    vendor_count = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return self.rfq_number


class ThreeWayMatching(models.Model):
    """Three-way matching (PO, GR, Invoice)"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('MATCHED', 'Matched'),
        ('VARIANCE', 'Variance'),
        ('UNMATCHED', 'Unmatched'),
    )
    
    po_number = models.CharField(max_length=100)
    goods_receipt_number = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100)
    matching_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    variance_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Match: {self.po_number}/{self.goods_receipt_number}/{self.invoice_number}"


class VendorQuotation(models.Model):
    """Vendor quotations"""
    STATUS_CHOICES = (
        ('QUOTED', 'Quoted'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED', 'Expired'),
    )
    
    quotation_number = models.CharField(max_length=100, unique=True)
    vendor_name = models.CharField(max_length=255)
    rfq_number = models.CharField(max_length=100)
    quotation_date = models.DateField()
    expiry_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='QUOTED')
    
    def __str__(self):
        return self.quotation_number


class Vendor(models.Model):
    """Legacy vendor model - kept for backward compatibility"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'procurement_vendor'
        ordering = ['name']

    def __str__(self):
        return self.name
