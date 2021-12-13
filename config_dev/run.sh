#!/usr/bin/env bash
#This file uses the container's environment variables found in .env_app_dev
echo 'Waiting for Postgres...'
while ! nc -z ${SQL_HOST} 5432; do
  sleep 0.1
done

echo 'Clearing the database...'
python manage.py flush --no-input
echo 'Applying migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --noinput --settings=${SETTINGS}

echo "Run Gunicorn"
python manage.py runserver 0:${PORT} --settings=${SETTINGS}
#gunicorn --workers=4 -b 0.0.0.0:${PORT} i2amparis.wsgi:application
