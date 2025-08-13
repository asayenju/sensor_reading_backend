FROM python:3.11-slim

WORKDIR /app/api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command (can be overridden in docker-compose)
CMD ["python", "producer.py"]
