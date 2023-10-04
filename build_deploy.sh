#!/bin/bash

# Build the Docker image
docker buildx build --platform linux/amd64 -t bggapi --target runtime .

# Tag the Docker image
docker tag bggapi:latest gcr.io/bggapi/bggapi:latest

# Push the Docker image to Google Container Registry
docker push gcr.io/bggapi/bggapi:latest

# Apply Kubernetes deployment and service YAML files
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml