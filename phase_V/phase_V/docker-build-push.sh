#!/bin/bash

# Docker build and push script for WSL
# Replace 'yourusername' with your actual Docker Hub username

DOCKER_USERNAME="yourusername"

# Check if Docker username is provided as an argument
if [ $# -eq 1 ]; then
    DOCKER_USERNAME=$1
fi

# Check if Docker username is still default
if [ "$DOCKER_USERNAME" = "yourusername" ]; then
    echo "ERROR: Please replace 'yourusername' with your actual Docker Hub username."
    echo "Usage: ./docker-build-push.sh [your-docker-username]"
    echo "Or edit this script to set the DOCKER_USERNAME variable."
    exit 1
fi

echo "Using Docker Hub username: $DOCKER_USERNAME"

# Backend image details
BACKEND_IMAGE_NAME="${DOCKER_USERNAME}/phasev-backend"
BACKEND_TAG="latest"

# Frontend image details
FRONTEND_IMAGE_NAME="${DOCKER_USERNAME}/phasev-frontend"
FRONTEND_TAG="latest"

# Build backend image
echo "Building backend image..."
cd backend
docker build -t $BACKEND_IMAGE_NAME:$BACKEND_TAG .
if [ $? -ne 0 ]; then
    echo "Error building backend image"
    exit 1
fi
echo "Backend image built successfully"

# Return to root directory
cd ..

# Build frontend image
echo "Building frontend image..."
cd frontend
docker build -t $FRONTEND_IMAGE_NAME:$FRONTEND_TAG .
if [ $? -ne 0 ]; then
    echo "Error building frontend image"
    exit 1
fi
echo "Frontend image built successfully"

# Return to root directory
cd ..

# Log in to Docker Hub
echo "Logging in to Docker Hub..."
docker login
if [ $? -ne 0 ]; then
    echo "Error logging in to Docker Hub"
    exit 1
fi

# Push backend image
echo "Pushing backend image..."
docker push $BACKEND_IMAGE_NAME:$BACKEND_TAG
if [ $? -ne 0 ]; then
    echo "Error pushing backend image"
    exit 1
fi
echo "Backend image pushed successfully"

# Push frontend image
echo "Pushing frontend image..."
docker push $FRONTEND_IMAGE_NAME:$FRONTEND_TAG
if [ $? -ne 0 ]; then
    echo "Error pushing frontend image"
    exit 1
fi
echo "Frontend image pushed successfully"

echo "All images built and pushed successfully!"
echo "Backend image: $BACKEND_IMAGE_NAME:$BACKEND_TAG"
echo "Frontend image: $FRONTEND_IMAGE_NAME:$FRONTEND_TAG"