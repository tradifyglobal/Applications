"""Fast module generator for ERP system"""
import os

modules_config = {
    'accounts_payable': {
        'models': ['APAging', 'APDiscount', 'APReconciliation', 'APSettings', 'VendorBill', 'VendorBillLineItem', 'VendorPayment'],
        'verbose': 'Accounts Payable'
    },
    'authentication': {
        'models': ['Group', 'User'],
        'verbose': 'Authentication'
    },
    'cash_management': {
        'models': ['CashFlowForecastDetail', 'CashManagementSettings', 'CashPosition', 'FxExposure', 'LiquidityForecastLine', 'LiquidityForecast', 'PaymentSchedule', 'TreasuryAccount'],
        'verbose': 'Cash Management'
    },
    'crm': {
        'models': ['Activity', 'Appointment', 'Campaign', 'Contact', 'Lead', 'Opportunity', 'Quote'],
        'verbose': 'CRM'
    },
    'employee_expenses': {
        'models': ['EmployeeExpenseReport', 'EmployeeExpense', 'ExpenseBudget', 'ExpenseCategory', 'ExpenseReimbursement'],
        'verbose': 'Employee Expenses'
    },
    'manufacturing': {
        'models': ['Product', 'ProductionOrder', 'Equipment', 'WorkCenter', 'BillOfMaterial'],
        'verbose': 'Manufacturing'
    },
    'project_management': {
        'models': ['Project', 'Task', 'ProjectBudget', 'ResourceAllocation', 'TimeEntry'],
        'verbose': 'Project Management'
    },
    'site_maintenance': {
        'models': ['WorkOrder', 'MaintenanceTask', 'MaintenanceAsset', 'SparePart'],
        'verbose': 'Site Maintenance'
    },
    'sites': {
        'models': ['Site'],
        'verbose': 'Sites'
    },
    'social_auth': {
        'models': ['SocialAccount', 'SocialApplication', 'SocialApplicationToken'],
        'verbose': 'Social Auth'
    },
}


def create_apps_py(module_name, verbose_name):
    """Create apps.py"""
    config_class = ''.join(w.capitalize() for w in module_name.split('_')) + 'Config'
    return f"""from django.apps import AppConfig


class {config_class}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{module_name}'
    verbose_name = '{verbose_name}'
"""


def create_serializers_py(models):
    """Create serializers.py"""
    content = """from rest_framework import serializers
from .models import *

"""
    for model in models:
        content += f"""
class {model}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model}
        fields = '__all__'
"""
    return content


def create_views_py(models):
    """Create views.py"""
    content = """from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


class StandardPagination(PageNumberPagination):
    page_size = 50


"""
    for model in models:
        content += f"""
class {model}ViewSet(viewsets.ModelViewSet):
    queryset = {model}.objects.all()
    serializer_class = {model}Serializer
    pagination_class = StandardPagination
"""
    return content


def create_urls_py(module_name, models):
    """Create urls.py"""
    content = f"""from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = '{module_name}'

router = DefaultRouter()
"""
    for model in models:
        route = '-'.join([c.lower() if i == 0 else c.lower() for i, c in enumerate(model)]).replace('-', '-')
        route = ''.join(['-' + c.lower() if c.isupper() else c for c in model]).lstrip('-') + 's'
        viewset = f'{model}ViewSet'
        basename = model.lower()
        content += f"router.register(r'{route}', views.{viewset}, basename='{basename}')\n"
    
    content += """
urlpatterns = [
    path('', include(router.urls)),
]
"""
    return content


print("Module boilerplate generator created successfully!")
