# Enterprise Resource Planning (ERP) System

A comprehensive, modular Django-based ERP system with separate deployment pipelines for each module using GitHub Actions.

## 🚀 Quick Overview

- **Backend**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL 15
- **Infrastructure**: Docker & Docker Compose
- **CI/CD**: GitHub Actions with automated testing and deployment
- **Architecture**: Microservices-inspired modular design
- **Authentication**: JWT (JSON Web Tokens)
- **Admin Dashboard**: Django admin with Minia theme support

## 📦 Modules

| Module | Purpose | Status |
|--------|---------|--------|
| **HR** | Employee management, attendance, leaves | ✅ Ready |
| **Inventory** | Product catalog, stock management | ✅ Ready |
| **Finance** | Chart of accounts, transactions | ✅ Ready |
| **Sales** | Customer management | ✅ Ready |
| **Procurement** | Vendor management | ✅ Ready |
| **Production** | Work orders, production planning | ✅ Ready |
| **Quality** | Quality checks and compliance | ✅ Ready |
| **Maintenance** | Equipment and maintenance requests | ✅ Ready |

## 🎯 Key Features

✨ **Modular Architecture** - Deploy modules independently  
🔐 **JWT Authentication** - Secure API endpoints  
📊 **RESTful API** - Complete API documentation  
🐳 **Docker Ready** - Containerized deployment  
🚀 **CI/CD Pipeline** - Automated testing and deployment  
📱 **Admin Panel** - Professional Django admin  
⚡ **High Performance** - Optimized queries and caching  
🔄 **Version Control** - Git-based workflows  

## 📋 Quick Start

### For Local Development

See `README/LOCAL_DEVELOPMENT.md` for detailed setup:

```bash
git clone <repository-url>
cd erp
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker-compose up -d
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### For Production Deployment

See `README/DEPLOYMENT.md` for complete deployment guide:

1. **Prerequisites**: Install Docker, PostgreSQL, Git (see `README/PREREQUISITES.md`)
2. **SSH Setup**: Configure SSH keys (see `README/SSH_SETUP.md`)
3. **GitHub Actions**: Setup CI/CD (see `README/GITHUB_ACTIONS.md`)
4. **Deploy**: Push code to trigger automated deployment

## 📚 Documentation

All documentation is organized in the `README/` directory:

- **00-MAIN-README.md** - Project overview and architecture
- **01-PREREQUISITES.md** - Server setup requirements
- **02-SSH_SETUP.md** - SSH key configuration
- **03-GITHUB_ACTIONS.md** - CI/CD pipeline setup
- **04-DEPLOYMENT.md** - Production deployment guide
- **05-LOCAL_DEVELOPMENT.md** - Local development setup
- **06-API_DOCUMENTATION.md** - API reference

## 🏗️ Project Structure

```
erp/
├── README/                          # Documentation (all .md files)
├── apps/                            # Django applications
│   ├── hr/                          # HR module
│   ├── inventory/                   # Inventory module
│   ├── finance/                     # Finance module
│   ├── sales/                       # Sales module
│   ├── procurement/                 # Procurement module
│   ├── production/                  # Production module
│   ├── quality/                     # Quality module
│   └── maintenance/                 # Maintenance module
├── core/                            # Django core configuration
├── scripts/                         # Deployment scripts
├── .github/workflows/               # GitHub Actions workflows
├── Dockerfile                       # Docker image definition
├── docker-compose.yml              # Docker Compose configuration
├── requirements.txt                # Python dependencies
├── manage.py                       # Django management
└── .env.example                    # Environment template
```

## 🔄 Deployment Architecture

```
┌─────────────────────────────────────┐
│   GitHub Repository (Source Code)   │
└──────────────────┬──────────────────┘
                   │ Push
                   ▼
┌─────────────────────────────────────┐
│    GitHub Actions CI/CD Pipeline    │
│  ├─ Test Code                       │
│  ├─ Build Docker Image              │
│  └─ Deploy via SSH                  │
└──────────────────┬──────────────────┘
         ┌─────────┴─────────┐
         ▼                   ▼
    ┌─────────────┐    ┌──────────────┐
    │ App Server  │    │ Database     │
    │ (Ubuntu)    │    │ Server       │
    │             │    │ (Ubuntu)     │
    │ Port: 8000  │───→│ Port: 5432   │
    │ Django+     │    │ PostgreSQL   │
    │ Gunicorn    │    │              │
    └─────────────┘    └──────────────┘
```

## 🔐 Security Features

- **JWT Authentication** - Stateless API security
- **CORS Protection** - Cross-origin resource control
- **HTTPS Ready** - SSL/TLS support in production
- **SQL Injection Prevention** - ORM-based queries
- **CSRF Protection** - Cross-site request forgery prevention
- **Secret Management** - Environment-based secrets

## 📊 API Endpoints

All endpoints are documented in `README/API_DOCUMENTATION.md`

**Authentication**:
```bash
POST /api/token/                    # Get JWT token
POST /api/token/refresh/            # Refresh token
```

**Modules** (Example):
```bash
GET    /api/hr/employees/           # List employees
POST   /api/hr/employees/           # Create employee
GET    /api/hr/employees/{id}/      # Retrieve employee
PUT    /api/hr/employees/{id}/      # Update employee
DELETE /api/hr/employees/{id}/      # Delete employee
```

Similar endpoints for other modules.

## 🚀 GitHub Actions Workflows

Each module has its own deployment workflow:

- `.github/workflows/deploy-hr.yml` - HR module
- `.github/workflows/deploy-inventory.yml` - Inventory module
- `.github/workflows/deploy-full.yml` - Full application

**Workflow Stages**:
1. **Test** - Unit and integration tests
2. **Build** - Docker image creation
3. **Deploy** - SSH deployment to production
4. **Verify** - Health checks

## 📋 Prerequisites Checklist

**App Server**:
- [ ] Ubuntu 20.04+ LTS
- [ ] Docker & Docker Compose installed
- [ ] Git installed
- [ ] SSH public key authentication configured
- [ ] 4GB RAM, 20GB disk space

**Database Server**:
- [ ] Ubuntu 20.04+ LTS
- [ ] PostgreSQL 15 installed
- [ ] Remote access configured
- [ ] SSH public key authentication configured
- [ ] 4GB RAM, 20GB disk space

## 🛠️ Configuration

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Key variables:
- `DEBUG` - Django debug mode (False in production)
- `SECRET_KEY` - Django secret key (generate new one!)
- `DB_HOST` - Database server IP
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` - Database credentials
- `ALLOWED_HOSTS` - Allowed domain names
- `JWT_ACCESS_LIFETIME` - Token expiration time

## 🧪 Testing

Run tests locally:

```bash
# All tests
pytest

# Specific module
pytest apps/hr/

# With coverage
pytest --cov=apps
```

GitHub Actions runs tests automatically on every push.

## 🔍 Monitoring

View application logs:

```bash
# On app server
docker logs -f erp_app

# Or using compose
docker-compose logs -f app
```

Check system health:

```bash
# Container status
docker ps

# Resource usage
docker stats erp_app

# Database connection
psql -U erp_user -d erp_db -h <db-server-ip>
```

## 📈 Performance Optimization

- Database query optimization with `select_related()` and `prefetch_related()`
- Redis caching for frequently accessed data
- Static file compression and minification
- CDN-ready static file serving
- Connection pooling for database
- Load balancing ready architecture

## 🔄 Update Strategy

1. **Minor Updates**: Push to `develop` branch → GitHub Actions tests → Manual PR review → Merge to `main` → Auto-deploy
2. **Patch Updates**: Direct to `main` branch for hotfixes → Auto-deploy (with approval)
3. **Major Updates**: Feature branch → Extended testing → Release branch → Staged deployment

## 🤝 Future Integrations

The system is designed to integrate with:

- **AI Integration**: AI Void integration for intelligent automation
- **E-commerce**: Website integration for online sales
- **Payment Gateway**: Payment processing (Stripe, PayPal, etc.)
- **Email/SMS**: Notification system integration
- **Analytics**: BI tools integration (Power BI, Tableau)
- **Third-party APIs**: Custom API integrations

## 📞 Support

For issues or questions:

1. Check relevant README file in `README/` directory
2. Review GitHub Issues
3. Check application logs
4. Contact development team

## 📄 License

This project is proprietary. All rights reserved.

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)

## ✅ Deployment Checklist

- [ ] Read all README files
- [ ] Complete prerequisites setup
- [ ] Configure SSH keys
- [ ] Add GitHub Secrets
- [ ] Create test deployment
- [ ] Verify all modules working
- [ ] Setup monitoring
- [ ] Create backup strategy
- [ ] Document custom configs
- [ ] Train users

---

**Start here**: Read `README/00-MAIN-README.md` for complete project overview.

**Need help?** Check the relevant README file in the `README/` directory.

Happy deploying! 🚀
