#!/bin/bash

# Setup Remote Servers
# This script should be run on the remote servers to prepare them for deployment

echo "========================================="
echo "Setting up Remote Server"
echo "========================================="

# Update system
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
echo "Adding user to docker group..."
sudo usermod -aG docker $USER
newgrp docker

# Install other dependencies
echo "Installing additional dependencies..."
sudo apt-get install -y git curl wget postgresql-client redis-tools

# Create application directory
echo "Creating application directory..."
sudo mkdir -p /opt/erp
sudo chown $USER:$USER /opt/erp

# Create logs directory
echo "Creating logs directory..."
mkdir -p /opt/erp/logs

# Create Docker network
echo "Creating Docker network..."
docker network create erp_network || true

# Create storage directories
echo "Creating storage directories..."
mkdir -p /opt/erp/staticfiles
mkdir -p /opt/erp/media
mkdir -p /opt/erp/postgres_data

echo "========================================="
echo "Server setup completed!"
echo "========================================="
