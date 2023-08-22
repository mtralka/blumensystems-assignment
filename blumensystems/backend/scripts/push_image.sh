#!/bin/bash

IMAGE_NAME="blumensystems-pad-backend"
TAG="latest"

docker tag $IMAGE_NAME:$TAG gcr.io/blumensystems-usgs-pad/$IMAGE_NAME:$TAG
docker push gcr.io/blumensystems-usgs-pad/$IMAGE_NAME:$TAG
