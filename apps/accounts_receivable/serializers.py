from rest_framework import serializers
from .models import *


class ARAingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARaging
        fields = '__all__'


class ARDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARDiscount
        fields = '__all__'


class ARReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARReconciliation
        fields = '__all__'


class ARSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARSettings
        fields = '__all__'


class CustomerInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInvoice
        fields = '__all__'


class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPayment
        fields = '__all__'


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = '__all__'
