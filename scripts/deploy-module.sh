#!/bin/bash

# Deploy Single Module
# Usage: ./deploy-module.sh <module_name> <image_tag>

MODULE_NAME=$1
IMAGE_TAG=$2
APP_HOME="/opt/erp"
CONTAINER_NAME="erp_app"
IMAGE_NAME="erp-app:${MODULE_NAME}-${IMAGE_TAG}"

if [ -z "$MODULE_NAME" ] || [ -z "$IMAGE_TAG" ]; then
    echo "Usage: $0 <module_name> <image_tag>"
    exit 1
fi

echo "========================================="
echo "Deploying $MODULE_NAME Module"
echo "========================================="

# Navigate to app directory
cd $APP_HOME

# Stop current container if running
echo "Stopping current container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Load new image
echo "Loading Docker image..."
docker load -i /tmp/docker-image.tar

# Create environment file if doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Run new container
echo "Starting new container with image $IMAGE_NAME..."
docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    --network erp_network \
    -p 8000:8000 \
    --env-file .env \
    -v /opt/erp/static:/app/staticfiles \
    -v /opt/erp/media:/app/media \
    $IMAGE_NAME

# Wait for container to be healthy
echo "Waiting for container to be healthy..."
for i in {1..30}; do
    if docker exec $CONTAINER_NAME curl -s http://localhost:8000/admin/ > /dev/null 2>&1; then
        echo "Container is healthy!"
        break
    fi
    echo "Attempt $i: Waiting for container to be ready..."
    sleep 2
done

echo "========================================="
echo "Deployment of $MODULE_NAME module completed!"
echo "========================================="
