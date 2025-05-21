#!/bin/sh

echo "Waiting for database at $POSTGRES_HOST:$POSTGRES_PORT..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
exec gunicorn --bind 0.0.0.0:8000 django_app.wsgi:application
