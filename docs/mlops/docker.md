# Docker Containerization

Package and deploy the application using Docker.

## Overview

Docker containerizes the application with all dependencies for consistent deployment across environments.

## Dockerfile

Our multi-stage Dockerfile optimizes image size:

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Create wheels
RUN pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install Python packages
RUN pip install --no-cache /wheels/*

# Copy application
COPY . .

# Install package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data models reports outputs

# Set entrypoint
ENTRYPOINT ["python", "src/training/train.py"]
```

## Building Images

### Build Image

```bash
# Build with default tag
docker build -t image-classifier .

# Build with custom tag
docker build -t image-classifier:v1.0 .

# Build with build args
docker build --build-arg PYTHON_VERSION=3.10 -t image-classifier .
```

### View Images

```bash
# List images
docker images | grep image-classifier

# View image info
docker inspect image-classifier
```

## Running Containers

### Basic Training

```bash
# Run default training (CIFAR-10)
docker run --rm image-classifier

# Run with GPU support
docker run --rm --gpus all image-classifier

# Run on MNIST
docker run --rm image-classifier data=mnist
```

### With Volume Mounts

```bash
# Mount data directory
docker run --rm \
    -v /home/user/data:/app/data \
    image-classifier

# Mount models directory
docker run --rm \
    -v /home/user/models:/app/models \
    image-classifier

# Mount all project directories
docker run --rm \
    -v /home/user/project:/app \
    image-classifier
```

### Interactive Mode

```bash
# Open bash shell
docker run --rm -it \
    --entrypoint /bin/bash \
    image-classifier

# Run custom command
docker run --rm -it \
    --entrypoint python \
    image-classifier \
    -c "from src.models.model import get_model; print(get_model('simple_cnn'))"
```

### Environmental Variables

```bash
# Pass configuration via environment
docker run --rm \
    -e CUDA_VISIBLE_DEVICES=0 \
    -e PYTHONUNBUFFERED=1 \
    image-classifier
```

## Environment Variables

### Useful Variables

```bash
# Python settings
PYTHONUNBUFFERED=1        # Unbuffered output
PYTHONDONTWRITEBYTECODE=1 # Don't create .pyc files

# GPU settings
CUDA_VISIBLE_DEVICES=0    # Use specific GPU

# Application settings
LOG_LEVEL=INFO            # Logging level
```

## Multi-GPU Training

### Single GPU

```bash
docker run --rm --gpus device=0 image-classifier
```

### Multiple GPUs

```bash
# GPU 0 and 1
docker run --rm --gpus '"device=0,1"' image-classifier
```

### All GPUs

```bash
docker run --rm --gpus all image-classifier
```

## Docker Compose

### Multi-service Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  training:
    build: .
    image: image-classifier:latest
    container_name: image-classifier-train
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./reports:/app/reports
    environment:
      - CUDA_VISIBLE_DEVICES=0
    command: data=cifar10 hyperparameters.num_epochs=50

  inference:
    build: .
    image: image-classifier:latest
    container_name: image-classifier-inference
    volumes:
      - ./models:/app/models
    ports:
      - "8000:8000"
    command: python src/api/serve.py
    depends_on:
      - training
```

### Run with Docker Compose

```bash
# Start services
docker-compose up

# Run specific service
docker-compose up training

# Background mode
docker-compose up -d

# View logs
docker-compose logs -f training

# Stop services
docker-compose down
```

## Publishing Images

### Docker Hub

```bash
# Tag image
docker tag image-classifier:latest yourusername/image-classifier:latest

# Login to Docker Hub
docker login

# Push image
docker push yourusername/image-classifier:latest

# Pull image
docker pull yourusername/image-classifier:latest
```

## Performance Optimization

### Reduce Image Size

Current optimizations:
- Multi-stage build (~500MB final image)
- Python slim base image
- Remove build dependencies
- Minimal runtime dependencies

### Speed Up Builds

```bash
# Use BuildKit
DOCKER_BUILDKIT=1 docker build -t image-classifier .

# Cache layers efficiently
# Put dependencies early in Dockerfile
# Order: base image → system deps → python deps → app code
```

## Debugging

### View Image Layers

```bash
# List image history
docker history image-classifier

# Inspect layer details
docker inspect image-classifier
```

### Run with Debugging

```bash
# Keep container running
docker run --rm -it \
    --entrypoint /bin/bash \
    image-classifier

# Inside container
python -m pdb src/training/train.py
```

### View Container Logs

```bash
# Run and see logs
docker run --rm image-classifier

# View logs of stopped container
docker logs container-id
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Build Docker Image

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build image
        run: docker build -t image-classifier .
      
      - name: Run tests in container
        run: docker run --rm image-classifier pytest
```

## Cleanup

### Remove Images and Containers

```bash
# Remove container
docker rm container-id

# Remove image
docker rmi image-classifier

# Remove unused images
docker image prune

# Remove everything
docker system prune -a
```

## Troubleshooting

### Out of Memory

```bash
# Limit memory usage
docker run --rm -m 4g image-classifier

# Check memory usage
docker stats
```

### GPU Not Available

```bash
# Check GPU access
docker run --rm --gpus all nvidia-smi

# Verify nvidia-docker installation
nvidia-docker --version
```

### Large Build Sizes

```bash
# Use .dockerignore to exclude files
# Similar to .gitignore

# Check what's included
docker build --progress=plain .
```

## Best Practices

1. **Use specific base image versions**
   ```dockerfile
   FROM python:3.11-slim  # ✓ Good (specific)
   FROM python:3.11      # ✗ Could be unstable
   ```

2. **Minimize layers**
   ```dockerfile
   # ✓ Good - fewer layers
   RUN apt-get update && \
       apt-get install -y curl && \
       rm -rf /var/lib/apt/lists/*
   
   # ✗ Bad - more layers
   RUN apt-get update
   RUN apt-get install -y curl
   RUN rm -rf /var/lib/apt/lists/*
   ```

3. **Use .dockerignore**
   ```
   __pycache__
   *.pyc
   .git
   .gitignore
   README.md
   .venv
   ```

4. **Set proper entrypoint**
   ```dockerfile
   # ✓ Good - exec form (PID 1)
   ENTRYPOINT ["python", "src/training/train.py"]
   
   # ✗ Bad - shell form
   ENTRYPOINT python src/training/train.py
   ```

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
- [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)
