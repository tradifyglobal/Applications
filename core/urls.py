"""
URL configuration for ERP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from . import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app import views
    2. Add a URL to urlpatterns:  path('', views.Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core API URLs
    path('api/accounting/', include('apps.accounting.urls', namespace='accounting')),
    path('api/authentication/', include('apps.authentication.urls', namespace='authentication')),
    path('api/sites/', include('apps.sites.urls', namespace='sites')),
    path('api/dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    
    # Financial APIs
    path('api/accounts-receivable/', include('apps.accounts_receivable.urls', namespace='accounts_receivable')),
    path('api/accounts-payable/', include('apps.accounts_payable.urls', namespace='accounts_payable')),
    path('api/cash-management/', include('apps.cash_management.urls', namespace='cash_management')),
    
    # Operations APIs
    path('api/inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('api/procurement/', include('apps.procurement.urls', namespace='procurement')),
    path('api/manufacturing/', include('apps.manufacturing.urls', namespace='manufacturing')),
    
    # HR & Expenses APIs
    path('api/hr/', include('apps.hr.urls', namespace='hr')),
    path('api/employee-expenses/', include('apps.employee_expenses.urls', namespace='employee_expenses')),
    
    # Sales & CRM APIs
    path('api/sales/', include('apps.sales.urls', namespace='sales')),
    path('api/crm/', include('apps.crm.urls', namespace='crm')),
    
    # Project & Maintenance APIs
    path('api/project-management/', include('apps.project_management.urls', namespace='project_management')),
    path('api/site-maintenance/', include('apps.site_maintenance.urls', namespace='site_maintenance')),
    
    # Social APIs
    path('api/social-auth/', include('apps.social_auth.urls', namespace='social_auth')),
    
    # Legacy APIs (kept for backward compatibility)
    path('api/production/', include('apps.production.urls', namespace='production')),
    path('api/quality/', include('apps.quality.urls', namespace='quality')),
    path('api/maintenance/', include('apps.maintenance.urls', namespace='maintenance')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
