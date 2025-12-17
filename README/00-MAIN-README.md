# ERP System - Main README

This is a comprehensive Django-based ERP (Enterprise Resource Planning) system with separate modules for HR, Inventory, Finance, Sales, Procurement, Production, Quality, and Maintenance.

## Project Structure

```
├── README/                          # Documentation folder
│   ├── PREREQUISITES.md            # Server prerequisites and setup
│   ├── DEPLOYMENT.md               # Deployment instructions
│   ├── SSH_SETUP.md                # SSH key configuration
│   ├── DATABASE_SETUP.md           # Database configuration
│   ├── GITHUB_ACTIONS.md           # GitHub Actions setup
│   ├── LOCAL_DEVELOPMENT.md        # Local development guide
│   └── API_DOCUMENTATION.md        # API endpoints documentation
├── apps/                           # Django applications
│   ├── hr/                         # HR Module
│   ├── inventory/                  # Inventory Module
│   ├── finance/                    # Finance Module
│   ├── sales/                      # Sales Module
│   ├── procurement/                # Procurement Module
│   ├── production/                 # Production Module
│   ├── quality/                    # Quality Module
│   └── maintenance/                # Maintenance Module
├── core/                           # Django core settings
├── scripts/                        # Deployment and setup scripts
├── .github/                        # GitHub Actions workflows
├── docker-compose.yml              # Docker Compose configuration
├── Dockerfile                      # Docker image configuration
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
└── .env.example                    # Environment variables template
```

## Key Features

- **Modular Architecture**: Each module can be deployed independently
- **Django REST API**: RESTful API for all modules
- **PostgreSQL Database**: Production-ready relational database
- **Docker Support**: Containerized deployment
- **GitHub Actions**: Automated CI/CD pipeline
- **JWT Authentication**: Secure API authentication
- **CORS Support**: Cross-origin resource sharing
- **Admin Dashboard**: Django admin interface
- **Minia Theme**: Professional admin theme (purchased separately)

## Modules

### 1. HR Module (Human Resources)
- Employee management
- Attendance tracking
- Leave management
- Department management

### 2. Inventory Module
- Product catalog
- Stock management
- Stock movements (In/Out/Adjustment)
- Category management

### 3. Finance Module
- Chart of accounts
- Financial transactions
- Reporting (Future)

### 4. Sales Module
- Customer management
- Orders (Future)
- Invoices (Future)

### 5. Procurement Module
- Vendor management
- Purchase orders (Future)
- Supplier management

### 6. Production Module
- Work orders
- Production planning (Future)
- Resource management (Future)

### 7. Quality Module
- Quality checks
- Inspections (Future)
- Compliance tracking (Future)

### 8. Maintenance Module
- Equipment management
- Maintenance requests
- Maintenance scheduling (Future)

## Quick Start

### Local Development
See `README/LOCAL_DEVELOPMENT.md` for detailed setup instructions.

```bash
# Clone repository
git clone <repository-url>
cd erp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose build
docker-compose up -d

# Access the application
# App: http://localhost:8000
# Admin: http://localhost:8000/admin
```

## Prerequisites

Before deployment, ensure you have:

1. **Ubuntu 20.04 or 22.04 LTS** on both servers
2. **SSH Access** with public key authentication
3. **Docker & Docker Compose** installed
4. **PostgreSQL** installed on database server
5. **Git** installed on app server
6. **Python 3.11+** (for local development)

See `README/PREREQUISITES.md` for detailed prerequisites.

## Deployment

### Using GitHub Actions

1. **Setup SSH Keys**: See `README/SSH_SETUP.md`
2. **Configure GitHub Secrets**: See `README/GITHUB_ACTIONS.md`
3. **Deploy**: Push to `main` branch

Each module has its own GitHub Actions workflow:
- `.github/workflows/deploy-hr.yml`
- `.github/workflows/deploy-inventory.yml`
- `.github/workflows/deploy-full.yml`

### Manual Deployment

See `README/DEPLOYMENT.md` for step-by-step manual deployment instructions.

## Server Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Local Development                      │
│                 (Your Machine)                          │
│                                                         │
│  Docker Container (App + DB)                            │
│  ├── Django App (Port 8000)                             │
│  ├── PostgreSQL (Port 5432)                             │
│  └── Redis (Port 6379)                                  │
└─────────────────────────────────────────────────────────┘
         ↓ Push to GitHub ↓
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions CI/CD Pipeline              │
│                                                         │
│  ├── Test (Unit/Integration Tests)                      │
│  ├── Build (Docker Image)                               │
│  └── Deploy (SSH to Servers)                            │
└─────────────────────────────────────────────────────────┘
         ↓ SSH Deploy ↓ SSH Deploy ↓
    ┌────────────┐         ┌────────────┐
    │ App Server │         │  DB Server │
    │ (Ubuntu)   │         │  (Ubuntu)  │
    │            │         │            │
    │ Docker     │────────→│ PostgreSQL │
    │ Container  │ TCP:5432│            │
    │ Port: 8000 │         │ Port: 5432 │
    └────────────┘         └────────────┘
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Django
DEBUG=False  # Always False in production
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=app.yourdomain.com,yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_db
DB_USER=erp_user
DB_PASSWORD=your-secure-password
DB_HOST=<database-server-ip>
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# JWT
JWT_ACCESS_LIFETIME=5
JWT_REFRESH_LIFETIME=1
```

## API Endpoints

All API endpoints are prefixed with `/api/` and require JWT authentication.

### HR Module
- `GET/POST /api/hr/employees/` - List/Create employees
- `GET /api/hr/attendance/` - View attendance records
- `GET/POST /api/hr/leaves/` - Manage leave requests

### Inventory Module
- `GET/POST /api/inventory/products/` - Product management
- `GET /api/inventory/stock-movements/` - Track stock movements
- `GET /api/inventory/categories/` - Product categories

### Finance Module
- `GET/POST /api/finance/charts/` - Chart of accounts

### Sales Module
- `GET/POST /api/sales/customers/` - Customer management

### Procurement Module
- `GET/POST /api/procurement/vendors/` - Vendor management

### Production Module
- `GET/POST /api/production/work-orders/` - Work order management

### Quality Module
- `GET /api/quality/checks/` - Quality check records

### Maintenance Module
- `GET/POST /api/maintenance/equipment/` - Equipment management
- `GET/POST /api/maintenance/requests/` - Maintenance requests

## Authentication

All API endpoints require JWT token authentication.

### Obtaining a Token

```bash
# Get access and refresh tokens
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using the Token

```bash
# Include in Authorization header
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/hr/employees/
```

## Database Backup

### Automated Backup

```bash
# On database server
pg_dump -U erp_user -d erp_db > /var/backups/erp_db/backup-$(date +%Y%m%d).sql
```

### Restore from Backup

```bash
# Restore database
psql -U erp_user -d erp_db < /var/backups/erp_db/backup-YYYYMMDD.sql
```

## Monitoring and Logs

### View Logs

```bash
# Application logs
docker logs -f erp_app

# Database logs
docker logs -f erp_db

# View log file
tail -f /opt/erp/logs/erp.log
```

### Health Check

```bash
# Check application health
curl http://localhost:8000/admin/

# Check database connection
docker exec erp_db pg_isready -U erp_user
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check database server is running
   - Verify connection credentials in .env
   - Check firewall rules for port 5432

2. **Module Not Loading**
   - Run migrations: `python manage.py migrate`
   - Check module is in INSTALLED_APPS in settings.py

3. **Static Files Not Loading**
   - Collect static files: `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL configuration

4. **Permission Denied SSH Error**
   - Verify SSH key permissions: `chmod 600 ~/.ssh/id_rsa`
   - Check GitHub Secrets are configured correctly

## Future Integrations

The system is designed to support integrations with:
- AI Void integration
- Website integration for online sales
- Third-party payment gateways
- Email and SMS notifications
- Analytics platforms

## Documentation

For detailed information, refer to:
- `README/LOCAL_DEVELOPMENT.md` - Local development setup
- `README/DEPLOYMENT.md` - Server deployment guide
- `README/PREREQUISITES.md` - Prerequisites checklist
- `README/GITHUB_ACTIONS.md` - GitHub Actions setup
- `README/DATABASE_SETUP.md` - Database configuration
- `README/SSH_SETUP.md` - SSH key setup
- `README/API_DOCUMENTATION.md` - API reference

## Support and Contribution

For support, issues, or contributions, please:
1. Check existing documentation
2. Review GitHub issues
3. Create a new issue with detailed information

## License

This project is proprietary. All rights reserved.

## Contact

For questions or support, contact the development team.
