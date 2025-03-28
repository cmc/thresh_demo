FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server/ .

EXPOSE 5010

CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "5010"] 