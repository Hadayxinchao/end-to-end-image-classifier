# Model Serving with FastAPI

REST API for serving the trained image classification model.

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install fastapi uvicorn python-multipart
```

### 2. Start the server

```bash
# From project root
python serve/app.py

# Or with uvicorn directly
uvicorn serve.app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda"
}
```

### `POST /predict`
Classify an image.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Image file

**Response:**
```json
{
  "success": true,
  "predicted_class": "cat",
  "confidence": 0.9234,
  "all_probabilities": {
    "airplane": 0.0123,
    "automobile": 0.0045,
    "bird": 0.0234,
    "cat": 0.9234,
    ...
  }
}
```

### `GET /classes`
Get list of available classes.

**Response:**
```json
["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
```

### `GET /model-info`
Get model information.

**Response:**
```json
{
  "model_name": "simple_cnn",
  "num_classes": 10,
  "input_channels": 3,
  "device": "cuda"
}
```

## 🧪 Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Predict image
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/image.jpg"

# Get classes
curl http://localhost:8000/classes
```

### Using Python

```python
import requests

# Predict
url = "http://localhost:8000/predict"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Using httpie

```bash
# Install httpie
pip install httpie

# Predict
http -f POST localhost:8000/predict file@image.jpg
```

## 🐳 Docker Deployment

### Build image

```bash
docker build -f serve/Dockerfile -t image-classifier-api .
```

### Run container

```bash
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models:ro \
  image-classifier-api
```

## 🔧 Configuration

### Environment Variables

- `MODEL_PATH`: Path to model checkpoint (default: `models/simple_cnn_best.pth`)
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `WORKERS`: Number of workers (default: `1`)

### Production Deployment

```bash
# With gunicorn + uvicorn workers
gunicorn serve.app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

## 📊 Performance

- **Throughput**: ~50-100 requests/second (CPU)
- **Latency**: ~50-100ms per prediction (CPU)
- **Batch processing**: Not yet implemented

## 🔒 Security Considerations

- Add authentication (JWT, API keys)
- Rate limiting
- Input validation
- CORS configuration
- HTTPS in production

## 📝 TODO

- [ ] Batch prediction endpoint
- [ ] Async processing with Celery
- [ ] Model versioning support
- [ ] Monitoring with Prometheus
- [ ] A/B testing support
