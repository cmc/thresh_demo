FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY client/ .

ENV SERVER_URL="http://localhost:5010"

ENTRYPOINT ["python", "client.py"] 