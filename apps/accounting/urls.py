from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'accounting'

router = DefaultRouter()
router.register(r'audit-logs', views.AuditLogViewSet, basename='auditlog')
router.register(r'balance-sheets', views.BalanceSheetViewSet, basename='balancesheet')
router.register(r'bank-payment-lines', views.BankPaymentLineViewSet, basename='bankpaymentline')
router.register(r'bank-profiles', views.BankProfileViewSet, basename='bankprofile')
router.register(r'bank-receipt-lines', views.BankReceiptLineViewSet, basename='bankreceiptline')
router.register(r'bank-statements', views.BankStatementViewSet, basename='bankstatement')
router.register(r'capital-contributions', views.CapitalContributionViewSet, basename='capitalcontribution')
router.register(r'cash-flow-forecasts', views.CashFlowForecastViewSet, basename='cashflowforecast')
router.register(r'cash-payment-lines', views.CashPaymentLineViewSet, basename='cashpaymentline')
router.register(r'cash-receipt-lines', views.CashReceiptLineViewSet, basename='cashreceiptline')
router.register(r'cash-transactions', views.CashTransactionViewSet, basename='cashtransaction')
router.register(r'currencies', views.CurrencyViewSet, basename='currency')
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'deferred-expenses', views.DeferredExpenseViewSet, basename='deferredexpense')
router.register(r'deferred-revenues', views.DeferredRevenueViewSet, basename='deferredrevenue')
router.register(r'fixed-assets', views.FixedAssetViewSet, basename='fixedasset')
router.register(r'ledger-entries', views.LedgerEntryViewSet, basename='ledgerentry')
router.register(r'module-permissions', views.ModulePermissionViewSet, basename='modulepermission')
router.register(r'period-locks', views.PeriodLockViewSet, basename='periodlock')
router.register(r'profit-loss-reports', views.ProfitLossReportViewSet, basename='profitlossreport')
router.register(r'reconciliation-entries', views.ReconciliationEntryViewSet, basename='reconciliationentry')
router.register(r'reconciliation-matches', views.ReconciliationMatchViewSet, basename='reconciliationmatch')
router.register(r'reconciliation-records', views.ReconciliationRecordViewSet, basename='reconciliationrecord')
router.register(r'shareholdings', views.ShareholdingViewSet, basename='shareholding')
router.register(r'stakeholders', views.StakeholderViewSet, basename='stakeholder')
router.register(r'tax-rates', views.TaxRateViewSet, basename='taxrate')
router.register(r'tax-summaries', views.TaxSummaryViewSet, basename='taxsummary')
router.register(r'tax-transactions', views.TaxTransactionViewSet, basename='taxtransaction')
router.register(r'themes', views.ThemeViewSet, basename='theme')
router.register(r'trial-balances', views.TrialBalanceViewSet, basename='trialbalance')
router.register(r'user-entities', views.UserEntityViewSet, basename='userentity')
router.register(r'user-theme-preferences', views.UserThemePreferenceViewSet, basename='userthemepreference')
router.register(r'vendor-invoices', views.VendorInvoiceViewSet, basename='vendorinvoice')
router.register(r'vendor-payments', views.VendorPaymentViewSet, basename='vendorpayment')
router.register(r'vendors', views.VendorViewSet, basename='vendor')

urlpatterns = [
    path('', include(router.urls)),
]
