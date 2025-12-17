# ⚡ QUICK REFERENCE GUIDE

Fast access to common commands and information.

## 🚀 Start Here (In This Order)

1. **Read Overview**: `README/00-MAIN-README.md` (5 min)
2. **Check Prerequisites**: `README/01-PREREQUISITES.md` (10 min)
3. **Setup SSH**: `README/02-SSH_SETUP.md` (15 min)
4. **Configure GitHub**: `README/03-GITHUB_ACTIONS.md` (10 min)
5. **Deploy**: `README/04-DEPLOYMENT.md` (30 min)

---

## 📍 Key Directories

```
/README          - All documentation (read these!)
/apps            - Django modules (8 modules)
/core            - Django settings
/scripts         - Deployment scripts
/.github         - GitHub Actions workflows
```

---

## 🔐 Credentials & Keys to Create

```bash
# Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate SSH keys
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

# Show SSH public key (for GitHub Secrets)
cat ~/.ssh/id_rsa.pub
```

---

## 🎯 GitHub Secrets to Add (6 Required)

| Secret | Value |
|--------|-------|
| `SSH_PRIVATE_KEY` | Content of `~/.ssh/id_rsa` |
| `APP_SERVER_IP` | Your app server IP (e.g., 203.0.113.45) |
| `APP_SERVER_USER` | SSH user (usually `deploy` or `ubuntu`) |
| `APP_SERVER_PORT` | SSH port (usually `22`) |
| `DB_SERVER_IP` | Your database server IP |
| `DB_SERVER_USER` | SSH user on DB server |

---

## 🐳 Docker Commands

```bash
# Start all containers
docker-compose up -d

# View containers
docker ps

# View logs
docker-compose logs -f app

# Stop containers
docker-compose down

# Rebuild image
docker-compose build

# Execute command in container
docker-compose exec app python manage.py migrate
```

---

## 🔗 Important URLs

```
Admin Panel:         http://APP_SERVER_IP:8000/admin
API Base:            http://APP_SERVER_IP:8000/api/
API Docs (Swagger):  http://APP_SERVER_IP:8000/api/schema/swagger/
API Docs (ReDoc):    http://APP_SERVER_IP:8000/api/schema/redoc/

Modules:
HR:                  http://APP_SERVER_IP:8000/api/hr/
Inventory:           http://APP_SERVER_IP:8000/api/inventory/
Finance:             http://APP_SERVER_IP:8000/api/finance/
Sales:               http://APP_SERVER_IP:8000/api/sales/
Procurement:         http://APP_SERVER_IP:8000/api/procurement/
Production:          http://APP_SERVER_IP:8000/api/production/
Quality:             http://APP_SERVER_IP:8000/api/quality/
Maintenance:         http://APP_SERVER_IP:8000/api/maintenance/
```

---

## 🔑 Django Management Commands

```bash
# Local development
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
pytest

# Database shell
python manage.py dbshell

# Create superuser (automated)
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password123')" | python manage.py shell
```

---

## 🐚 SSH Commands

```bash
# Connect to servers
ssh deploy@APP_SERVER_IP
ssh deploy@DB_SERVER_IP

# Check SSH access
ssh deploy@APP_SERVER_IP "echo 'Success'"

# Copy file to server
scp file.txt deploy@APP_SERVER_IP:/tmp/

# View remote logs
ssh deploy@APP_SERVER_IP "docker logs -f erp_app"
```

---

## 🚢 Deployment Commands

```bash
# On app server
cd /opt/erp
docker-compose up -d
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py collectstatic --noinput
docker-compose exec app python manage.py createsuperuser

# Check status
docker ps
curl http://localhost:8000/admin/

# View logs
docker-compose logs -f app
```

---

## 🧪 Testing Commands

```bash
# Run all tests
pytest

# Run specific module tests
pytest apps/hr/

# Run with coverage
pytest --cov=apps

# Run specific test
pytest apps/hr/tests.py::TestEmployeeModel

# Run with output
pytest -v -s
```

---

## 📊 Database Commands

```bash
# Connect to PostgreSQL
psql -U erp_user -d erp_db -h localhost

# Create backup
pg_dump -U erp_user -d erp_db > backup.sql

# Restore from backup
psql -U erp_user -d erp_db < backup.sql

# Show all databases
psql -U erp_user -l

# From container
docker-compose exec db psql -U erp_user -d erp_db
```

---

## 📝 Configuration Files to Edit

```
.env                 - All environment variables (required)
core/settings.py    - Django configuration (usually OK as-is)
docker-compose.yml  - Container configuration (usually OK as-is)
Dockerfile          - Image definition (usually OK as-is)
```

---

## 🔄 Git Workflow

```bash
# Clone repository
git clone https://github.com/username/erp.git
cd erp

# Create branch
git checkout -b feature/my-feature

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Add my feature"

# Push
git push origin feature/my-feature

# Create Pull Request on GitHub
# After review and merge to main, GitHub Actions auto-deploys!
```

---

## 📋 ENV Variables

```env
# Required
DEBUG=False
SECRET_KEY=your-secret-key-min-50-chars

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_db
DB_USER=erp_user
DB_PASSWORD=your-password
DB_HOST=database-server-ip
DB_PORT=5432

# Security
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# JWT
JWT_ACCESS_LIFETIME=5
JWT_REFRESH_LIFETIME=1

# Optional
TIME_ZONE=UTC
DEBUG_SQL=False
```

---

## 🎯 API Authentication

```bash
# Get tokens
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Response has: access, refresh tokens

# Use access token
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  http://localhost:8000/api/hr/employees/

# Refresh token when expired
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "REFRESH_TOKEN"}'
```

---

## 🐛 Troubleshooting Commands

```bash
# Check if Docker is running
docker ps

# Check server connectivity
ping APP_SERVER_IP
ssh -v deploy@APP_SERVER_IP

# View app logs
docker-compose logs -f app

# View database logs
docker-compose logs -f db

# Check port availability
netstat -tuln | grep 8000

# Check disk space
df -h

# Check memory
free -h

# Test database connection
psql -U erp_user -h DB_SERVER_IP -d erp_db -c "SELECT 1;"
```

---

## 📞 Common Issues Quick Fix

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | `sudo lsof -i :8000; kill -9 PID` |
| Database not connecting | Check IP, port, credentials in .env |
| SSH connection failed | Check key permissions: `chmod 600 ~/.ssh/id_rsa` |
| Docker build failed | Check Python version (3.11+), disk space |
| Tests failing | Run `python manage.py migrate` first |
| Static files missing | Run `python manage.py collectstatic` |
| Permission denied | Check file ownership: `sudo chown $USER:$USER /opt/erp` |

---

## 📱 Module API Examples

### Create Employee (HR)
```bash
curl -X POST http://localhost:8000/api/hr/employees/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "department": "HR",
    "position": "Manager",
    "salary": "50000.00"
  }'
```

### Get Products (Inventory)
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/inventory/products/?category=1&search=widget"
```

### Create Customer (Sales)
```bash
curl -X POST http://localhost:8000/api/sales/customers/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ACME Corp",
    "email": "info@acme.com",
    "phone": "555-1234",
    "address": "123 Business St",
    "city": "New York",
    "country": "USA"
  }'
```

---

## 🔄 Deployment Workflow

1. **Make changes** locally
2. **Test locally** (`pytest`)
3. **Commit** (`git add . && git commit -m "message"`)
4. **Push** (`git push origin branch`)
5. **GitHub Actions** runs automatically:
   - Tests run (pass = proceed, fail = stop)
   - Docker image built
   - Deployed to production via SSH
   - Health checks run
6. **Verify** at `http://APP_SERVER_IP:8000/admin`

---

## ⏱️ Typical Timings

| Task | Time |
|------|------|
| Setup prerequisites | 1 hour |
| Setup servers | 30 minutes |
| Configure GitHub | 15 minutes |
| First deployment | 20-35 minutes |
| Subsequent deployments | 10-20 minutes |

---

## 📚 Documentation Quick Links

- Overview: `README/00-MAIN-README.md`
- Prerequisites: `README/01-PREREQUISITES.md`
- SSH Setup: `README/02-SSH_SETUP.md`
- GitHub Actions: `README/03-GITHUB_ACTIONS.md`
- Deployment: `README/04-DEPLOYMENT.md`
- Local Dev: `README/05-LOCAL_DEVELOPMENT.md`
- API Docs: `README/06-API_DOCUMENTATION.md`
- Next Steps: `README/07-NEXT_STEPS.md`

---

## 🎯 Daily Commands (After Setup)

```bash
# Check app status
docker ps

# View logs
docker-compose logs -f app

# Deploy latest code
git pull origin main
docker-compose down
docker-compose up -d

# Backup database
docker-compose exec db pg_dump -U erp_user erp_db > backup-$(date +%Y%m%d).sql
```

---

## 🆘 When Something Goes Wrong

1. **Check logs**: `docker-compose logs app`
2. **Check database**: `docker-compose logs db`
3. **Check GitHub Actions**: Go to Actions tab
4. **SSH to server**: `ssh deploy@APP_SERVER_IP`
5. **Review error messages**: Look for clues in logs
6. **Rollback if needed**: `git revert HEAD`
7. **Consult documentation**: Check README files

---

**Remember**: Read the full documentation for detailed explanations!

This quick reference is for quick lookups, not a replacement for complete documentation.

**For complete information, see README files.**
