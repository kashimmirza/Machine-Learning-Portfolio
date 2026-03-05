#!/bin/bash
set -e

# Load environment variables from the appropriate .env file if valid
if [ -f ".env.${APP_ENV}" ]; then
    echo "Loading environment from .env.${APP_ENV}"
    export $(grep -v '^#' .env.${APP_ENV} | xargs)
fi

# Check required sensitive environment variables
required_vars=("POSTGRES_USER" "POSTGRES_PASSWORD" "OPENAI_API_KEY")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        missing_vars+=("$var")
    fi
done

if [[ ${#missing_vars[@]} -gt 0 ]]; then
    echo "ERROR: The following required environment variables are missing:"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    exit 1
fi

echo "Starting Application in ${APP_ENV} mode..."
exec "$@"
