# backend/Dockerfile
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# System dependencies for psycopg2-binary and others
RUN apt-get update && \
    apt-get install -y gcc libpq-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser --gid=1000 && \
    useradd -r -g appuser --uid=1000 --home-dir=/app --shell=/bin/bash appuser

# Copy all backend files into container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Change ownership of app directory to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
