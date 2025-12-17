#!/bin/bash
# Ubuntu Server Initial Setup Script
# Run as: sudo bash initial_setup.sh

set -e

echo "=================================="
echo "ERP - Ubuntu Server Setup"
echo "=================================="
echo ""

# Update System
echo "[1/10] Updating system packages..."
apt-get update
apt-get upgrade -y
apt-get install -y curl wget git nano htop unzip build-essential

# Setup Firewall
echo "[2/10] Configuring firewall..."
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 5432/tcp
ufw allow 8000/tcp

# Create Deployment User
echo "[3/10] Creating deployment user..."
useradd -m -s /bin/bash erpadmin || echo "User already exists"
usermod -aG sudo erpadmin || echo "User group already added"

# Configure Timezone
echo "[4/10] Configuring timezone..."
timedatectl set-timezone UTC

# Install Python
echo "[5/10] Installing Python 3.10..."
apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Install PostgreSQL
echo "[6/10] Installing PostgreSQL 15..."
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update
apt-get install -y postgresql-15 postgresql-contrib-15 libpq-dev
systemctl start postgresql
systemctl enable postgresql

# Install Redis
echo "[7/10] Installing Redis..."
apt-get install -y redis-server
systemctl start redis-server
systemctl enable redis-server

# Install Nginx
echo "[8/10] Installing Nginx..."
apt-get install -y nginx
systemctl enable nginx

# Install Certbot for SSL
echo "[9/10] Installing Certbot..."
apt-get install -y certbot python3-certbot-nginx

# Create Application Directory
echo "[10/10] Creating application directory..."
mkdir -p /var/www/erp
chown erpadmin:erpadmin /var/www/erp
mkdir -p /backups/postgresql
chown postgres:postgres /backups/postgresql
chmod 700 /backups/postgresql

echo ""
echo "=================================="
echo "✓ Initial Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Run database setup: sudo bash database_setup.sh"
echo "2. Run app setup: bash app_setup.sh"
echo "3. Run web server setup: sudo bash webserver_setup.sh"
echo ""
