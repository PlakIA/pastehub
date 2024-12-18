#!/bin/sh

set -e

echo "Applying Migrations..."
python manage.py migrate --noinput

echo "Static Collecting..."
python manage.py collectstatic --noinput

echo "Messages Compiling..."
python manage.py compilemessages --noinput

echo "Start gunicorn"
exec gunicorn pastehub.wsgi:application --workers=$GUNICORN_WORKERS --bind 0.0.0.0:$PORT