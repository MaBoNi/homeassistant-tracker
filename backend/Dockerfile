# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy only the backend folder content
COPY . /app

# Update packages and install any additional packages for DEV
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Assuming your requirements.txt is in the project_root
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --upgrade --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
