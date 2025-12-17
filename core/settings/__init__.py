"""
Settings package for ERP project.
Dynamically loads settings based on ENVIRONMENT variable.
"""

import os
from decouple import config

# Get environment from environment variable
ENVIRONMENT = config('ENVIRONMENT', default='development')

# Import the appropriate settings module
if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'staging':
    from .staging import *
else:
    # Default to development
    from .development import *

__all__ = ['ENVIRONMENT']
