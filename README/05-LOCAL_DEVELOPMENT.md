# Local Development Guide

Set up the ERP system for local development on your machine.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- PostgreSQL or Docker
- Git
- A code editor (VS Code, PyCharm, etc.)

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd erp
```

## Step 2: Create Virtual Environment

### On macOS/Linux

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Verify activation:

```bash
# Should show venv Python path
which python
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Setup Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit configuration
nano .env  # or use your editor
```

### Default Development Configuration

```env
DEBUG=True
SECRET_KEY=dev-secret-key-not-secure-for-production
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_db
DB_USER=erp_user
DB_PASSWORD=erp_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Step 5: Setup Database (Choose One)

### Option A: Using Docker (Recommended)

```bash
# Start Docker containers
docker-compose up -d

# Wait 10 seconds for database to be ready
sleep 10

# Verify containers are running
docker ps
```

### Option B: Local PostgreSQL

On macOS with Homebrew:

```bash
brew install postgresql
brew services start postgresql

# Create database and user
createdb erp_db
psql -c "CREATE USER erp_user WITH PASSWORD 'erp_password';"
psql -c "ALTER ROLE erp_user SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;"
```

On Ubuntu/Debian:

```bash
sudo apt-get install -y postgresql postgresql-contrib

# Create database and user
sudo -u postgres createdb erp_db
sudo -u postgres psql -c "CREATE USER erp_user WITH PASSWORD 'erp_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;"
```

## Step 6: Run Migrations

```bash
python manage.py migrate
```

Expected output:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, finance, hr, inventory, ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

## Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

Follow prompts:

```
Username: admin
Email: admin@example.com
Password: 
Password (again): 
Superuser created successfully.
```

## Step 8: Run Development Server

```bash
python manage.py runserver
```

Output:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Step 9: Access Application

### Admin Panel

Open browser: `http://localhost:8000/admin`

Login with superuser credentials.

### API

Get JWT token:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

Use token to access endpoints:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/hr/employees/
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/my-feature
```

### 2. Make Changes

```bash
# Edit files
nano apps/hr/models.py

# Create migrations if models changed
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 3. Run Tests

```bash
# Run all tests
pytest

# Run specific module tests
pytest apps/hr/

# Run with coverage
pytest --cov=apps
```

### 4. Code Quality Checks

```bash
# Format code
black apps/

# Check linting
flake8 apps/

# Check type hints
mypy apps/
```

### 5. Commit and Push

```bash
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
```

### 6. Create Pull Request

On GitHub, create PR and request review.

---

## Common Development Tasks

### Create New Model

```bash
# Edit models.py
nano apps/inventory/models.py

# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Register in admin
nano apps/inventory/admin.py

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
```

### Create New API Endpoint

```bash
# 1. Create serializer
nano apps/sales/serializers.py

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

# 2. Create viewset
nano apps/sales/views.py

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# 3. Register in urls.py
router.register(r'orders', OrderViewSet)
```

### Create New Test

```bash
# Create test file
nano apps/sales/tests.py

from django.test import TestCase

class OrderTestCase(TestCase):
    def setUp(self):
        self.order = Order.objects.create(...)
    
    def test_order_creation(self):
        self.assertEqual(self.order.id, 1)

# Run test
pytest apps/sales/tests.py::OrderTestCase::test_order_creation
```

### Add Package Dependency

```bash
# Install package
pip install package-name

# Add to requirements.txt
echo "package-name==1.0.0" >> requirements.txt

# Or update all
pip freeze > requirements.txt
```

---

## Useful Commands

### Database Management

```bash
# Create backup
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json

# Clear database
python manage.py flush

# Reset specific app
python manage.py migrate apps.hr zero
```

### Development Utilities

```bash
# Django shell
python manage.py shell

# Create sample data
python manage.py shell < scripts/create_sample_data.py

# Check configuration
python manage.py check

# Show settings
python manage.py diffsettings

# Collect static files
python manage.py collectstatic

# Run development server on different port
python manage.py runserver 0.0.0.0:8001
```

### Debugging

```bash
# Enable SQL query logging
# In settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Or use in shell
python manage.py shell
>>> from django.db import connection
>>> print(connection.queries)
```

### API Testing

```bash
# Using curl
curl http://localhost:8000/api/hr/employees/

# Using httpie
http GET http://localhost:8000/api/hr/employees/

# Using Python requests
python
>>> import requests
>>> r = requests.get('http://localhost:8000/api/hr/employees/')
>>> r.json()
```

---

## IDE Setup

### VS Code

#### Install Extensions

- Python
- Django
- SQLTools
- REST Client
- Thunder Client

#### .vscode/settings.json

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.defaultFormatter": "ms-python.python",
        "editor.formatOnSave": true
    }
}
```

### PyCharm

1. File → Settings → Project → Python Interpreter
2. Click gear → Add
3. Select existing environment: `/path/to/erp/venv`
4. Mark `apps/` as Sources Root
5. Configure Run/Debug configurations

---

## Troubleshooting

### Virtual Environment Not Activated

```bash
# Verify
which python

# Should show path with venv

# Activate if needed
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

### Database Connection Error

```bash
# Check PostgreSQL running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Check connection
psql -U erp_user -d erp_db -c "SELECT 1;"

# Check .env file
cat .env | grep DB_
```

### Module Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify installed packages
pip list | grep django
```

### Migration Errors

```bash
# Show migration status
python manage.py showmigrations

# Check for conflicts
python manage.py migrate --plan

# Reset migrations (WARNING: data loss!)
python manage.py migrate apps.hr zero
```

---

## Performance Tips

### Use select_related/prefetch_related

```python
# Avoid N+1 queries
employees = Employee.objects.select_related('user').prefetch_related('leaves')

# Instead of
employees = Employee.objects.all()
```

### Enable Query Caching

```python
# Add to views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def employee_list(request):
    return Response(...)
```

### Use Django Debug Toolbar

```bash
pip install django-debug-toolbar

# Add to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    'debug_toolbar',
    ...
]

# Access at http://localhost:8000/__debug__/
```

---

## Documentation Tools

### Generate API Documentation

```bash
# View Swagger/OpenAPI
http://localhost:8000/api/schema/swagger/

# Download OpenAPI schema
http://localhost:8000/api/schema/
```

### Generate Code Documentation

```bash
pip install sphinx

sphinx-quickstart docs
sphinx-apidoc -o docs/ apps/

cd docs
make html
```

---

## Next Steps

1. Explore the admin interface
2. Run the test suite
3. Create your first API endpoint
4. Write tests for your code
5. Submit a pull request

---

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pytest Documentation](https://docs.pytest.org/)

Happy coding! 🚀
