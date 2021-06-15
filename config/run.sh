#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --settings=${SETTINGS}

echo "Run Gunicorn"
#python manage.py runserver 0:${PORT} --settings=${SETTINGS}
gunicorn --workers=4 -b 0.0.0.0:${PORT} i2amparis.wsgi:application
