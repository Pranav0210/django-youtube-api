#!/bin/sh

echo "Waiting for database..."
sleep 5

python manage.py migrate

exec "$@"
