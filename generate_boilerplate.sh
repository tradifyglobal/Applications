#!/bin/bash
# Generate boilerplate files for all ERP modules

# Module list
modules=(
  "accounting"
  "accounts_receivable"
  "accounts_payable"
  "authentication"
  "cash_management"
  "crm"
  "employee_expenses"
  "manufacturing"
  "project_management"
  "site_maintenance"
  "sites"
  "social_auth"
)

# Also need to update existing modules
existing_modules=(
  "finance"
  "hr"
  "inventory"
  "maintenance"
  "production"
  "procurement"
  "quality"
  "sales"
)

# Create boilerplate for new modules
for module in "${modules[@]}"; do
  module_path="apps/$module"
  
  # Create __init__.py if it doesn't exist
  if [ ! -f "$module_path/__init__.py" ]; then
    touch "$module_path/__init__.py"
  fi
  
  # Create apps.py
  cat > "$module_path/apps.py" << 'EOF'
from django.apps import AppConfig


class ${ModuleNameConfig}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.${modulename}'
    verbose_name = '${Module Name}'
EOF

  # Create serializers.py
  cat > "$module_path/serializers.py" << 'EOF'
from rest_framework import serializers
from .models import *


# Import all models from this module
# Create serializers for each model following DRY principle
EOF

  # Create views.py
  cat > "$module_path/views.py" << 'EOF'
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Create ViewSets for each model
EOF

  # Create urls.py
  cat > "$module_path/urls.py" << 'EOF'
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = '${modulename}'

router = DefaultRouter()
# Register viewsets here

urlpatterns = [
    path('', include(router.urls)),
]
EOF

  # Create admin.py
  cat > "$module_path/admin.py" << 'EOF'
from django.contrib import admin
from .models import *


# Register all models here
EOF

  echo "Created boilerplate for $module"
done

echo "Boilerplate generation completed!"
