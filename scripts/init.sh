#!/bin/bash

# ERP System Initial Setup Script
# Run this script after cloning the repository

echo "========================================="
echo "ERP System - Initial Setup"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python3 --version || { echo -e "${RED}Python 3 not found${NC}"; exit 1; }

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate || . venv\Scripts\activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please edit it with your settings.${NC}"
else
    echo -e "${YELLOW}.env file already exists${NC}"
fi

# Create logs directory
mkdir -p logs

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo -e "${GREEN}Docker found${NC}"
    
    # Try to start Docker services
    echo -e "${YELLOW}Starting Docker services...${NC}"
    if docker-compose up -d; then
        echo -e "${GREEN}Docker services started${NC}"
        sleep 5
        
        # Run migrations
        echo -e "${YELLOW}Running database migrations...${NC}"
        python manage.py migrate
        
        echo -e "${GREEN}Setup complete!${NC}"
        echo -e "${YELLOW}Next steps:${NC}"
        echo "1. Edit .env file with your configuration"
        echo "2. Run: python manage.py createsuperuser"
        echo "3. Run: python manage.py runserver"
        echo "4. Visit: http://localhost:8000/admin"
    else
        echo -e "${RED}Docker services failed to start${NC}"
        echo "Please ensure Docker and Docker Compose are running"
    fi
else
    echo -e "${YELLOW}Docker not found. For local development with PostgreSQL:${NC}"
    
    # Check if postgresql-client is available
    if command -v psql &> /dev/null; then
        echo -e "${GREEN}PostgreSQL client found${NC}"
        echo "Run: python manage.py migrate"
        echo "Run: python manage.py createsuperuser"
        echo "Run: python manage.py runserver"
    else
        echo -e "${RED}PostgreSQL client not found${NC}"
        echo "Please install either Docker or PostgreSQL for database"
    fi
fi

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Setup complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "For detailed setup instructions, see:"
echo "- README/05-LOCAL_DEVELOPMENT.md (local development)"
echo "- README/01-PREREQUISITES.md (production prerequisites)"
echo "- README/DEPLOYMENT.md (production deployment)"
