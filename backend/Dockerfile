# backend/Dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# System dependencies for psycopg2-binary and others
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy all backend files into container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
