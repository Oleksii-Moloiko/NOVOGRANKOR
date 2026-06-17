#!/usr/bin/env bash
set -o errexit

python manage.py migrate
python manage.py createsuperuser --noinput || true

exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT