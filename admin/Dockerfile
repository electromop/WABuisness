FROM python:3.12-slim

WORKDIR /app

COPY admin_panel/ /app/admin_panel
COPY main/ /app/main
COPY manage.py requirements.txt ./

EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py runserver 0.0.0.0:5000