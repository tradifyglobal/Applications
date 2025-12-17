from django.db import models
from django.core.validators import MinValueValidator


class Activity(models.Model):
    """CRM activities"""
    ACTIVITY_TYPE = (
        ('CALL', 'Call'),
        ('EMAIL', 'Email'),
        ('MEETING', 'Meeting'),
        ('TASK', 'Task'),
        ('NOTE', 'Note'),
    )
    
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE)
    related_to = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    assigned_to = models.CharField(max_length=255)
    activity_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.activity_type} - {self.related_to}"


class Appointment(models.Model):
    """Appointments"""
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    )
    
    title = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    attendees = models.CharField(max_length=500)  # Comma-separated
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.start_datetime}"


class Campaign(models.Model):
    """Marketing campaigns"""
    STATUS_CHOICES = (
        ('PLANNING', 'Planning'),
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('COMPLETED', 'Completed'),
    )
    
    campaign_name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    spent_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.campaign_name


class Communication(models.Model):
    """Communications log"""
    COMMUNICATION_TYPE = (
        ('EMAIL', 'Email'),
        ('PHONE', 'Phone'),
        ('SMS', 'SMS'),
        ('CHAT', 'Chat'),
        ('MEETING', 'Meeting'),
    )
    
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPE)
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    communication_date = models.DateTimeField()
    related_to = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.communication_type} - {self.recipient}"


class Contact(models.Model):
    """CRM contacts"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contract(models.Model):
    """Contracts"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    )
    
    contract_number = models.CharField(max_length=100, unique=True)
    contract_name = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    contract_value = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    document_path = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return self.contract_number


class CrmSettings(models.Model):
    """CRM module settings"""
    auto_lead_assignment = models.BooleanField(default=True)
    auto_follow_up_enabled = models.BooleanField(default=True)
    default_follow_up_days = models.IntegerField(default=7)
    lead_scoring_enabled = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "CRM Settings"
    
    def __str__(self):
        return "CRM Settings"


class CustomerGroup(models.Model):
    """Customer groups"""
    group_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    member_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.group_name


class CustomerSegment(models.Model):
    """Customer segments"""
    segment_name = models.CharField(max_length=255, unique=True)
    criteria = models.JSONField(help_text="Segmentation criteria")
    member_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.segment_name


class EmailCampaign(models.Model):
    """Email campaigns"""
    campaign_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    recipient_count = models.IntegerField(validators=[MinValueValidator(0)])
    sent_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    open_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    click_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.campaign_name


class EmailGroup(models.Model):
    """Email distribution groups"""
    group_name = models.CharField(max_length=255, unique=True)
    email_list = models.JSONField(help_text="List of email addresses")
    member_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.group_name


class LeadSource(models.Model):
    """Lead sources"""
    source_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.source_name


class Lead(models.Model):
    """Sales leads"""
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('QUALIFIED', 'Qualified'),
        ('UNQUALIFIED', 'Unqualified'),
        ('CONVERTED', 'Converted'),
    )
    
    lead_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    lead_source = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    assigned_to = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.lead_name


class LoyaltyMember(models.Model):
    """Loyalty program members"""
    member_number = models.CharField(max_length=50, unique=True)
    member_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    points_balance = models.IntegerField(default=0)
    tier_level = models.CharField(max_length=50, default='BASIC')
    joined_date = models.DateField()
    
    def __str__(self):
        return f"{self.member_number} - {self.member_name}"


class LoyaltyProgram(models.Model):
    """Loyalty programs"""
    program_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    points_per_purchase = models.IntegerField(validators=[MinValueValidator(1)])
    redemption_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.program_name


class MaintenanceSchedule(models.Model):
    """Maintenance schedules"""
    schedule_name = models.CharField(max_length=255)
    frequency = models.CharField(max_length=50)
    next_maintenance_date = models.DateField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.schedule_name


class MaintenanceVisit(models.Model):
    """Maintenance visits"""
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    visit_date = models.DateField()
    technician_name = models.CharField(max_length=255)
    visit_duration_hours = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Visit - {self.visit_date}"


class Opportunity(models.Model):
    """Sales opportunities"""
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
        ('ON_HOLD', 'On Hold'),
    )
    
    opportunity_name = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    opportunity_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    probability_percentage = models.IntegerField(validators=[MinValueValidator(0)])
    expected_close_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.opportunity_name


class PointTransaction(models.Model):
    """Loyalty points transactions"""
    member_number = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=20, choices=(('EARN', 'Earn'), ('REDEEM', 'Redeem')))
    points_amount = models.IntegerField(validators=[MinValueValidator(1)])
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.member_number} - {self.transaction_type}"


class PosTransaction(models.Model):
    """POS transactions"""
    transaction_number = models.CharField(max_length=100, unique=True)
    transaction_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=50)
    items_count = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return self.transaction_number


class PromotionUsage(models.Model):
    """Promotion usage records"""
    promotion_code = models.CharField(max_length=100)
    usage_count = models.IntegerField(validators=[MinValueValidator(1)])
    last_used_date = models.DateTimeField()
    revenue_generated = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.promotion_code


class Promotion(models.Model):
    """Promotions"""
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('EXPIRED', 'Expired'),
    )
    
    promotion_code = models.CharField(max_length=100, unique=True)
    promotion_name = models.CharField(max_length=255)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    def __str__(self):
        return self.promotion_code


class Prospect(models.Model):
    """Prospects"""
    prospect_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    interest_level = models.CharField(max_length=50)
    next_contact_date = models.DateField()
    
    def __str__(self):
        return self.prospect_name


class Quote(models.Model):
    """Sales quotes"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )
    
    quote_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    quote_date = models.DateField()
    expiry_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    def __str__(self):
        return self.quote_number


class SalesPerson(models.Model):
    """Sales persons"""
    employee_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    territory = models.CharField(max_length=100)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Sales Persons"
    
    def __str__(self):
        return self.name


class SalesStage(models.Model):
    """Sales pipeline stages"""
    stage_name = models.CharField(max_length=100, unique=True)
    sequence = models.IntegerField()
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Sales Stages"
    
    def __str__(self):
        return self.stage_name


class SmsCenter(models.Model):
    """SMS management center"""
    sms_provider = models.CharField(max_length=100)
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "SMS Centers"
    
    def __str__(self):
        return self.sms_provider


class SmsLog(models.Model):
    """SMS logs"""
    recipient_number = models.CharField(max_length=20)
    message_content = models.TextField()
    sent_datetime = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "SMS Logs"
    
    def __str__(self):
        return f"SMS to {self.recipient_number}"


class SmsSettings(models.Model):
    """SMS module settings"""
    default_provider = models.CharField(max_length=100)
    max_characters_per_sms = models.IntegerField(default=160)
    auto_send_enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "SMS Settings"
    
    def __str__(self):
        return "SMS Settings"


class Territory(models.Model):
    """Sales territories"""
    territory_code = models.CharField(max_length=50, unique=True)
    territory_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    assigned_to = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Territories"
    
    def __str__(self):
        return self.territory_name


class WarrantyClaim(models.Model):
    """Warranty claims"""
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('PROCESSING', 'Processing'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    
    claim_number = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=255)
    claim_date = models.DateField()
    claim_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    
    def __str__(self):
        return self.claim_number
