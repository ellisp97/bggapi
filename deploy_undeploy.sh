#!/bin/bash

function deploy_app() {
  # Build the Docker image
  docker buildx build --platform linux/amd64 -t bggapi --target runtime .

  # Tag the Docker image
  docker tag bggapi:latest gcr.io/bggapi/bggapi:latest

  # Push the Docker image to Google Container Registry
  docker push gcr.io/bggapi/bggapi:latest

  # Apply Kubernetes deployment and service YAML files
  kubectl apply -f deployment.yaml
  kubectl apply -f service.yaml
}

function undeploy_app() {
  # Delete Kubernetes deployment and service
  kubectl delete -f deployment.yaml
  kubectl delete -f service.yaml

  # Optionally, you can also delete the Docker image from the registry
  # docker rmi gcr.io/bggapi/bggapi:latest
}

# Check if the user wants to deploy or undeploy
if [ "$1" == "deploy" ]; then
  deploy_app
  echo "Application deployed successfully."
elif [ "$1" == "undeploy" ]; then
  undeploy_app
  echo "Application undeployed successfully."
else
  echo "Usage: $0 [deploy|undeploy]"
  exit 1
fi
