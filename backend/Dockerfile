FROM python:3.10-slim

WORKDIR /app

COPY . .
RUN chmod +x ./wait-for-it.sh

RUN pip install --no-cache-dir flask psycopg2-binary flask-cors kafka-python python-dotenv requests

EXPOSE 5000

CMD ["python", "app.py"]
