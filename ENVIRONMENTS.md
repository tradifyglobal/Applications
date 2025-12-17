# Multi-Environment Configuration Guide

## Overview

The ERP application now supports three distinct environments:
- **Development**: For local development with relaxed security settings
- **Staging**: Pre-production environment for testing and validation
- **Production**: Live production environment with strict security settings

## Environment-Specific Settings Structure

```
core/
├── settings/
│   ├── __init__.py          # Dynamic loader based on ENVIRONMENT variable
│   ├── base.py              # Common settings for all environments
│   ├── development.py       # Development environment settings
│   ├── staging.py           # Staging environment settings
│   └── production.py        # Production environment settings
└── settings.py              # Entry point (imports from settings package)
```

## Configuration

### Setting the Environment

The active environment is determined by the `ENVIRONMENT` environment variable:

```bash
# Development (default)
export ENVIRONMENT=development
# or
set ENVIRONMENT=development

# Staging
export ENVIRONMENT=staging
# or
set ENVIRONMENT=staging

# Production
export ENVIRONMENT=production
# or
set ENVIRONMENT=production
```

### Environment Variables (.env file)

Copy `.env.example` to `.env` and configure based on your environment:

```bash
cp .env.example .env
```

#### Development Configuration (.env)
```
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=dev-secret-key-not-used-in-production
DB_NAME=erp_dev_db
DB_HOST=localhost
DB_USER=erp_user
DB_PASSWORD=erp_password
```

#### Staging Configuration (.env)
```
ENVIRONMENT=staging
DEBUG=False
SECRET_KEY=your-strong-staging-secret-key
DB_NAME=erp_staging_db
DB_HOST=staging-db.example.com
DB_USER=erp_staging_user
DB_PASSWORD=your-staging-db-password
ALLOWED_HOSTS=staging.example.com,www.staging.example.com
CORS_ALLOWED_ORIGINS=https://staging.example.com,https://www.staging.example.com
SSL_CERTIFICATE_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

#### Production Configuration (.env)
```
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-extremely-strong-production-secret-key
DB_NAME=erp_production_db
DB_HOST=prod-db.example.com
DB_USER=erp_prod_user
DB_PASSWORD=your-very-strong-production-db-password
ALLOWED_HOSTS=example.com,www.example.com
CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-specific-password
SSL_CERTIFICATE_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

## Environment-Specific Features

### Development
- ✅ DEBUG=True (detailed error pages)
- ✅ All origins allowed (CORS)
- ✅ SSL disabled
- ✅ Verbose logging (DEBUG level)
- ✅ Database connection pooling: OFF
- ✅ Hot reload supported
- ✅ django_extensions installed

### Staging
- ✅ DEBUG=False (production-like errors)
- ✅ SSL enabled (HTTPS required)
- ✅ HTTPS-only cookies
- ✅ Security headers enabled
- ✅ Specific ALLOWED_HOSTS required
- ✅ Detailed logging (DEBUG level)
- ✅ Database connection pooling: OFF
- ✅ Email sending enabled
- ✅ HSTS headers disabled (for flexibility during testing)

### Production
- ✅ DEBUG=False (minimal error info)
- ✅ SSL enforced (HTTPS only)
- ✅ HTTPS-only cookies with extended timeout
- ✅ Strict security headers
- ✅ HSTS enabled (1 year)
- ✅ HSTS preload enabled
- ✅ CSP policy strict
- ✅ Specific ALLOWED_HOSTS required
- ✅ Warning-level logging only
- ✅ Database connection pooling: 600s
- ✅ Email sending required
- ✅ Static files manifesto storage

## Running the Application

### Development
```bash
export ENVIRONMENT=development
python manage.py runserver
```

### Staging
```bash
export ENVIRONMENT=staging
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Production
```bash
export ENVIRONMENT=production
gunicorn core.wsgi:application \
  --workers 4 \
  --worker-class sync \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

## Docker Deployment

### Development
```bash
docker build -t erp:dev -f Dockerfile.dev .
docker run -e ENVIRONMENT=development -p 8000:8000 erp:dev
```

### Staging
```bash
docker build -t erp:staging -f Dockerfile.staging .
docker run -e ENVIRONMENT=staging -p 443:443 -p 80:80 erp:staging
```

### Production
```bash
docker build -t erp:prod -f Dockerfile.prod .
docker run \
  -e ENVIRONMENT=production \
  -e SECRET_KEY='your-production-secret' \
  -p 443:443 \
  -p 80:80 \
  -v /etc/letsencrypt:/etc/letsencrypt \
  erp:prod
```

## Security Considerations

### For Development
- Never use production data
- Use weak secrets (acceptable for local development)
- Keep DEBUG=True for better error messages

### For Staging
- Use realistic but test data
- Keep strong SECRET_KEY
- Enable SSL/HTTPS
- Test all integrations
- Monitor logs for issues

### For Production
- Use strong, unique SECRET_KEY (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Secure database credentials
- Enable all security headers
- Monitor logs continuously
- Regular backups
- Use environment-specific passwords
- Enable rate limiting
- Use CDN for static files
- Implement DDoS protection

## Database Migrations

Run migrations for the specific environment:

```bash
# Development
export ENVIRONMENT=development
python manage.py migrate

# Staging
export ENVIRONMENT=staging
python manage.py migrate

# Production
export ENVIRONMENT=production
python manage.py migrate
```

## Testing

```bash
# Run tests in development environment
export ENVIRONMENT=development
python manage.py test

# Create test database for staging
export ENVIRONMENT=staging
python manage.py test
```

## Troubleshooting

### Settings Not Loading
```bash
# Verify ENVIRONMENT variable is set
echo $ENVIRONMENT  # Unix/Linux/Mac
echo %ENVIRONMENT%  # Windows

# Check which settings are being used
python manage.py shell
>>> from django.conf import settings
>>> print(settings.ENVIRONMENT)
```

### Database Connection Issues
```bash
# Test database connection
python manage.py dbshell

# Check database settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
```

### Debug Mode Issues
```bash
# If seeing detailed errors when DEBUG should be False
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
```

## See Also

- [Django Settings Documentation](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)
