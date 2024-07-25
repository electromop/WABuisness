FROM python:3.12-slim

WORKDIR /app
COPY database/ /app/database/
COPY requirements.txt db.env admin_panel.py ./
EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt
CMD python admin_panel.py