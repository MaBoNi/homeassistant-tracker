# backend/Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copy backend source only
COPY . /app

# Install system packages for psycopg2-binary and general use
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
