from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class AuditLog(models.Model):
    """Track audit logs for accounting operations"""
    ACTION_CHOICES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
    )
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=100)
    entity_id = models.IntegerField()
    user = models.CharField(max_length=255)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} - {self.entity_type} ({self.entity_id})"


class BalanceSheet(models.Model):
    """Balance sheet records"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('FINALIZED', 'Finalized'),
        ('CLOSED', 'Closed'),
    )
    
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_equity = models.DecimalField(max_digits=15, decimal_places=2)
    prepared_by = models.CharField(max_length=255)
    prepared_date = models.DateTimeField(auto_now_add=True)
    finalized_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-period_end']
    
    def __str__(self):
        return f"Balance Sheet {self.period_start} - {self.period_end}"


class BankPaymentLine(models.Model):
    """Bank payment line details"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    reference_number = models.CharField(max_length=100, unique=True)
    payee = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reference_number} - {self.payee}"


class BankProfile(models.Model):
    """Bank account profiles"""
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
    )
    
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True)
    account_holder = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    branch_code = models.CharField(max_length=50)
    swift_code = models.CharField(max_length=11)
    iban = models.CharField(max_length=34, blank=True)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


class BankReceiptLine(models.Model):
    """Bank receipt line details"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
    )
    
    reference_number = models.CharField(max_length=100, unique=True)
    payer = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    receipt_date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reference_number} - {self.payer}"


class BankStatement(models.Model):
    """Bank statements"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RECONCILED', 'Reconciled'),
        ('APPROVED', 'Approved'),
    )
    
    bank_profile = models.ForeignKey(BankProfile, on_delete=models.CASCADE)
    statement_date = models.DateField()
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=15, decimal_places=2)
    total_deposits = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_withdrawals = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    def __str__(self):
        return f"Statement {self.bank_profile.bank_name} - {self.statement_date}"


class CapitalContribution(models.Model):
    """Capital contributions from shareholders"""
    CONTRIBUTION_TYPE = (
        ('CASH', 'Cash'),
        ('ASSET', 'Asset'),
        ('LOAN', 'Loan Conversion'),
    )
    
    contributor_name = models.CharField(max_length=255)
    contribution_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPE)
    contribution_date = models.DateField()
    description = models.TextField(blank=True)
    certificate_number = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"Capital Contribution - {self.contributor_name}"


class CashFlowForecast(models.Model):
    """Cash flow forecasts"""
    period_start = models.DateField()
    period_end = models.DateField()
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2)
    projected_inflows = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    projected_outflows = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    projected_closing = models.DecimalField(max_digits=15, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cash Flow Forecast {self.period_start} - {self.period_end}"


class CashPaymentLine(models.Model):
    """Cash payment line details"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    reference_number = models.CharField(max_length=100, unique=True)
    payee = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    voucher_number = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reference_number} - {self.payee}"


class CashReceiptLine(models.Model):
    """Cash receipt line details"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
    )
    
    reference_number = models.CharField(max_length=100, unique=True)
    payer = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    receipt_date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    receipt_number = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reference_number} - {self.payer}"


class CashTransaction(models.Model):
    """Cash transactions"""
    TRANSACTION_TYPE = (
        ('RECEIPT', 'Receipt'),
        ('PAYMENT', 'Payment'),
    )
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    reference_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    transaction_date = models.DateField()
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type} - {self.reference_number}"


class Currency(models.Model):
    """Currency definitions"""
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    is_base_currency = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Currencies"
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Customer(models.Model):
    """Customers in accounting system"""
    CUSTOMER_TYPE = (
        ('INDIVIDUAL', 'Individual'),
        ('BUSINESS', 'Business'),
    )
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class DeferredExpense(models.Model):
    """Deferred expenses"""
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    expense_date = models.DateField()
    deferral_period_months = models.IntegerField(validators=[MinValueValidator(1)])
    amortization_start_date = models.DateField()
    monthly_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"Deferred Expense - {self.description}"


class DeferredRevenue(models.Model):
    """Deferred revenues"""
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    received_date = models.DateField()
    recognition_period_months = models.IntegerField(validators=[MinValueValidator(1)])
    recognition_start_date = models.DateField()
    monthly_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"Deferred Revenue - {self.description}"


class FixedAsset(models.Model):
    """Fixed assets"""
    ASSET_TYPE = (
        ('BUILDING', 'Building'),
        ('MACHINERY', 'Machinery'),
        ('EQUIPMENT', 'Equipment'),
        ('VEHICLE', 'Vehicle'),
        ('FURNITURE', 'Furniture'),
        ('OTHER', 'Other'),
    )
    
    asset_code = models.CharField(max_length=50, unique=True)
    asset_name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    salvage_value = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    useful_life_years = models.IntegerField(validators=[MinValueValidator(1)])
    accumulated_depreciation = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.asset_code} - {self.asset_name}"


class LedgerEntry(models.Model):
    """General ledger entries"""
    ENTRY_TYPE = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )
    
    entry_number = models.CharField(max_length=100, unique=True)
    account_code = models.CharField(max_length=50)
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    entry_date = models.DateField()
    reference_document = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Entry {self.entry_number}"


class ModulePermission(models.Model):
    """Module-level permissions"""
    PERMISSION_TYPE = (
        ('VIEW', 'View'),
        ('CREATE', 'Create'),
        ('EDIT', 'Edit'),
        ('DELETE', 'Delete'),
        ('APPROVE', 'Approve'),
    )
    
    user_id = models.IntegerField()
    module_name = models.CharField(max_length=100)
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPE)
    is_granted = models.BooleanField(default=True)
    granted_by = models.CharField(max_length=255)
    granted_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.module_name} - {self.permission_type}"


class PeriodLock(models.Model):
    """Period locks for accounting"""
    lock_date = models.DateField()
    locked_by = models.CharField(max_length=255)
    reason = models.TextField(blank=True)
    is_locked = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Period Lock - {self.lock_date}"


class ProfitLossReport(models.Model):
    """Profit and loss reports"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('FINALIZED', 'Finalized'),
    )
    
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    operating_profit = models.DecimalField(max_digits=15, decimal_places=2)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2)
    prepared_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-period_end']
    
    def __str__(self):
        return f"P&L Report {self.period_start} - {self.period_end}"


class ReconciliationEntry(models.Model):
    """Reconciliation entries"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RECONCILED', 'Reconciled'),
        ('REJECTED', 'Rejected'),
    )
    
    reference_number = models.CharField(max_length=100, unique=True)
    entry_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reconciliation {self.reference_number}"


class ReconciliationMatch(models.Model):
    """Reconciliation matches between system and bank"""
    match_date = models.DateField()
    system_entry = models.CharField(max_length=100)
    bank_entry = models.CharField(max_length=100)
    matched_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    is_matched = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Match {self.system_entry} - {self.bank_entry}"


class ReconciliationRecord(models.Model):
    """Reconciliation records"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    
    reconciliation_period = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    unmatched_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    reconciliation_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Reconciliation Record - {self.reconciliation_period}"


class Shareholding(models.Model):
    """Shareholdings"""
    shareholder_name = models.CharField(max_length=255)
    number_of_shares = models.IntegerField(validators=[MinValueValidator(1)])
    share_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    acquisition_date = models.DateField()
    share_class = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.shareholder_name} - {self.number_of_shares} shares"


class Stakeholder(models.Model):
    """Stakeholders"""
    STAKEHOLDER_TYPE = (
        ('SHAREHOLDER', 'Shareholder'),
        ('CREDITOR', 'Creditor'),
        ('DEBTOR', 'Debtor'),
        ('EMPLOYEE', 'Employee'),
        ('SUPPLIER', 'Supplier'),
        ('CUSTOMER', 'Customer'),
    )
    
    name = models.CharField(max_length=255)
    stakeholder_type = models.CharField(max_length=20, choices=STAKEHOLDER_TYPE)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    outstanding_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.name} - {self.stakeholder_type}"


class TaxRate(models.Model):
    """Tax rates"""
    TAX_TYPE = (
        ('INCOME_TAX', 'Income Tax'),
        ('SALES_TAX', 'Sales Tax'),
        ('VAT', 'VAT'),
        ('PAYROLL_TAX', 'Payroll Tax'),
    )
    
    tax_code = models.CharField(max_length=50, unique=True)
    tax_name = models.CharField(max_length=255)
    tax_type = models.CharField(max_length=20, choices=TAX_TYPE)
    rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    effective_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.tax_code} - {self.rate}%"


class TaxSummary(models.Model):
    """Tax summaries"""
    period_start = models.DateField()
    period_end = models.DateField()
    tax_type = models.CharField(max_length=50)
    total_taxable_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_tax_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=(('DRAFT', 'Draft'), ('FILED', 'Filed')), default='DRAFT')
    filed_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-period_end']
    
    def __str__(self):
        return f"Tax Summary {self.tax_type} - {self.period_start} to {self.period_end}"


class TaxTransaction(models.Model):
    """Tax transactions"""
    transaction_number = models.CharField(max_length=100, unique=True)
    tax_type = models.CharField(max_length=50)
    transaction_date = models.DateField()
    taxable_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"Tax Transaction - {self.transaction_number}"


class Theme(models.Model):
    """UI Themes"""
    name = models.CharField(max_length=100)
    primary_color = models.CharField(max_length=7)  # Hex color
    secondary_color = models.CharField(max_length=7)
    accent_color = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class TrialBalance(models.Model):
    """Trial balance reports"""
    period_date = models.DateField()
    total_debits = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_credits = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    is_balanced = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-period_date']
    
    def __str__(self):
        return f"Trial Balance - {self.period_date}"


class UserEntity(models.Model):
    """User entities mapping"""
    user_id = models.IntegerField()
    entity_name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User {self.user_id} - {self.entity_name}"


class UserThemePreference(models.Model):
    """User theme preferences"""
    user_id = models.IntegerField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"User {self.user_id} - {self.theme.name}"


class VendorInvoice(models.Model):
    """Vendor invoices"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('RECEIVED', 'Received'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    
    invoice_number = models.CharField(max_length=100, unique=True)
    vendor_name = models.CharField(max_length=255)
    invoice_date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    description = models.TextField(blank=True)
    received_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.invoice_number} - {self.vendor_name}"


class VendorPayment(models.Model):
    """Vendor payments"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    payment_number = models.CharField(max_length=100, unique=True)
    vendor_invoice = models.ForeignKey(VendorInvoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.payment_number}"


class Vendor(models.Model):
    """Vendors in accounting system"""
    vendor_code = models.CharField(max_length=50, unique=True)
    vendor_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.vendor_code} - {self.vendor_name}"
