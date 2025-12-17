from django.db import models
from django.core.validators import MinValueValidator


class CashFlowForecastDetail(models.Model):
    """Cash flow forecast details"""
    forecast_date = models.DateField()
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2)
    projected_inflows = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    projected_outflows = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    closing_balance = models.DecimalField(max_digits=15, decimal_places=2)
    confidence_level = models.IntegerField(default=80, validators=[MinValueValidator(0)])  # Percentage
    
    def __str__(self):
        return f"Cash Flow Detail - {self.forecast_date}"


class CashManagementSettings(models.Model):
    """Cash management module settings"""
    auto_reconciliation_enabled = models.BooleanField(default=True)
    cash_low_threshold = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_high_threshold = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    auto_transfer_enabled = models.BooleanField(default=False)
    auto_transfer_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Cash Management Settings"
    
    def __str__(self):
        return "Cash Management Settings"


class CashPosition(models.Model):
    """Cash positions by account"""
    account_name = models.CharField(max_length=255)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_deposits = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_withdrawals = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    as_of_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.account_name} - {self.as_of_date}"


class FxExposure(models.Model):
    """Foreign exchange exposures"""
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_rate = models.DecimalField(max_digits=10, decimal_places=4)
    home_currency_equivalent = models.DecimalField(max_digits=15, decimal_places=2)
    risk_level = models.CharField(max_length=20, choices=(('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')))
    as_of_date = models.DateField()
    
    class Meta:
        verbose_name_plural = "FX Exposures"
    
    def __str__(self):
        return f"FX {self.currency} - {self.amount}"


class LiquidityForecastLine(models.Model):
    """Liquidity forecast line items"""
    forecast_date = models.DateField()
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.category} - {self.forecast_date}"


class LiquidityForecast(models.Model):
    """Liquidity forecasts"""
    period_start = models.DateField()
    period_end = models.DateField()
    total_liquidity = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    required_reserve = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    available_liquidity = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"Liquidity Forecast {self.period_start} - {self.period_end}"


class PaymentSchedule(models.Model):
    """Payment schedules"""
    description = models.CharField(max_length=255)
    scheduled_date = models.DateField()
    scheduled_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=(('PENDING', 'Pending'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled')))
    
    def __str__(self):
        return f"{self.description} - {self.scheduled_date}"


class TreasuryAccount(models.Model):
    """Treasury accounts"""
    account_code = models.CharField(max_length=50, unique=True)
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=3)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.account_code} - {self.account_name}"
