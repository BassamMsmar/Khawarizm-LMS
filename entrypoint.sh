#!/bin/sh

# Wait for potential DB startup delay (optional, but good practice)
# sleep 2

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn server
echo "Starting Gunicorn..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000
