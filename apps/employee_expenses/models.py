from django.db import models
from django.core.validators import MinValueValidator


class EmployeeExpenseReport(models.Model):
    """Employee expense reports"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REIMBURSED', 'Reimbursed'),
    )
    
    report_number = models.CharField(max_length=100, unique=True)
    employee_name = models.CharField(max_length=255)
    report_period_start = models.DateField()
    report_period_end = models.DateField()
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    submitted_date = models.DateField(null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    reimbursed_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.report_number


class EmployeeExpense(models.Model):
    """Employee expenses"""
    EXPENSE_CATEGORY_CHOICES = (
        ('TRAVEL', 'Travel'),
        ('MEALS', 'Meals'),
        ('ACCOMMODATION', 'Accommodation'),
        ('OFFICE', 'Office'),
        ('EQUIPMENT', 'Equipment'),
        ('OTHER', 'Other'),
    )
    
    expense_report = models.ForeignKey(EmployeeExpenseReport, on_delete=models.CASCADE, related_name='expenses')
    expense_date = models.DateField()
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=50)
    receipt_attached = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.category} - {self.description}"


class ExpenseApprovalWorkflow(models.Model):
    """Expense approval workflows"""
    workflow_name = models.CharField(max_length=255)
    approval_levels = models.IntegerField(validators=[MinValueValidator(1)])
    approvers = models.JSONField(help_text="List of approver emails")
    minimum_approval_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.workflow_name


class ExpenseBudget(models.Model):
    """Expense budgets"""
    fiscal_year = models.IntegerField()
    category = models.CharField(max_length=100)
    budgeted_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    spent_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.fiscal_year} - {self.category}"


class ExpenseCategory(models.Model):
    """Expense categories"""
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    requires_approval = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Expense Categories"
    
    def __str__(self):
        return self.category_name


class ExpenseReimbursement(models.Model):
    """Expense reimbursements"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    
    reimbursement_number = models.CharField(max_length=100, unique=True)
    expense_report = models.ForeignKey(EmployeeExpenseReport, on_delete=models.CASCADE)
    reimbursement_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.reimbursement_number
