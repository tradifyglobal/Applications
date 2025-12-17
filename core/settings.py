"""
Django settings for ERP project.

This file imports from the appropriate environment-specific settings module.
Set ENVIRONMENT environment variable to: development, staging, or production
Default is 'development'.

Usage:
    export ENVIRONMENT=production  # or staging, or development
    python manage.py runserver
"""

# Import all settings from the appropriate environment module
# The settings package's __init__.py handles the dynamic loading
from core.settings import *  # noqa
