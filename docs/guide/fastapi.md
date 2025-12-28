# FastAPI Web Interface Guide

## Overview

The project now includes a FastAPI-based web interface for image classification with a beautiful, interactive UI.

## Features

- 🎨 **Modern UI** - Beautiful gradient design with drag-and-drop support
- 🚀 **Fast API** - RESTful API built with FastAPI
- 📊 **Real-time Results** - Instant predictions with confidence scores
- 🎯 **Batch Processing** - Support for multiple image uploads
- 📱 **Responsive** - Works on desktop and mobile devices

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API Server

```bash
# Run directly
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using Python
python -m src.app.main
```

### 3. Access the Interface

Open your browser and navigate to:
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Using the Web Interface

1. **Upload Image**:
   - Click the upload area or drag and drop an image
   - Supports JPG, PNG (max 5MB)

2. **Classify**:
   - Click "Classify Image" button
   - Wait for results

3. **View Results**:
   - Predicted class with confidence score
   - Visual confidence bar
   - All class probabilities ranked

## API Endpoints

### GET `/`
Main web interface (HTML page)

### GET `/health`
Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu",
  "dataset": "cifar10"
}
```

### POST `/predict`
Predict single image

**Request**:
- `file`: Image file (multipart/form-data)

**Response**:
```json
{
  "predicted_class": "airplane",
  "confidence": 0.9523,
  "all_probabilities": [
    {"class": "airplane", "probability": 0.9523},
    {"class": "ship", "probability": 0.0234},
    ...
  ]
}
```

### POST `/predict_batch`
Predict multiple images

**Request**:
- `files`: List of image files

**Response**:
```json
{
  "results": [
    {
      "filename": "img1.jpg",
      "predicted_class": "cat",
      "confidence": 0.8765
    },
    ...
  ]
}
```

### GET `/classes`
Get available classes

**Response**:
```json
{
  "dataset": "cifar10",
  "classes": ["airplane", "automobile", ...]
}
```

## Using the API Programmatically

### Python Example

```python
import requests

# Single prediction
url = "http://localhost:8000/predict"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()

print(f"Predicted: {result['predicted_class']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### cURL Example

```bash
# Single prediction
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"

# Health check
curl http://localhost:8000/health
```

### JavaScript Example

```javascript
// Upload and classify image
async function classifyImage(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  console.log('Prediction:', result.predicted_class);
  console.log('Confidence:', result.confidence);
}
```

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t image-classifier .

# Run container (API will start automatically)
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  image-classifier
```

### Access from Docker

- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Override Command (for training)

```bash
# Run training instead of API
docker run image-classifier python src/training/train.py

# Run inference CLI
docker run image-classifier \
  python src/models/predict.py \
  --model_path models/simple_cnn_best.pth \
  --image_path data/test.jpg \
  --dataset cifar10
```

## Configuration

### Change Model

Modify the startup function in `src/app/main.py`:

```python
@app.on_event("startup")
async def startup_event():
    model_path = "models/your_model.pth"
    initialize_model(
        model_path=model_path,
        model_name="simple_cnn",  # or "resnet"
        dataset="cifar10"  # or "mnist"
    )
```

### Change Port

```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 5000
```

### Enable GPU

The API automatically detects and uses GPU if available:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

### CORS Configuration

Edit CORS settings in `src/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn

gunicorn src.app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Environment Variables

```bash
export MODEL_PATH=/path/to/model.pth
export DATASET=cifar10
export PORT=8000
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Test all endpoints interactively
- See request/response schemas
- Download OpenAPI specification

## Testing the API

### Unit Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict():
    with open("test_image.jpg", "rb") as f:
        response = client.post(
            "/predict",
            files={"file": ("test.jpg", f, "image/jpeg")}
        )
    assert response.status_code == 200
    assert "predicted_class" in response.json()
```

### Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py and run
locust -f locustfile.py --host http://localhost:8000
```

## Monitoring

### Logging

Add logging configuration:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/predict")
async def predict_image_api(file: UploadFile = File(...)):
    logger.info(f"Received prediction request for {file.filename}")
    # ... rest of code
```

### Metrics

Install Prometheus client:

```bash
pip install prometheus-fastapi-instrumentator
```

Add to app:

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## Troubleshooting

### Model Not Found

Ensure model exists:
```bash
ls -la models/simple_cnn_best.pth
```

### Port Already in Use

Change port or kill existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

### Large File Upload

Increase max file size in `main.py`:
```python
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()
app.add_middleware(TrustedHostMiddleware, max_upload_size=10485760)  # 10MB
```

### CUDA Out of Memory

Reduce batch size or use CPU:
```python
device = torch.device("cpu")  # Force CPU
```

## Best Practices

1. **Model Versioning**: Include version in API response
2. **Input Validation**: Validate image size and format
3. **Error Handling**: Return meaningful error messages
4. **Rate Limiting**: Implement rate limiting for production
5. **Caching**: Cache predictions for identical images
6. **Async Processing**: Use background tasks for batch processing
7. **Security**: Add authentication for production APIs

## Next Steps

- Add authentication (JWT, OAuth2)
- Implement rate limiting
- Add model versioning
- Set up CI/CD for deployment
- Add monitoring and alerting
- Implement A/B testing for models
- Add feedback mechanism for predictions

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Production Deployment Guide](https://fastapi.tiangolo.com/deployment/)
