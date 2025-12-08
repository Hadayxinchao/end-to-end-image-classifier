# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p /app/data/raw /app/models /app/reports

# Expose port for potential web service
EXPOSE 8000

# Default command - can be overridden
CMD ["python", "src/training/train.py"]

# To run inference instead, override with:
# docker run image-classifier python src/models/predict.py --help
