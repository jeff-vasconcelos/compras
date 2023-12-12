#!/bin/bash

# Aplicar migrações
python3.8 manage.py migrate

# Iniciar o servidor de desenvolvimento do Django em segundo plano
python3.8 manage.py runserver &

# Iniciar o Celery worker
celery -A setup worker -l info &

echo "Ambiente de desenvolvimento iniciado. Acesse http://127.0.0.1:8000/ no navegador."
