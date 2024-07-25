FROM python:3.12-slim

WORKDIR /app

COPY database/ /app/database/
COPY files/ /app/files/
COPY templates/ /app/templates
COPY requirements.txt .env  config_reader.py create_db.py YaDisk.py main.py states.py db.env ./
EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt

CMD python create_db.py && python main.py