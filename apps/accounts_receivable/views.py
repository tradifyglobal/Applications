from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


class StandardPagination(PageNumberPagination):
    page_size = 50


class ARAingViewSet(viewsets.ModelViewSet):
    queryset = ARaging.objects.all()
    serializer_class = ARAingSerializer
    pagination_class = StandardPagination


class ARDiscountViewSet(viewsets.ModelViewSet):
    queryset = ARDiscount.objects.all()
    serializer_class = ARDiscountSerializer
    pagination_class = StandardPagination


class ARReconciliationViewSet(viewsets.ModelViewSet):
    queryset = ARReconciliation.objects.all()
    serializer_class = ARReconciliationSerializer
    pagination_class = StandardPagination


class ARSettingsViewSet(viewsets.ModelViewSet):
    queryset = ARSettings.objects.all()
    serializer_class = ARSettingsSerializer
    pagination_class = StandardPagination


class CustomerInvoiceViewSet(viewsets.ModelViewSet):
    queryset = CustomerInvoice.objects.all()
    serializer_class = CustomerInvoiceSerializer
    pagination_class = StandardPagination


class CustomerPaymentViewSet(viewsets.ModelViewSet):
    queryset = CustomerPayment.objects.all()
    serializer_class = CustomerPaymentSerializer
    pagination_class = StandardPagination


class InvoiceLineItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceLineItem.objects.all()
    serializer_class = InvoiceLineItemSerializer
    pagination_class = StandardPagination
