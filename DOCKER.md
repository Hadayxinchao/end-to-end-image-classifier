# Docker Usage Guide

## Building the Image

Build the Docker image:
```bash
docker build -t image-classifier:latest .
```

Build with a specific tag:
```bash
docker build -t image-classifier:v1.0 .
```

## Running the Container

### Training

Run training with default configuration:
```bash
docker run --rm image-classifier:latest
```

Run training with custom configuration:
```bash
docker run --rm image-classifier:latest \
  python src/training/train.py \
  hyperparameters.learning_rate=0.001 \
  hyperparameters.num_epochs=10
```

Run with GPU support:
```bash
docker run --rm --gpus all image-classifier:latest
```

### Mounting Volumes

Mount data directory:
```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/reports:/app/reports \
  image-classifier:latest
```

### Inference

Run inference on a single image:
```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  image-classifier:latest \
  python src/models/predict.py \
  --model_path models/simple_cnn_best.pth \
  --image_path data/test_image.jpg \
  --dataset cifar10
```

### Interactive Mode

Run container with bash for debugging:
```bash
docker run --rm -it image-classifier:latest /bin/bash
```

### Running Tests

Run tests inside container:
```bash
docker run --rm image-classifier:latest pytest tests/ -v
```

## Docker Compose (Optional)

Create a `docker-compose.yml` for easier management:

```yaml
version: '3.8'

services:
  training:
    build: .
    image: image-classifier:latest
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./reports:/app/reports
    environment:
      - PYTHONUNBUFFERED=1
    command: python src/training/train.py

  inference:
    build: .
    image: image-classifier:latest
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    command: python src/models/predict.py --help
```

Then run:
```bash
docker-compose up training
```

## Publishing to Registry

### Docker Hub
```bash
# Tag the image
docker tag image-classifier:latest username/image-classifier:latest

# Login
docker login

# Push
docker push username/image-classifier:latest
```

### GitHub Container Registry
```bash
# Tag for GHCR
docker tag image-classifier:latest ghcr.io/username/image-classifier:latest

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u username --password-stdin

# Push
docker push ghcr.io/username/image-classifier:latest
```

## Best Practices

1. **Use multi-stage builds** for smaller images (if needed)
2. **Mount volumes** for data and models instead of copying them
3. **Use .dockerignore** to exclude unnecessary files
4. **Set resource limits** when running:
   ```bash
   docker run --rm --memory="4g" --cpus="2" image-classifier:latest
   ```
5. **Use specific tags** instead of `latest` in production

## Cleaning Up

Remove image:
```bash
docker rmi image-classifier:latest
```

Remove all unused images:
```bash
docker image prune -a
```

Remove all containers and images:
```bash
docker system prune -a
```
