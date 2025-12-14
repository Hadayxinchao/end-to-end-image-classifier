# Dockerfile for FastAPI serving
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements-ci.txt .
RUN pip install --no-cache-dir -r requirements-ci.txt && \
    pip install --no-cache-dir fastapi uvicorn python-multipart gunicorn

# Copy source code
COPY src/ ./src/
COPY serve/ ./serve/
COPY configs/ ./configs/
COPY setup.py .

# Install package
RUN pip install --no-deps -e .

# Create model directory
RUN mkdir -p /app/models

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "serve.app:app", "--host", "0.0.0.0", "--port", "8000"]
