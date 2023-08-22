#!/bin/bash

PROJECT_ID="blumensystems-usgs-pad"
IMAGE_NAME="blumensystems-pad-backend"
IMAGE_TAG="latest"
REGION="us-central1"
SERVICE_NAME="usgs-pad-api"

gcloud config set project $PROJECT_ID

IMAGE_URL="gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG"
echo "Deploying image: $IMAGE_URL"

gcloud run deploy $SERVICE_NAME \
  --image=$IMAGE_URL \
  --platform=managed \
  --region=$REGION \
  --port=8000 \
  --allow-unauthenticated
  --set-env-vars DATABASE_URL=../data/db.sqlite

echo "Service URL:"
gcloud run services describe $SERVICE_NAME --region=$REGION --format "value(status.url)"