from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'entity_type', 'user']
    search_fields = ['entity_type', 'user']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']


class BalanceSheetViewSet(viewsets.ModelViewSet):
    queryset = BalanceSheet.objects.all()
    serializer_class = BalanceSheetSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['period_end']
    ordering = ['-period_end']


class BankPaymentLineViewSet(viewsets.ModelViewSet):
    queryset = BankPaymentLine.objects.all()
    serializer_class = BankPaymentLineSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['reference_number', 'payee']
    ordering_fields = ['payment_date']


class BankProfileViewSet(viewsets.ModelViewSet):
    queryset = BankProfile.objects.all()
    serializer_class = BankProfileSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['currency', 'is_active']
    search_fields = ['bank_name', 'account_number']


class BankReceiptLineViewSet(viewsets.ModelViewSet):
    queryset = BankReceiptLine.objects.all()
    serializer_class = BankReceiptLineSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['reference_number', 'payer']
    ordering_fields = ['receipt_date']


class BankStatementViewSet(viewsets.ModelViewSet):
    queryset = BankStatement.objects.all()
    serializer_class = BankStatementSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['statement_date']


class CapitalContributionViewSet(viewsets.ModelViewSet):
    queryset = CapitalContribution.objects.all()
    serializer_class = CapitalContributionSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['contribution_type']
    search_fields = ['contributor_name']


class CashFlowForecastViewSet(viewsets.ModelViewSet):
    queryset = CashFlowForecast.objects.all()
    serializer_class = CashFlowForecastSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['period_end']


class CashPaymentLineViewSet(viewsets.ModelViewSet):
    queryset = CashPaymentLine.objects.all()
    serializer_class = CashPaymentLineSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['reference_number', 'payee']


class CashReceiptLineViewSet(viewsets.ModelViewSet):
    queryset = CashReceiptLine.objects.all()
    serializer_class = CashReceiptLineSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['reference_number', 'payer']


class CashTransactionViewSet(viewsets.ModelViewSet):
    queryset = CashTransaction.objects.all()
    serializer_class = CashTransactionSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['transaction_type']
    search_fields = ['reference_number']


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_base_currency']
    search_fields = ['code', 'name']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['customer_type', 'is_active']
    search_fields = ['code', 'name', 'email']


class DeferredExpenseViewSet(viewsets.ModelViewSet):
    queryset = DeferredExpense.objects.all()
    serializer_class = DeferredExpenseSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['description']


class DeferredRevenueViewSet(viewsets.ModelViewSet):
    queryset = DeferredRevenue.objects.all()
    serializer_class = DeferredRevenueSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['description']


class FixedAssetViewSet(viewsets.ModelViewSet):
    queryset = FixedAsset.objects.all()
    serializer_class = FixedAssetSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['asset_type']
    search_fields = ['asset_code', 'asset_name']


class LedgerEntryViewSet(viewsets.ModelViewSet):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['entry_type']
    search_fields = ['entry_number', 'account_code']


class ModulePermissionViewSet(viewsets.ModelViewSet):
    queryset = ModulePermission.objects.all()
    serializer_class = ModulePermissionSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['module_name', 'permission_type', 'is_granted']


class PeriodLockViewSet(viewsets.ModelViewSet):
    queryset = PeriodLock.objects.all()
    serializer_class = PeriodLockSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_locked']
    ordering_fields = ['lock_date']


class ProfitLossReportViewSet(viewsets.ModelViewSet):
    queryset = ProfitLossReport.objects.all()
    serializer_class = ProfitLossReportSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['period_end']


class ReconciliationEntryViewSet(viewsets.ModelViewSet):
    queryset = ReconciliationEntry.objects.all()
    serializer_class = ReconciliationEntrySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['reference_number']


class ReconciliationMatchViewSet(viewsets.ModelViewSet):
    queryset = ReconciliationMatch.objects.all()
    serializer_class = ReconciliationMatchSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_matched']


class ReconciliationRecordViewSet(viewsets.ModelViewSet):
    queryset = ReconciliationRecord.objects.all()
    serializer_class = ReconciliationRecordSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['reconciliation_period']


class ShareholdingViewSet(viewsets.ModelViewSet):
    queryset = Shareholding.objects.all()
    serializer_class = ShareholdingSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['shareholder_name']


class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['stakeholder_type']
    search_fields = ['name', 'email']


class TaxRateViewSet(viewsets.ModelViewSet):
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tax_type']
    search_fields = ['tax_code']


class TaxSummaryViewSet(viewsets.ModelViewSet):
    queryset = TaxSummary.objects.all()
    serializer_class = TaxSummarySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'tax_type']
    ordering_fields = ['period_end']


class TaxTransactionViewSet(viewsets.ModelViewSet):
    queryset = TaxTransaction.objects.all()
    serializer_class = TaxTransactionSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tax_type']
    search_fields = ['transaction_number']


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']


class TrialBalanceViewSet(viewsets.ModelViewSet):
    queryset = TrialBalance.objects.all()
    serializer_class = TrialBalanceSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_balanced']
    ordering_fields = ['period_date']


class UserEntityViewSet(viewsets.ModelViewSet):
    queryset = UserEntity.objects.all()
    serializer_class = UserEntitySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_default']
    search_fields = ['entity_name']


class UserThemePreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserThemePreference.objects.all()
    serializer_class = UserThemePreferenceSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dark_mode']


class VendorInvoiceViewSet(viewsets.ModelViewSet):
    queryset = VendorInvoice.objects.all()
    serializer_class = VendorInvoiceSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['invoice_number', 'vendor_name']


class VendorPaymentViewSet(viewsets.ModelViewSet):
    queryset = VendorPayment.objects.all()
    serializer_class = VendorPaymentSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['payment_date']


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['vendor_code', 'vendor_name', 'email']
