"""FastAPI application for model serving."""

import io
from pathlib import Path
from typing import Dict, List

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import BaseModel

from models.model import get_model
from models.predict import predict_single

# Initialize FastAPI app
app = FastAPI(
    title="Image Classifier API",
    description="Deep learning image classification service",
    version="1.0.0",
)

# Global model cache
MODEL_CACHE = {}
DEFAULT_MODEL_PATH = Path("models/simple_cnn_best.pth")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# CIFAR-10 classes
CIFAR10_CLASSES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


class PredictionResponse(BaseModel):
    """Response model for predictions."""

    success: bool
    predicted_class: str
    confidence: float
    all_probabilities: Dict[str, float]


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    model_loaded: bool
    device: str


def load_model(model_path: Path = DEFAULT_MODEL_PATH):
    """Load model into cache if not already loaded."""
    if "model" not in MODEL_CACHE:
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        checkpoint = torch.load(model_path, map_location=DEVICE)
        config = checkpoint.get("config", {})

        model = get_model(
            model_name=config.get("model", {}).get("name", "simple_cnn"),
            num_classes=config.get("data", {}).get("num_classes", 10),
            input_channels=config.get("data", {}).get("input_channels", 3),
            dropout=config.get("model", {}).get("dropout", 0.5),
        )

        model.load_state_dict(checkpoint["model_state_dict"])
        model.to(DEVICE)
        model.eval()

        MODEL_CACHE["model"] = model
        MODEL_CACHE["config"] = config

    return MODEL_CACHE["model"]


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    try:
        load_model()
        print(f"✅ Model loaded successfully on {DEVICE}")
    except Exception as e:
        print(f"⚠️  Warning: Could not load model on startup: {e}")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "Image Classifier API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded="model" in MODEL_CACHE,
        device=str(DEVICE),
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Predict image class.

    Args:
        file: Image file to classify

    Returns:
        Prediction results with class and confidence
    """
    try:
        # Load model
        model = load_model()

        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Get prediction
        predicted_idx, probabilities = predict_single(
            model, image, DEVICE, dataset="cifar10"
        )

        predicted_class = CIFAR10_CLASSES[predicted_idx]
        confidence = float(probabilities[predicted_idx])

        # Create probability dictionary
        all_probs = {
            CIFAR10_CLASSES[i]: float(probabilities[i])
            for i in range(len(CIFAR10_CLASSES))
        }

        return PredictionResponse(
            success=True,
            predicted_class=predicted_class,
            confidence=confidence,
            all_probabilities=all_probs,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/classes", response_model=List[str])
async def get_classes():
    """Get list of available classes."""
    return CIFAR10_CLASSES


@app.get("/model-info", response_model=Dict)
async def model_info():
    """Get model information."""
    if "config" not in MODEL_CACHE:
        load_model()

    config = MODEL_CACHE.get("config", {})
    return {
        "model_name": config.get("model", {}).get("name", "unknown"),
        "num_classes": config.get("data", {}).get("num_classes", 10),
        "input_channels": config.get("data", {}).get("input_channels", 3),
        "device": str(DEVICE),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
