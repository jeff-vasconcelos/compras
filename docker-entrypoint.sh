#!/bin/bash

python3 manage.py migrate

echo "Apply collectstatic --no-input"
python3 manage.py collectstatic --no-input

echo "Starting server"
python manage.py runserver 0.0.0.0:8000

#celery -A setup worker -B --loglevel=info --concurrency=4
celery -A setup worker -l INFO & celery -A setup beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler