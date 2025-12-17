# Deployment Guide

Complete step-by-step guide to deploy the ERP system to production servers.

## Architecture Overview

```
GitHub Repository
       ↓ push code
GitHub Actions CI/CD
       ├─ Test Code
       ├─ Build Docker Image
       └─ Deploy via SSH
            ├─ App Server (Port 8000)
            │  └─ Docker Container
            │     ├─ Django App
            │     ├─ Gunicorn
            │     └─ Static Files
            └─ Database Server (Port 5432)
               └─ PostgreSQL Container
```

## Prerequisites

Before deploying, ensure:

1. ✓ Prerequisites installed (see `01-PREREQUISITES.md`)
2. ✓ SSH keys configured (see `02-SSH_SETUP.md`)
3. ✓ GitHub Secrets added (see `03-GITHUB_ACTIONS.md`)
4. ✓ Both servers have SSH access
5. ✓ Both servers can reach each other

## Deployment Methods

### Method 1: Automatic Deployment (Recommended)

Using GitHub Actions - automatically triggers on code push.

### Method 2: Manual SSH Deployment

For immediate deployment without pushing to GitHub.

### Method 3: Manual Full Deployment

Step-by-step deployment using scripts.

---

## Method 1: Automatic Deployment via GitHub Actions

### Step 1: Prepare Code

```bash
# Clone repository locally
git clone <repository-url>
cd erp

# Create feature branch
git checkout -b feature/my-feature

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add new feature"

# Push to repository
git push origin feature/my-feature

# Create Pull Request on GitHub
# After review, merge to main branch
```

### Step 2: Monitor Deployment

1. Go to GitHub repository → **Actions** tab
2. Select your workflow (e.g., "Deploy HR Module")
3. Watch the progress:
   - **Test** job runs first
   - **Build** job runs after tests pass
   - **Deploy** job runs after build completes
4. View logs for any job by clicking on it

### Step 3: Verify Deployment

Once workflow completes successfully:

```bash
# SSH into app server
ssh deploy@app-server-ip

# Check running containers
docker ps

# View application logs
docker logs -f erp_app

# Test application
curl http://localhost:8000/admin/
```

### Deployment Workflow Stages

```
1. Test Stage (5-10 minutes)
   └─ Runs unit tests
   └─ Tests database migrations
   └─ Checks code coverage

2. Build Stage (10-15 minutes)
   └─ Builds Docker image
   └─ Tags with commit SHA
   └─ Saves image for deployment

3. Deploy Stage (5-10 minutes)
   └─ Connects via SSH
   └─ Loads Docker image
   └─ Starts new container
   └─ Runs health checks

Total Time: 20-35 minutes
```

---

## Method 2: Manual SSH Deployment

For immediate deployment without GitHub Actions.

### Step 1: Build Docker Image Locally

```bash
# On your local machine
docker build -t erp-app:manual-$(date +%Y%m%d-%H%M%S) .
```

### Step 2: Save and Transfer Image

```bash
# Save image
docker save erp-app:manual-20240101-120000 > erp-app.tar

# Transfer to app server
scp -P 22 erp-app.tar deploy@app-server-ip:/tmp/
```

### Step 3: Deploy on App Server

```bash
# SSH into app server
ssh deploy@app-server-ip

# Navigate to app directory
cd /opt/erp

# Load Docker image
docker load -i /tmp/erp-app.tar

# Stop current container
docker stop erp_app || true
docker rm erp_app || true

# Start new container
docker run -d \
    --name erp_app \
    --restart unless-stopped \
    --network erp_network \
    -p 8000:8000 \
    --env-file .env \
    -v /opt/erp/static:/app/staticfiles \
    -v /opt/erp/media:/app/media \
    erp-app:manual-20240101-120000

# Check status
docker ps | grep erp_app
```

---

## Method 3: Manual Full Deployment with Scripts

### Step 1: Setup Database Server

```bash
# On database server
ssh deploy@db-server-ip

# Run database setup script
bash scripts/setup-db-server.sh

# Verify PostgreSQL
sudo systemctl status postgresql

# Test database
psql -U erp_user -d erp_db -h localhost -c "SELECT 1;"
```

### Step 2: Setup App Server

```bash
# On app server
ssh deploy@app-server-ip

# Run server setup script
bash scripts/setup-server.sh

# Verify Docker
docker --version
docker-compose --version

# Verify network
docker network ls | grep erp_network
```

### Step 3: Clone Repository

```bash
# On app server
cd /opt/erp

# Clone repository
git clone <repository-url> .

# Or if already cloned, pull latest
git pull origin main
```

### Step 4: Create Environment File

```bash
# On app server
cd /opt/erp

# Copy template
cp .env.example .env

# Edit with your values
nano .env
```

Fill in values:

```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-min-50-chars
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_db
DB_USER=erp_user
DB_PASSWORD=your-database-password
DB_HOST=<db-server-ip>
DB_PORT=5432
ALLOWED_HOSTS=app.yourdomain.com,yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Step 5: Build and Deploy

```bash
# On app server
cd /opt/erp

# Build Docker image
docker build -t erp-app:latest .

# Start containers
docker-compose up -d

# Run migrations
docker-compose exec app python manage.py migrate

# Collect static files
docker-compose exec app python manage.py collectstatic --noinput

# Create superuser (optional)
docker-compose exec app python manage.py createsuperuser
```

### Step 6: Verify Deployment

```bash
# Check running containers
docker ps

# Check logs
docker-compose logs -f app

# Test application
curl http://localhost:8000/admin/

# Health check
curl -I http://localhost:8000/admin/ | grep HTTP
```

---

## Post-Deployment Verification

### 1. Application Access

```bash
# From your local machine
curl -I http://app-server-ip:8000/admin/

# Should return HTTP 200
HTTP/1.1 200 OK
```

### 2. Admin Panel

Open browser and navigate to:
```
http://app-server-ip:8000/admin/
```

Login with superuser credentials created during setup.

### 3. API Endpoints

```bash
# Get JWT token
curl -X POST http://app-server-ip:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# Use token to access API
TOKEN="your_access_token_here"
curl -H "Authorization: Bearer $TOKEN" \
  http://app-server-ip:8000/api/hr/employees/
```

### 4. Database Connection

```bash
# From app server
docker-compose exec app python manage.py dbshell

# Or test directly
psql -U erp_user -d erp_db -h <db-server-ip> -c "SELECT version();"
```

### 5. Static Files

```bash
# Check if static files exist
docker exec erp_app ls -la /app/staticfiles/

# Access static files
curl http://app-server-ip:8000/static/admin/
```

---

## Deployment Troubleshooting

### Issue: Docker Build Failed

```bash
# View detailed error
docker build -t erp-app:test . --verbose

# Common causes:
# 1. Missing requirements
pip install -r requirements.txt

# 2. Python version mismatch
python --version  # Should be 3.11+

# 3. Disk space
df -h  # Check available space
```

### Issue: Database Connection Error

```bash
# Check PostgreSQL on DB server
ssh deploy@db-server-ip "sudo systemctl status postgresql"

# Test connection from app server
ssh deploy@app-server-ip "psql -U erp_user -h <db-server-ip> -d erp_db -c 'SELECT 1;'"

# Check firewall
ssh deploy@db-server-ip "sudo ufw status"
ssh deploy@db-server-ip "sudo ufw allow 5432/tcp"
```

### Issue: Application Won't Start

```bash
# Check logs
docker logs erp_app

# Common errors:
# 1. Secret key not set
# Check .env file exists and has SECRET_KEY

# 2. Database not ready
# Wait a few seconds after starting database

# 3. Port already in use
docker port erp_app
# Kill process: kill -9 <PID>
```

### Issue: Static Files Not Loading

```bash
# Collect static files
docker-compose exec app python manage.py collectstatic --noinput

# Check permissions
docker exec erp_app ls -la /app/staticfiles/

# Verify STATIC_URL in settings
docker exec erp_app python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_URL)
>>> print(settings.STATIC_ROOT)
```

### Issue: Out of Memory

```bash
# Check server resources
free -h
df -h

# Increase swap if needed
sudo swapon -s
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Rollback Procedure

If deployment fails or needs to be rolled back:

### Option 1: GitHub Actions Rollback

In the failed workflow job:

1. Go to GitHub Actions
2. Find the failed deployment
3. Click "Re-run jobs"
4. Select "Re-run failed jobs"

Or manually deploy previous version:

```bash
# On app server
cd /opt/erp

# Show git history
git log --oneline

# Checkout previous version
git checkout <previous-commit-sha>

# Rebuild and redeploy
docker build -t erp-app:rollback .
docker stop erp_app
docker rm erp_app
docker run -d ... erp-app:rollback
```

### Option 2: Docker Rollback

```bash
# On app server
docker stop erp_app

# List previous images
docker images | grep erp-app

# Run previous image
docker run -d \
    --name erp_app \
    -p 8000:8000 \
    --env-file .env \
    erp-app:previous-version
```

### Option 3: Docker Compose Rollback

```bash
# On app server
cd /opt/erp

# Show git history
git log --oneline

# Revert to previous version
git revert HEAD

# Redeploy
docker-compose down
docker-compose up -d
```

---

## Monitoring After Deployment

### View Logs

```bash
# Real-time logs
docker-compose logs -f app

# Last 100 lines
docker logs --tail 100 erp_app

# Logs with timestamps
docker logs -f --timestamps erp_app
```

### Check Disk Usage

```bash
# Container disk usage
docker exec erp_app du -sh /app/

# Server disk usage
df -h
```

### Monitor Resources

```bash
# CPU and memory usage
docker stats erp_app

# Database size
docker exec erp_db du -sh /var/lib/postgresql/data/
```

### Database Backups

```bash
# Automated backup
docker exec erp_db pg_dump -U erp_user erp_db > /opt/erp/backup-$(date +%Y%m%d).sql

# Check backup
ls -lh /opt/erp/backup-*.sql
```

---

## Performance Optimization

### Enable Caching

```bash
# Update .env
CELERY_BROKER_URL=redis://redis:6379/0
CACHE_TIMEOUT=3600
```

### Database Optimization

```bash
# Analyze query performance
docker-compose exec app python manage.py shell
>>> from django.db import connection
>>> with connection.cursor() as cursor:
...     cursor.execute("ANALYZE;")
```

### Static File Optimization

```bash
# Minimize CSS/JS
pip install django-compressor

# Configure in settings.py
COMPRESS_ENABLED = True
```

---

## Next Steps

1. ✓ Deployment complete
2. Configure domain name and SSL certificate
3. Set up monitoring and alerting
4. Create database backup strategy
5. Document any custom configurations
6. Train users on the system
7. Schedule regular maintenance

---

## Deployment Checklist

- [ ] Prerequisites installed on both servers
- [ ] SSH keys configured and tested
- [ ] GitHub Secrets added
- [ ] Repository pushed to GitHub
- [ ] GitHub Actions workflow triggered
- [ ] All tests passed
- [ ] Docker image built successfully
- [ ] Deployment to app server successful
- [ ] Application accessible at http://app-server-ip:8000
- [ ] Admin panel accessible
- [ ] Database connection verified
- [ ] Static files loading
- [ ] API endpoints responding
- [ ] Logs reviewed for errors
- [ ] Health checks passing

---

**Remember**: Test in a staging environment first before deploying to production!
