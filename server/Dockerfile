FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server/config.json config.json
COPY server/server.py .

EXPOSE 5010

CMD ["python", "server.py"] 