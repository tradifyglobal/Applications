#!/bin/bash

# Setup PostgreSQL Database Server
# Run this script on the database server

echo "========================================="
echo "Setting up PostgreSQL Database Server"
echo "========================================="

# Update system
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install PostgreSQL
echo "Installing PostgreSQL 15..."
sudo apt-get install -y postgresql postgresql-contrib

# Start PostgreSQL
echo "Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
echo "Creating ERP database and user..."
sudo -u postgres psql <<EOF
CREATE DATABASE erp_db;
CREATE USER erp_user WITH PASSWORD 'erp_password';
ALTER ROLE erp_user SET client_encoding TO 'utf8';
ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE erp_user SET default_transaction_deferrable TO on;
ALTER ROLE erp_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;
EOF

# Configure PostgreSQL for remote connections
echo "Configuring PostgreSQL for remote connections..."
sudo bash -c 'echo "host    all             all             0.0.0.0/0               md5" >> /etc/postgresql/15/main/pg_hba.conf'
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/15/main/postgresql.conf

# Restart PostgreSQL
echo "Restarting PostgreSQL..."
sudo systemctl restart postgresql

# Create backup directory
echo "Creating backup directory..."
sudo mkdir -p /var/backups/erp_db
sudo chown postgres:postgres /var/backups/erp_db

echo "========================================="
echo "PostgreSQL Database Server setup completed!"
echo "Database: erp_db"
echo "User: erp_user"
echo "========================================="
