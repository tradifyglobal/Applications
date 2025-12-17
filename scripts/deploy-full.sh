#!/bin/bash

# Deploy Full Application
# Usage: ./deploy-full.sh

APP_HOME="/opt/erp"
DOCKER_COMPOSE_FILE="$APP_HOME/docker-compose.yml"

echo "========================================="
echo "Deploying Full ERP Application"
echo "========================================="

# Navigate to app directory
cd $APP_HOME

# Create environment file if doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env file with your configuration!"
fi

# Pull latest images
echo "Pulling latest Docker images..."
docker compose pull

# Create/update containers
echo "Starting containers..."
docker compose up -d

# Run migrations
echo "Running database migrations..."
docker compose exec -T app python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker compose exec -T app python manage.py collectstatic --noinput

# Create superuser (optional)
# docker compose exec -T app python manage.py shell -c \
#     "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" \
#     || echo "Superuser already exists or error occurred"

echo "========================================="
echo "Deployment completed!"
echo "Application is running at http://localhost:8000"
echo "Admin panel at http://localhost:8000/admin"
echo "========================================="
