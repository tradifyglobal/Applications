from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'accounts_receivable'

router = DefaultRouter()
router.register(r'ar-agings', views.ARAingViewSet, basename='araing')
router.register(r'ar-discounts', views.ARDiscountViewSet, basename='ardiscount')
router.register(r'ar-reconciliations', views.ARReconciliationViewSet, basename='arreconciliation')
router.register(r'ar-settings', views.ARSettingsViewSet, basename='arsettings')
router.register(r'customer-invoices', views.CustomerInvoiceViewSet, basename='customerinvoice')
router.register(r'customer-payments', views.CustomerPaymentViewSet, basename='customerpayment')
router.register(r'invoice-line-items', views.InvoiceLineItemViewSet, basename='invoicelineitem')

urlpatterns = [
    path('', include(router.urls)),
]
