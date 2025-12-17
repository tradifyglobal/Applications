# Ubuntu Server Setup Guide for ERP Deployment

## Prerequisites
- Ubuntu 20.04 LTS or 22.04 LTS server
- Root or sudo access
- SSH access to the server
- Minimum 4GB RAM, 20GB storage

## Table of Contents
1. [Initial Server Setup](#initial-server-setup)
2. [Database Server Setup](#database-server-setup)
3. [App Server Setup](#app-server-setup)
4. [Web Server Setup (Nginx)](#web-server-setup)
5. [SSL Certificate Setup](#ssl-certificate-setup)
6. [Deployment](#deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Initial Server Setup

### 1. Update System Packages
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y curl wget git nano htop
```

### 2. Configure Firewall (UFW)
```bash
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5432/tcp  # PostgreSQL
sudo ufw allow 8000/tcp  # Django (for testing)
```

### 3. Create Deployment User
```bash
sudo useradd -m -s /bin/bash erpadmin
sudo usermod -aG sudo erpadmin
sudo passwd erpadmin
```

### 4. Generate SSH Keys
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/erp_deploy_key -N ""
# Copy public key to server: cat ~/.ssh/erp_deploy_key.pub
```

### 5. Configure Timezone
```bash
sudo timedatectl set-timezone UTC
sudo timedatectl status
```

---

## Database Server Setup

### 1. Install PostgreSQL 15
```bash
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y postgresql-15 postgresql-contrib-15
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create Database User & Database
```bash
sudo -u postgres psql << EOF
CREATE USER erp_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE erp_db OWNER erp_user;
ALTER ROLE erp_user SET client_encoding TO 'utf8';
ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE erp_user SET default_transaction_deferrable TO on;
ALTER ROLE erp_user SET default_transaction_level TO 'read committed';
ALTER ROLE erp_user SET timezone TO 'UTC';
EOF
```

### 3. Configure PostgreSQL for Remote Connections
Edit `/etc/postgresql/15/main/postgresql.conf`:
```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
```
Find and modify:
```
listen_addresses = '*'
```

Edit `/etc/postgresql/15/main/pg_hba.conf`:
```bash
sudo nano /etc/postgresql/15/main/pg_hba.conf
```
Add line:
```
host    erp_db    erp_user    0.0.0.0/0    md5
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### 4. Create Backup Directory
```bash
sudo mkdir -p /backups/postgresql
sudo chown postgres:postgres /backups/postgresql
sudo chmod 700 /backups/postgresql
```

### 5. Setup Automated Backups
```bash
sudo crontab -u postgres -e
```
Add:
```
0 2 * * * /usr/bin/pg_dump -Fc erp_db > /backups/postgresql/erp_db_$(date +\%Y\%m\%d_\%H\%M\%S).dump
0 3 * * 0 find /backups/postgresql -mtime +30 -delete
```

---

## App Server Setup

### 1. Install Python & Dependencies
```bash
sudo apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip
sudo apt-get install -y libpq-dev gcc postgresql-client
```

### 2. Create Application Directory
```bash
sudo mkdir -p /var/www/erp
sudo chown erpadmin:erpadmin /var/www/erp
cd /var/www/erp
```

### 3. Create Python Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
```

### 4. Install Python Dependencies
```bash
pip install Django==4.2.0 \
    djangorestframework==3.14.0 \
    django-cors-headers==4.0.0 \
    django-filter==23.1 \
    drf-yasg==1.21.6 \
    djangorestframework-simplejwt==5.2.2 \
    psycopg2-binary==2.9.6 \
    gunicorn==20.1.0 \
    whitenoise==6.4.0 \
    python-dotenv==1.0.0 \
    celery==5.2.7 \
    redis==4.5.5
```

### 5. Clone ERP Repository
```bash
cd /var/www/erp
git clone https://github.com/your-org/erp-system.git .
```

### 6. Configure Environment Variables
Create `.env` file:
```bash
nano /var/www/erp/.env
```
Content:
```
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=erp_db
DATABASE_USER=erp_user
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

### 7. Run Django Migrations
```bash
cd /var/www/erp
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 8. Create Gunicorn Socket & Service Files

Create `/etc/systemd/system/gunicorn.socket`:
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
Content:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=127.0.0.1:8000
Accept=false

[Install]
WantedBy=sockets.target
```

Create `/etc/systemd/system/gunicorn.service`:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Content:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=erpadmin
Group=www-data
WorkingDirectory=/var/www/erp
ExecStart=/var/www/erp/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind unix:/run/gunicorn.sock \
    core.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
KillSignal=SIGQUIT

[Install]
WantedBy=multi-user.target
```

Enable services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn.socket gunicorn.service
sudo systemctl start gunicorn.socket gunicorn.service
```

### 9. Install Redis (for Caching & Celery)
```bash
sudo apt-get install -y redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 10. Setup Celery Worker
Create `/etc/systemd/system/celery.service`:
```bash
sudo nano /etc/systemd/system/celery.service
```
Content:
```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=erpadmin
Group=www-data
WorkingDirectory=/var/www/erp
ExecStart=/var/www/erp/venv/bin/celery -A core worker -l info
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Web Server Setup (Nginx)

### 1. Install Nginx
```bash
sudo apt-get install -y nginx
sudo systemctl enable nginx
```

### 2. Create Nginx Configuration
Create `/etc/nginx/sites-available/erp`:
```bash
sudo nano /etc/nginx/sites-available/erp
```
Content:
```nginx
upstream erp {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 20M;

    location /static/ {
        alias /var/www/erp/static/;
    }

    location /media/ {
        alias /var/www/erp/media/;
    }

    location / {
        proxy_pass http://erp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable configuration:
```bash
sudo ln -s /etc/nginx/sites-available/erp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

---

## SSL Certificate Setup

### 1. Install Certbot
```bash
sudo apt-get install -y certbot python3-certbot-nginx
```

### 2. Obtain SSL Certificate
```bash
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com
```

### 3. Update Nginx Configuration
Update `/etc/nginx/sites-available/erp`:
```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # ... rest of configuration
}

server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 4. Setup Auto-Renewal
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Deployment

### 1. Deploy from Git
```bash
cd /var/www/erp
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### 2. Create Deployment Script
Create `/var/www/erp/deploy.sh`:
```bash
#!/bin/bash
set -e

cd /var/www/erp
source venv/bin/activate

echo "Pulling latest code..."
git pull origin main

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting services..."
sudo systemctl restart gunicorn
sudo systemctl restart celery

echo "Deployment completed!"
```

Make executable:
```bash
chmod +x /var/www/erp/deploy.sh
```

---

## Monitoring & Maintenance

### 1. Check Service Status
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis-server
sudo systemctl status celery
```

### 2. View Logs
```bash
# Gunicorn logs
sudo journalctl -u gunicorn -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Django logs
tail -f /var/www/erp/logs/django.log
```

### 3. Performance Monitoring
```bash
# Memory & CPU
htop

# Disk usage
df -h

# Database size
sudo -u postgres psql -d erp_db -c "SELECT pg_size_pretty(pg_database_size('erp_db'));"
```

### 4. Backup Strategy
```bash
# Manual full backup
sudo -u postgres pg_dump -Fc erp_db > /backups/erp_db_backup.dump

# Restore from backup
sudo -u postgres pg_restore -d erp_db /backups/erp_db_backup.dump
```

### 5. Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get autoremove -y
```

---

## Troubleshooting

### Django Not Connecting to Database
```bash
# Test connection
sudo -u postgres psql -h localhost -U erp_user -d erp_db -c "SELECT 1;"
```

### Gunicorn Socket Error
```bash
# Remove old socket file
sudo rm /run/gunicorn.sock
sudo systemctl restart gunicorn.socket
```

### Nginx Connection Refused
```bash
# Check if gunicorn is running
sudo systemctl status gunicorn
# Restart both
sudo systemctl restart gunicorn nginx
```

### Permission Denied Errors
```bash
# Fix permissions
sudo chown -R erpadmin:www-data /var/www/erp
sudo chmod -R 755 /var/www/erp
sudo chmod -R 755 /var/www/erp/media
```

### Database Disk Full
```bash
# Check disk space
df -h /var/lib/postgresql/

# Vacuum database
sudo -u postgres vacuumdb -z erp_db
```

---

## Quick Reference Commands

```bash
# Start/Stop/Restart Services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart postgresql
sudo systemctl restart redis-server

# View Real-time Status
watch -n 1 'sudo systemctl status gunicorn'

# Run Django Management Commands
cd /var/www/erp && source venv/bin/activate
python manage.py createsuperuser
python manage.py shell
python manage.py dbshell

# Database Queries
sudo -u postgres psql -d erp_db
```

---

## Security Checklist

- [ ] Change default passwords
- [ ] Setup SSH key authentication
- [ ] Disable password SSH login
- [ ] Configure firewall rules
- [ ] Setup SSL/TLS certificates
- [ ] Enable automatic security updates
- [ ] Configure Django DEBUG=False
- [ ] Setup backup strategy
- [ ] Enable audit logging
- [ ] Regular security patches
