# Prerequisites Checklist

Before deploying the ERP system, ensure all prerequisites are met on both app and database servers.

## System Requirements

### Operating System
- Ubuntu 20.04 LTS or 22.04 LTS
- Minimum 2 vCPU cores
- Minimum 4GB RAM (8GB recommended)
- Minimum 20GB disk space (50GB recommended)
- Stable internet connection

## APP SERVER Prerequisites

### 1. System Updates
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Docker and Docker Compose

#### Install Docker
```bash
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install Docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Verify installation
docker --version
```

#### Install Docker Compose
```bash
# Download latest version
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

#### Add User to Docker Group
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Git

```bash
sudo apt-get install -y git

# Configure Git (optional)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. Other Utilities

```bash
sudo apt-get install -y \
    curl \
    wget \
    postgresql-client \
    redis-tools \
    htop \
    vim \
    nano
```

### 5. Directory Structure

Create required directories:

```bash
sudo mkdir -p /opt/erp
sudo mkdir -p /opt/erp/logs
sudo mkdir -p /opt/erp/staticfiles
sudo mkdir -p /opt/erp/media
sudo mkdir -p /opt/erp/postgres_data

# Set permissions
sudo chown $USER:$USER /opt/erp
chmod 755 /opt/erp -R
```

### 6. Docker Network

Create custom Docker network:

```bash
docker network create erp_network
```

### 7. SSH Configuration

Create SSH directory:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

## DATABASE SERVER Prerequisites

### 1. System Updates
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. PostgreSQL Installation

#### Install PostgreSQL 15
```bash
# Add PostgreSQL repository
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update and install
sudo apt-get update
sudo apt-get install -y postgresql-15 postgresql-contrib-15

# Verify installation
psql --version
```

#### Start PostgreSQL
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
```

#### Configure PostgreSQL for Remote Access

Edit PostgreSQL configuration:

```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
```

Change line:
```
#listen_addresses = 'localhost'
```

To:
```
listen_addresses = '*'
```

Edit client authentication:

```bash
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

Add line at end:
```
host    all             all             0.0.0.0/0               md5
```

Restart PostgreSQL:

```bash
sudo systemctl restart postgresql
```

### 3. Create Database and User

```bash
sudo -u postgres psql <<EOF
CREATE DATABASE erp_db;
CREATE USER erp_user WITH PASSWORD 'secure_password_here';

ALTER ROLE erp_user SET client_encoding TO 'utf8';
ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE erp_user SET default_transaction_deferrable TO on;
ALTER ROLE erp_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;

-- For future use, grant additional privileges if needed
ALTER USER erp_user CREATEDB;

\q
EOF
```

### 4. Verify Database Connection

```bash
# Test local connection
psql -U erp_user -d erp_db -h localhost

# Test remote connection (from app server)
psql -U erp_user -d erp_db -h <db-server-ip> -p 5432
```

### 5. Backup Directory

Create backup directory:

```bash
sudo mkdir -p /var/backups/erp_db
sudo chown postgres:postgres /var/backups/erp_db
sudo chmod 700 /var/backups/erp_db
```

### 6. Firewall Configuration

Allow PostgreSQL connections:

```bash
sudo ufw allow 5432/tcp
sudo ufw status

# If using AWS security groups or similar, ensure port 5432 is open
```

## Network Configuration

### App Server to Database Server Communication

Ensure app server can reach database server:

```bash
# Test from app server
telnet <database-server-ip> 5432
# Or
nc -zv <database-server-ip> 5432
```

## SSH Public Key Authentication

### On Local Machine

Generate SSH key pair (if not already done):

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

### Copy Public Keys to Servers

#### For App Server
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub deploy@app-server-ip
```

#### For Database Server
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub deploy@db-server-ip
```

Verify SSH access:

```bash
ssh deploy@app-server-ip
ssh deploy@db-server-ip
```

## Environment Configuration

### Create .env File

On app server:

```bash
cd /opt/erp
cp .env.example .env
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
DB_HOST=<database-server-ip>
DB_PORT=5432
ALLOWED_HOSTS=app.yourdomain.com,yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

## Verification Checklist

### App Server
- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] Git installed and configured
- [ ] SSH key generated and copied
- [ ] Directories created (/opt/erp, logs, media, etc.)
- [ ] Docker network created
- [ ] Can reach database server on port 5432

### Database Server
- [ ] PostgreSQL 15 installed
- [ ] PostgreSQL running and enabled on boot
- [ ] Remote access configured (listen_addresses, pg_hba.conf)
- [ ] Database and user created
- [ ] Can connect locally and remotely
- [ ] Backup directory created
- [ ] Firewall configured for port 5432

### Network Connectivity
- [ ] App server can SSH to database server
- [ ] Database server can be reached on port 5432 from app server
- [ ] Both servers have stable internet connection
- [ ] DNS resolves correctly (if using domain names)

## Troubleshooting

### PostgreSQL Connection Issues

```bash
# Check PostgreSQL is listening
sudo ss -tuln | grep 5432

# Check pg_hba.conf permissions
sudo chmod 644 /etc/postgresql/15/main/pg_hba.conf

# Test connection
sudo -u postgres psql -c "SELECT 1;"
```

### Docker Issues

```bash
# Check Docker daemon
sudo systemctl status docker

# Check Docker network
docker network ls

# Verify Docker user permissions
id $USER
```

### SSH Connection Issues

```bash
# Check SSH service
sudo systemctl status ssh

# Check SSH key permissions
ls -la ~/.ssh/
# Should show: -rw------- (600) for private keys

# Test SSH connection with verbose output
ssh -v deploy@server-ip
```

## Recommended Additional Setup

### Monitoring
- Install monitoring tools (Grafana, Prometheus)
- Setup system alerts

### Backup Strategy
- Automated daily database backups
- Backup retention policy

### SSL/TLS Certificates
- Install Let's Encrypt SSL certificates
- Configure auto-renewal

### Load Balancing (Future)
- Setup Nginx as reverse proxy
- Configure load balancing if needed

## Next Steps

1. Run `README/SSH_SETUP.md` for SSH key configuration
2. Run `README/GITHUB_ACTIONS.md` for GitHub Actions setup
3. Run `README/DEPLOYMENT.md` for deployment instructions
4. Run `README/LOCAL_DEVELOPMENT.md` for local development setup

---

**Important**: Keep all credentials and passwords secure. Never commit sensitive information to version control.
