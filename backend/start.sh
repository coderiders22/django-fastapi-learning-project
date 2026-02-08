#!/bin/bash

set -e  # Exit immediately if any command fails (safe for production)

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Creating Django superuser (if not exists)..."
python manage.py createsuperuser --noinput || true

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080}
