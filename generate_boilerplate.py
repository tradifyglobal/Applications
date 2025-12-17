"""
Script to generate boilerplate files for all ERP modules.
This script creates apps.py, serializers.py, views.py, urls.py, admin.py, and __init__.py
for each module based on their models.
"""

import os
import sys
from django.apps import apps as django_apps

# Module configurations
MODULES = {
    'accounts_receivable': ['ARaging', 'ARDiscount', 'ARReconciliation', 'ARSettings', 'CustomerInvoice', 'CustomerPayment', 'InvoiceLineItem'],
    'accounts_payable': ['APAging', 'APDiscount', 'APReconciliation', 'APSettings', 'VendorBill', 'VendorBillLineItem', 'VendorPayment'],
    'authentication': ['Group', 'User'],
    'cash_management': ['CashFlowForecastDetail', 'CashManagementSettings', 'CashPosition', 'FxExposure', 'LiquidityForecastLine', 'LiquidityForecast', 'PaymentSchedule', 'TreasuryAccount'],
    'crm': ['Activity', 'Appointment', 'Campaign', 'Communication', 'Contact', 'Contract', 'CrmSettings', 'CustomerGroup', 'CustomerSegment', 'EmailCampaign', 'EmailGroup', 'LeadSource', 'Lead', 'LoyaltyMember', 'LoyaltyProgram', 'MaintenanceSchedule', 'MaintenanceVisit', 'Opportunity', 'PointTransaction', 'PosTransaction', 'PromotionUsage', 'Promotion', 'Prospect', 'Quote', 'SalesPerson', 'SalesStage', 'SmsCenter', 'SmsLog', 'SmsSettings', 'Territory', 'WarrantyClaim'],
    'employee_expenses': ['EmployeeExpenseReport', 'EmployeeExpense', 'ExpenseApprovalWorkflow', 'ExpenseBudget', 'ExpenseCategory', 'ExpenseReimbursement'],
    'manufacturing': ['AfterSalesService', 'BillOfMaterial', 'Courier', 'DistributorContact', 'DistributorOrder', 'DistributorPerformance', 'Distributor', 'Equipment', 'OrderShipment', 'ProductCategory', 'ProductionOrder', 'Product', 'QualityInspection', 'RawMaterial', 'Routing', 'ServiceActivity', 'WarrantyRegistration', 'WorkCenter'],
    'project_management': ['ProjectBudget', 'ProjectKPI', 'ProjectPhase', 'ProjectSettings', 'Project', 'ResourceAllocation', 'Task', 'TimeEntry'],
    'site_maintenance': ['ComplianceAudit', 'ComplianceStandard', 'DowntimeRecord', 'MaintenanceAsset', 'MaintenanceCost', 'MaintenanceTask', 'MaintenanceVendor', 'SparePart', 'VendorContract', 'WorkOrderSparePart', 'WorkOrder'],
    'sites': ['Site'],
    'social_auth': ['SocialAccount', 'SocialApplicationToken', 'SocialApplication'],
}

def generate_files():
    """Generate all boilerplate files for modules"""
    for module_name in MODULES.keys():
        module_path = f'apps/{module_name}'
        
        # Create __init__.py
        init_file = f'{module_path}/__init__.py'
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('')
        
        # Create apps.py
        config_name = ''.join(word.capitalize() for word in module_name.split('_')) + 'Config'
        with open(f'{module_path}/apps.py', 'w') as f:
            f.write(f"""from django.apps import AppConfig


class {config_name}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{module_name}'
    verbose_name = '{module_name.replace('_', ' ').title()}'
""")
        
        print(f"Generated apps.py for {module_name}")

if __name__ == '__main__':
    generate_files()
    print("Boilerplate generation completed!")
