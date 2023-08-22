#!/bin/bash

TOP="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$TOP")"

IMAGE_NAME="blumensystems-pad-backend"
TAG="latest"

docker build -t "$IMAGE_NAME":"$TAG" "$APP_DIR"