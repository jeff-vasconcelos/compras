# Use a imagem base do Python
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y locales locales-all

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN chmod +x ./docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]
