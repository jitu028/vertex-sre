#!/bin/bash
set -e

# Usage: ./deployment.sh <PROJECT_ID> [REGION]

if [ -z "$1" ]; then
    echo "Usage: ./deployment.sh <PROJECT_ID> [REGION]"
    echo "Example: ./deployment.sh my-gcp-project us-central1"
    exit 1
fi

PROJECT_ID=$1
REGION=${2:-us-central1}

echo "🚀 Starting Deployment for Project: $PROJECT_ID in Region: $REGION"

# 1. Docker Authentication
echo "🔐 Configuring Docker auth..."
gcloud auth configure-docker --quiet

# 2. Build and Push Backend
echo "🔨 Building Backend..."
docker build -t gcr.io/$PROJECT_ID/vertex-sre-backend:latest backend
echo "⬆️ Pushing Backend..."
docker push gcr.io/$PROJECT_ID/vertex-sre-backend:latest

# 3. Build and Push Frontend
echo "🔨 Building Frontend..."
docker build -t gcr.io/$PROJECT_ID/vertex-sre-frontend:latest frontend
echo "⬆️ Pushing Frontend..."
docker push gcr.io/$PROJECT_ID/vertex-sre-frontend:latest

# 4. Terraform Apply
echo "🌍 Applying Infrastructure with Terraform..."
cd terraform
terraform init
terraform apply -var="project_id=$PROJECT_ID" -var="region=$REGION" -auto-approve

echo "✅ Deployment Complete!"
