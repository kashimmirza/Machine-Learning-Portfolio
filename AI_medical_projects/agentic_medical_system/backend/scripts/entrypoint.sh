#!/bin/bash
set -e

# Default to development if not set
APP_ENV=${APP_ENV:-development}

echo "Starting application in $APP_ENV mode..."

# Here we could run database migrations via alembic if we had them
# alembic upgrade head

# Exec the command passed to the container
exec "$@"
