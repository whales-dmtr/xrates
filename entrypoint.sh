#!/bin/sh
set -e  

cd xrates

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python -m gunicorn --bind 0.0.0.0:8000 --workers 3 xrates.asgi:application -k uvicorn.workers.UvicornWorker --timeout 60