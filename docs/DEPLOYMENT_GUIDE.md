# ERP System - Complete Deployment Guide

## Overview

This guide provides step-by-step instructions to deploy your Django ERP system on Ubuntu servers with:
- **Database Server**: PostgreSQL 15 (can be on separate machine)
- **App Server**: Python/Django with Gunicorn
- **Web Server**: Nginx reverse proxy
- **Cache**: Redis for sessions and Celery
- **SSL**: Let's Encrypt with auto-renewal

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Internet / Users                       │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Nginx (Port 443)   │
        │  (Reverse Proxy)    │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │    Gunicorn         │
        │  (Unix Socket)      │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   Django App        │
        │  (Python/DRF)       │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   PostgreSQL 15     │
        │   Redis Server      │
        └─────────────────────┘
```

## Prerequisites

1. **Two Ubuntu 20.04 LTS or 22.04 LTS servers**:
   - Server 1: Database Server (PostgreSQL)
   - Server 2: App Server (Django + Nginx)
   
   OR Single server for all components

2. **Domain name** (for SSL certificate)
3. **SSH access** to both servers
4. **Root or sudo** privileges
5. **Minimum specs**:
   - Database Server: 2GB RAM, 20GB storage
   - App Server: 4GB RAM, 20GB storage

## Step 1: Prepare Your Local Machine

### 1.1 Generate SSH Key Pair
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/erp_deploy_key -N ""
cat ~/.ssh/erp_deploy_key.pub
```

### 1.2 Add Key to Server
```bash
# On your server, add the public key
mkdir -p ~/.ssh
echo "your-public-key-content" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

### 1.3 Test SSH Connection
```bash
ssh -i ~/.ssh/erp_deploy_key root@your-server-ip
```

## Step 2: Initial Server Setup

### 2.1 Run Initial Setup Script
```bash
# Copy script to server
scp -i ~/.ssh/erp_deploy_key scripts/initial_setup.sh root@your-server-ip:/tmp/

# Run on server
ssh -i ~/.ssh/erp_deploy_key root@your-server-ip "sudo bash /tmp/initial_setup.sh"
```

Or run manually:
```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl wget git nano htop build-essential
```

## Step 3: Database Server Setup

### 3.1 Run Database Setup Script
```bash
scp -i ~/.ssh/erp_deploy_key scripts/database_setup.sh root@your-db-server:/tmp/
ssh -i ~/.ssh/erp_deploy_key root@your-db-server "sudo bash /tmp/database_setup.sh"
```

**Save the credentials** it generates!

### 3.2 Verify Database Connection
```bash
ssh -i ~/.ssh/erp_deploy_key root@your-db-server
sudo -u postgres psql -c "SELECT version();"
```

## Step 4: Application Server Setup

### 4.1 Clone Repository
```bash
ssh -i ~/.ssh/erp_deploy_key erpadmin@your-app-server

cd /var/www/erp
git clone https://github.com/your-org/erp-system.git .
# or download as zip and extract
```

### 4.2 Run App Setup Script
```bash
scp -i ~/.ssh/erp_deploy_key scripts/app_setup.sh erpadmin@your-app-server:/tmp/
ssh -i ~/.ssh/erp_deploy_key erpadmin@your-app-server "bash /tmp/app_setup.sh"
```

### 4.3 Configure Environment Variables
```bash
ssh -i ~/.ssh/erp_deploy_key erpadmin@your-app-server

cd /var/www/erp
cp .env.template .env
nano .env
```

Update with your credentials:
```bash
DEBUG=False
SECRET_KEY=$(openssl rand -base64 32)
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_NAME=erp_db
DATABASE_USER=erp_user
DATABASE_PASSWORD=your_generated_password
DATABASE_HOST=your-db-server-ip
DATABASE_PORT=5432
```

### 4.4 Run Migrations
```bash
cd /var/www/erp
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 4.5 Test Django Locally
```bash
python manage.py runserver 127.0.0.1:8000
```

## Step 5: Web Server Setup

### 5.1 Run Web Server Setup Script
```bash
scp -i ~/.ssh/erp_deploy_key scripts/webserver_setup.sh root@your-app-server:/tmp/
ssh -i ~/.ssh/erp_deploy_key root@your-app-server "sudo bash /tmp/webserver_setup.sh"
```

### 5.2 Verify Services
```bash
ssh -i ~/.ssh/erp_deploy_key root@your-app-server

sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis-server
```

## Step 6: SSL Certificate Setup

### 6.1 Obtain Certificate
```bash
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com
# or with Nginx
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

### 6.2 Verify Certificate
```bash
sudo ls -la /etc/letsencrypt/live/your-domain.com/
```

### 6.3 Auto-Renewal
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
sudo certbot renew --dry-run
```

## Step 7: Production Deployment

### 7.1 Update Django Settings
```bash
ssh -i ~/.ssh/erp_deploy_key erpadmin@your-app-server

cd /var/www/erp
nano core/settings.py
```

Update settings:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 7.2 Restart Services
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### 7.3 Verify Deployment
```bash
curl https://your-domain.com/api/dashboard/dashboards/
# Should return JSON response
```

## Step 8: Monitoring & Maintenance

### 8.1 Check Service Status
```bash
# On app server
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status redis-server

# On database server
sudo systemctl status postgresql
```

### 8.2 View Logs
```bash
# Django/Gunicorn
sudo journalctl -u gunicorn -f

# Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# System
dmesg | tail -20
```

### 8.3 Database Backup
```bash
# Manual backup
sudo -u postgres pg_dump -Fc erp_db > /backups/postgresql/erp_db_$(date +%Y%m%d).dump

# List backups
sudo ls -lh /backups/postgresql/

# Restore
sudo -u postgres pg_restore -d erp_db /backups/postgresql/erp_db_*.dump
```

### 8.4 Monitor Disk Space
```bash
# Check disk usage
df -h
du -sh /var/www/erp
du -sh /var/lib/postgresql

# Clean up old backups
sudo find /backups/postgresql -mtime +30 -delete
```

### 8.5 Performance Monitoring
```bash
# Memory & CPU
top
htop

# Network connections
netstat -an | grep ESTABLISHED

# Open files
lsof -i :443
lsof -i :5432
```

## Step 9: Continuous Deployment (Optional)

### 9.1 Setup GitHub Actions
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            cd /var/www/erp
            git pull origin main
            source venv/bin/activate
            pip install -r requirements.txt
            python manage.py migrate
            python manage.py collectstatic --noinput
            sudo systemctl restart gunicorn
```

### 9.2 Configure Secrets in GitHub
Settings → Secrets and variables → Actions:
- `SERVER_HOST`: your-app-server-ip
- `SERVER_USER`: erpadmin
- `DEPLOY_KEY`: your-private-key-content

## Troubleshooting

### Gunicorn Connection Refused
```bash
sudo systemctl status gunicorn.socket
sudo journalctl -u gunicorn -f
# Check socket file
ls -la /run/gunicorn.sock
```

### Database Connection Failed
```bash
# Test database connection
sudo -u postgres psql -h localhost -U erp_user -d erp_db -c "SELECT 1;"
# Check firewall
sudo ufw status
```

### Nginx 502 Bad Gateway
```bash
# Check if Gunicorn is running
ps aux | grep gunicorn
# Check socket
sudo systemctl restart gunicorn.socket gunicorn.service
```

### SSL Certificate Issues
```bash
# List certificates
sudo certbot certificates
# Renew manually
sudo certbot renew --force-renewal
# Check renewal logs
sudo journalctl -u certbot -f
```

### Permission Denied Errors
```bash
# Fix ownership
sudo chown -R erpadmin:www-data /var/www/erp
# Fix permissions
sudo chmod -R 755 /var/www/erp
sudo chmod -R 755 /var/www/erp/media
sudo chmod -R 755 /var/www/erp/static
```

## Performance Optimization

### 1. Gunicorn Workers
```bash
# Recommended: 2 × CPU cores + 1
# In gunicorn.service:
# --workers 9  (for 4 core CPU)
```

### 2. Database Optimization
```bash
# Vacuum and analyze
sudo -u postgres vacuumdb -z erp_db

# Check slow queries
# In postgresql.conf:
# log_min_duration_statement = 1000  # 1 second
```

### 3. Redis Optimization
```bash
# Configure persistence
sudo nano /etc/redis/redis.conf
# save 900 1
# save 300 10
# save 60 10000
```

### 4. Nginx Caching
```nginx
# Add to Nginx config
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;

location /api/ {
    proxy_cache my_cache;
    proxy_cache_valid 200 1m;
}
```

## Security Hardening

### 1. SSH Security
```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# PermitRootLogin no
# PasswordAuthentication no

sudo systemctl restart sshd
```

### 2. Firewall Rules
```bash
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 3. Fail2Ban
```bash
sudo apt-get install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 4. Auto-Update
```bash
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Rollback Procedure

If deployment fails:
```bash
cd /var/www/erp
git log --oneline -10
git checkout previous-commit-hash
source venv/bin/activate
python manage.py migrate
sudo systemctl restart gunicorn
```

## Support & Documentation

- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Nginx: https://nginx.org/en/docs/
- Gunicorn: https://docs.gunicorn.org/

---

**Last Updated**: December 17, 2024
**Version**: 1.0
