from django.contrib import admin
from .models import (
    AuditLog, BalanceSheet, BankPaymentLine, BankProfile, BankReceiptLine,
    BankStatement, CapitalContribution, CashFlowForecast, CashPaymentLine,
    CashReceiptLine, CashTransaction, Currency, Customer, DeferredExpense,
    DeferredRevenue, FixedAsset, LedgerEntry, ModulePermission, PeriodLock,
    ProfitLossReport, ReconciliationEntry, ReconciliationMatch, ReconciliationRecord,
    Shareholding, Stakeholder, TaxRate, TaxSummary, TaxTransaction, Theme,
    TrialBalance, UserEntity, UserThemePreference, VendorInvoice, VendorPayment, Vendor
)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'entity_type', 'entity_id', 'user', 'timestamp')
    list_filter = ('action', 'entity_type', 'timestamp')
    search_fields = ('user', 'entity_type')


@admin.register(BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = ('period_start', 'period_end', 'status', 'total_assets', 'total_equity')
    list_filter = ('status', 'period_end')
    search_fields = ('prepared_by',)


@admin.register(BankPaymentLine)
class BankPaymentLineAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'payee', 'amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('reference_number', 'payee')


@admin.register(BankProfile)
class BankProfileAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'currency', 'current_balance', 'is_active')
    list_filter = ('currency', 'is_active')
    search_fields = ('bank_name', 'account_number')


@admin.register(BankReceiptLine)
class BankReceiptLineAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'payer', 'amount', 'receipt_date', 'status')
    list_filter = ('status', 'receipt_date')
    search_fields = ('reference_number', 'payer')


@admin.register(BankStatement)
class BankStatementAdmin(admin.ModelAdmin):
    list_display = ('bank_profile', 'statement_date', 'opening_balance', 'closing_balance', 'status')
    list_filter = ('status', 'statement_date')
    search_fields = ('bank_profile__bank_name',)


@admin.register(CapitalContribution)
class CapitalContributionAdmin(admin.ModelAdmin):
    list_display = ('contributor_name', 'contribution_amount', 'contribution_type', 'contribution_date')
    list_filter = ('contribution_type', 'contribution_date')
    search_fields = ('contributor_name',)


@admin.register(CashFlowForecast)
class CashFlowForecastAdmin(admin.ModelAdmin):
    list_display = ('period_start', 'period_end', 'projected_inflows', 'projected_outflows', 'projected_closing')
    list_filter = ('period_start', 'period_end')


@admin.register(CashPaymentLine)
class CashPaymentLineAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'payee', 'amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('reference_number', 'payee')


@admin.register(CashReceiptLine)
class CashReceiptLineAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'payer', 'amount', 'receipt_date', 'status')
    list_filter = ('status', 'receipt_date')
    search_fields = ('reference_number', 'payer')


@admin.register(CashTransaction)
class CashTransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'transaction_type', 'amount', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('reference_number',)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'exchange_rate', 'is_base_currency')
    list_filter = ('is_base_currency',)
    search_fields = ('code', 'name')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'customer_type', 'email', 'is_active')
    list_filter = ('customer_type', 'is_active')
    search_fields = ('code', 'name', 'email')


@admin.register(DeferredExpense)
class DeferredExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'expense_date', 'deferral_period_months')
    list_filter = ('expense_date',)
    search_fields = ('description',)


@admin.register(DeferredRevenue)
class DeferredRevenueAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'received_date', 'recognition_period_months')
    list_filter = ('received_date',)
    search_fields = ('description',)


@admin.register(FixedAsset)
class FixedAssetAdmin(admin.ModelAdmin):
    list_display = ('asset_code', 'asset_name', 'asset_type', 'purchase_date', 'purchase_cost')
    list_filter = ('asset_type', 'purchase_date')
    search_fields = ('asset_code', 'asset_name')


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('entry_number', 'account_code', 'entry_type', 'amount', 'entry_date')
    list_filter = ('entry_type', 'entry_date')
    search_fields = ('entry_number', 'account_code')


@admin.register(ModulePermission)
class ModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'permission_type', 'user_id', 'is_granted', 'granted_date')
    list_filter = ('permission_type', 'is_granted', 'granted_date')
    search_fields = ('module_name',)


@admin.register(PeriodLock)
class PeriodLockAdmin(admin.ModelAdmin):
    list_display = ('lock_date', 'locked_by', 'is_locked', 'created_date')
    list_filter = ('is_locked', 'lock_date')
    search_fields = ('locked_by',)


@admin.register(ProfitLossReport)
class ProfitLossReportAdmin(admin.ModelAdmin):
    list_display = ('period_start', 'period_end', 'status', 'total_revenue', 'net_profit')
    list_filter = ('status', 'period_end')


@admin.register(ReconciliationEntry)
class ReconciliationEntryAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'entry_date', 'amount', 'status')
    list_filter = ('status', 'entry_date')
    search_fields = ('reference_number',)


@admin.register(ReconciliationMatch)
class ReconciliationMatchAdmin(admin.ModelAdmin):
    list_display = ('match_date', 'system_entry', 'bank_entry', 'matched_amount', 'is_matched')
    list_filter = ('is_matched', 'match_date')


@admin.register(ReconciliationRecord)
class ReconciliationRecordAdmin(admin.ModelAdmin):
    list_display = ('reconciliation_period', 'status', 'total_amount', 'unmatched_amount')
    list_filter = ('status', 'reconciliation_date')
    search_fields = ('reconciliation_period',)


@admin.register(Shareholding)
class ShareholdingAdmin(admin.ModelAdmin):
    list_display = ('shareholder_name', 'number_of_shares', 'share_percentage', 'acquisition_date')
    list_filter = ('acquisition_date',)
    search_fields = ('shareholder_name',)


@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ('name', 'stakeholder_type', 'email', 'outstanding_amount')
    list_filter = ('stakeholder_type',)
    search_fields = ('name', 'email')


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ('tax_code', 'tax_type', 'rate', 'effective_date')
    list_filter = ('tax_type', 'effective_date')
    search_fields = ('tax_code',)


@admin.register(TaxSummary)
class TaxSummaryAdmin(admin.ModelAdmin):
    list_display = ('period_start', 'period_end', 'tax_type', 'total_tax_amount', 'status')
    list_filter = ('status', 'tax_type', 'period_end')


@admin.register(TaxTransaction)
class TaxTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_number', 'tax_type', 'transaction_date', 'tax_amount')
    list_filter = ('tax_type', 'transaction_date')
    search_fields = ('transaction_number',)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_color', 'secondary_color', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(TrialBalance)
class TrialBalanceAdmin(admin.ModelAdmin):
    list_display = ('period_date', 'total_debits', 'total_credits', 'is_balanced')
    list_filter = ('is_balanced', 'period_date')


@admin.register(UserEntity)
class UserEntityAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'entity_name', 'is_default', 'assigned_date')
    list_filter = ('is_default',)
    search_fields = ('entity_name',)


@admin.register(UserThemePreference)
class UserThemePreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'theme', 'dark_mode', 'updated_date')
    list_filter = ('dark_mode',)


@admin.register(VendorInvoice)
class VendorInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'vendor_name', 'invoice_date', 'amount', 'status')
    list_filter = ('status', 'invoice_date')
    search_fields = ('invoice_number', 'vendor_name')


@admin.register(VendorPayment)
class VendorPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'vendor_invoice', 'amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('payment_number',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_code', 'vendor_name', 'email', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('vendor_code', 'vendor_name', 'email')
