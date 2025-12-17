from rest_framework import serializers
from .models import *


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'


class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheet
        fields = '__all__'


class BankPaymentLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankPaymentLine
        fields = '__all__'


class BankProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankProfile
        fields = '__all__'


class BankReceiptLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankReceiptLine
        fields = '__all__'


class BankStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankStatement
        fields = '__all__'


class CapitalContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapitalContribution
        fields = '__all__'


class CashFlowForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowForecast
        fields = '__all__'


class CashPaymentLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashPaymentLine
        fields = '__all__'


class CashReceiptLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashReceiptLine
        fields = '__all__'


class CashTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashTransaction
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class DeferredExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeferredExpense
        fields = '__all__'


class DeferredRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeferredRevenue
        fields = '__all__'


class FixedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedAsset
        fields = '__all__'


class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerEntry
        fields = '__all__'


class ModulePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulePermission
        fields = '__all__'


class PeriodLockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodLock
        fields = '__all__'


class ProfitLossReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitLossReport
        fields = '__all__'


class ReconciliationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationEntry
        fields = '__all__'


class ReconciliationMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationMatch
        fields = '__all__'


class ReconciliationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationRecord
        fields = '__all__'


class ShareholdingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shareholding
        fields = '__all__'


class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = '__all__'


class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRate
        fields = '__all__'


class TaxSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxSummary
        fields = '__all__'


class TaxTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxTransaction
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class TrialBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrialBalance
        fields = '__all__'


class UserEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntity
        fields = '__all__'


class UserThemePreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserThemePreference
        fields = '__all__'


class VendorInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorInvoice
        fields = '__all__'


class VendorPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPayment
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
