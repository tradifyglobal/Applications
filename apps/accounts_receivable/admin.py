from django.contrib import admin
from .models import ARaging, ARDiscount, ARReconciliation, ARSettings, CustomerInvoice, CustomerPayment, InvoiceLineItem


@admin.register(ARaging)
class ARAingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'total_outstanding', 'report_date')
    list_filter = ('report_date',)
    search_fields = ('customer_name',)


@admin.register(ARDiscount)
class ARDiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_code', 'discount_type', 'discount_percentage')
    list_filter = ('discount_type',)
    search_fields = ('discount_code',)


@admin.register(ARReconciliation)
class ARReconciliationAdmin(admin.ModelAdmin):
    list_display = ('reconciliation_period', 'status', 'total_invoices', 'total_payments')
    list_filter = ('status',)
    search_fields = ('reconciliation_period',)


@admin.register(ARSettings)
class ARSettingsAdmin(admin.ModelAdmin):
    list_display = ('auto_invoice_enabled', 'default_payment_terms_days', 'updated_date')


@admin.register(CustomerInvoice)
class CustomerInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer_name', 'invoice_date', 'invoice_amount', 'status')
    list_filter = ('status', 'invoice_date')
    search_fields = ('invoice_number', 'customer_name')


@admin.register(CustomerPayment)
class CustomerPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'customer_invoice', 'payment_amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('payment_number',)


@admin.register(InvoiceLineItem)
class InvoiceLineItemAdmin(admin.ModelAdmin):
    list_display = ('customer_invoice', 'description', 'quantity', 'unit_price', 'line_total')
    search_fields = ('description',)
