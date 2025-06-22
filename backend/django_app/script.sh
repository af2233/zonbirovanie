#!/bin/sh

echo "Waiting for database at $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
exec gunicorn --bind 0.0.0.0:8000 django_app.wsgi
