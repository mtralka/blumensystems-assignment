#!/bin/bash

TOP="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$TOP")"

isort $APP_DIR --profile black

black $APP_DIR