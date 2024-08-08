FROM python:3.12-slim

WORKDIR /app

COPY admin_panel/ /app/admin_panel
COPY main/ /app/main
COPY manage.py requirements.txt ./
COPY templates/ /app/templates

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt


