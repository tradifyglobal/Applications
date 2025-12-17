#!/bin/bash
# Database Setup Script for PostgreSQL
# Run as: sudo bash database_setup.sh

set -e

echo "=================================="
echo "PostgreSQL Database Setup"
echo "=================================="
echo ""

# Database Configuration
DB_NAME="erp_db"
DB_USER="erp_user"
DB_PASSWORD="$(openssl rand -base64 32)"
DB_HOST="localhost"
DB_PORT="5432"

echo "Creating database and user..."
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo ""

# Create database and user
sudo -u postgres psql << EOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
CREATE DATABASE $DB_NAME OWNER $DB_USER;
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET default_transaction_deferrable TO on;
ALTER ROLE $DB_USER SET timezone TO 'UTC';
EOF

echo "✓ Database and user created"
echo ""

# Configure PostgreSQL for Remote Connections
echo "Configuring PostgreSQL for remote connections..."
CONFIG_FILE="/etc/postgresql/15/main/postgresql.conf"
PG_HBA="/etc/postgresql/15/main/pg_hba.conf"

# Backup config files
cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"
cp "$PG_HBA" "${PG_HBA}.backup"

# Update postgresql.conf
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" "$CONFIG_FILE"

# Add connection rule to pg_hba.conf
echo "host    $DB_NAME    $DB_USER    0.0.0.0/0    md5" >> "$PG_HBA"

systemctl restart postgresql
echo "✓ PostgreSQL configured"
echo ""

# Setup Automated Backups
echo "Setting up automated backups..."
crontab -u postgres -l | grep -v "pg_dump" | crontab -u postgres - || true
(crontab -u postgres -l 2>/dev/null; echo "0 2 * * * /usr/bin/pg_dump -Fc $DB_NAME > /backups/postgresql/${DB_NAME}_\$(date +\%Y\%m\%d_\%H\%M\%S).dump") | crontab -u postgres -
(crontab -u postgres -l 2>/dev/null; echo "0 3 * * 0 find /backups/postgresql -mtime +30 -delete") | crontab -u postgres -

echo "✓ Backup schedule configured"
echo ""

echo "=================================="
echo "✓ Database Setup Complete!"
echo "=================================="
echo ""
echo "Save these credentials:"
echo "DATABASE_NAME=$DB_NAME"
echo "DATABASE_USER=$DB_USER"
echo "DATABASE_PASSWORD=$DB_PASSWORD"
echo "DATABASE_HOST=$DB_HOST"
echo "DATABASE_PORT=$DB_PORT"
echo ""
echo "Add them to your .env file"
echo ""
