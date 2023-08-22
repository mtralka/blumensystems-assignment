#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

echo "SCRIPT_DIR: $SCRIPT_DIR"
echo "APP_DIR: $APP_DIR"

uvicorn "$APP_DIR/api.main:app" --reload