# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy minimal requirements first for better caching
COPY requirements-ci.txt .

# Install Python dependencies (use CI requirements - lighter)
RUN pip install --no-cache-dir -r requirements-ci.txt

# Copy only necessary source files (not entire project)
COPY setup.py .
COPY src/ ./src/
COPY configs/ ./configs/

# Install the package
RUN pip install --no-deps -e .

# Create necessary directories
RUN mkdir -p /app/data/raw /app/models /app/reports

# Expose port for potential web service
EXPOSE 8000

# Default command - can be overridden
CMD ["python", "src/training/train.py"]

# To run inference instead, override with:
# docker run image-classifier python src/models/predict.py --help
