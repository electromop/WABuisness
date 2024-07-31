FROM python:3.12-slim

WORKDIR /app

COPY database/ /app/database/
COPY files/ /app/files/
COPY requirements.txt .env  config_reader.py create_db.py YaDisk.py main.py states.py db.env restarter.py script.pid ./
EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt

CMD python create_db.py && python restarter.py