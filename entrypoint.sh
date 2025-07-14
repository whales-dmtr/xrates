#!/bin/bash

echo "Starting app..."
exec sh -c '
python3 xrates/manage.py migrate && 
python xrates/manage.py collectstatic --noinput &&
python3 xrates/manage.py runserver 0.0.0.0:8000
'