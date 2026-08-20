#!/bin/sh
set -e

python3 manage.py wait_for_db
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

python3 cpserver.py &

exec gunicorn --bind 0.0.0.0:${PORT:-8000} django-project.wsgi:application