#!/bin/bash

# Parar o Celery worker
pkill -f "celery -A setup worker"

# Parar o servidor de desenvolvimento do Django
pkill -f "python manage.py runserver"

echo "Ambiente de desenvolvimento encerrado."
