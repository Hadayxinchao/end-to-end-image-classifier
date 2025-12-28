"""FastAPI application for image classification inference."""

import io
import sys
from pathlib import Path
from typing import Dict, List

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from PIL import Image

from src.models.model import get_model
from src.models.predict import CIFAR10_CLASSES, MNIST_CLASSES, load_model, predict, preprocess_image

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


# Initialize FastAPI app
app = FastAPI(
    title="Image Classifier API",
    description="API for image classification using trained CNN models",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
model = None
device = None
current_dataset = "cifar10"
classes = CIFAR10_CLASSES


def initialize_model(
    model_path: str = "models/simple_cnn_best.pth",
    model_name: str = "simple_cnn",
    dataset: str = "cifar10",
):
    """Initialize the model on startup."""
    global model, device, current_dataset, classes

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    current_dataset = dataset

    # Set classes based on dataset
    if dataset == "mnist":
        num_classes = 10
        input_channels = 1
        classes = MNIST_CLASSES
    else:
        num_classes = 10
        input_channels = 3
        classes = CIFAR10_CLASSES

    # Load model
    model = get_model(model_name, num_classes=num_classes, input_channels=input_channels)
    model = load_model(model_path, model, str(device))

    print(f"Model loaded successfully on {device}")
    print(f"Dataset: {dataset}")


@app.on_event("startup")
async def startup_event():
    """Initialize model on startup."""
    model_path = project_root / "models" / "simple_cnn_best.pth"
    if model_path.exists():
        initialize_model(str(model_path))
    else:
        print("Warning: Model not found. Please upload an image to initialize.")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Classifier</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }

            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                max-width: 600px;
                width: 100%;
            }

            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
            }

            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }

            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                background: #f8f9ff;
                cursor: pointer;
                transition: all 0.3s;
                margin-bottom: 20px;
            }

            .upload-area:hover {
                border-color: #764ba2;
                background: #f0f1ff;
            }

            .upload-area.dragover {
                border-color: #764ba2;
                background: #e8e9ff;
                transform: scale(1.02);
            }

            #fileInput {
                display: none;
            }

            .upload-icon {
                font-size: 3em;
                margin-bottom: 10px;
            }

            .upload-text {
                color: #667eea;
                font-size: 1.2em;
                font-weight: 500;
            }

            .upload-hint {
                color: #999;
                font-size: 0.9em;
                margin-top: 5px;
            }

            #preview {
                max-width: 100%;
                border-radius: 10px;
                margin: 20px 0;
                display: none;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }

            button {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 1.1em;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
                margin-top: 10px;
            }

            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }

            button:active {
                transform: translateY(0);
            }

            button:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
            }

            #result {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9ff;
                border-radius: 10px;
                display: none;
            }

            .prediction {
                font-size: 1.5em;
                font-weight: 600;
                color: #667eea;
                margin-bottom: 15px;
                text-align: center;
            }

            .confidence {
                text-align: center;
                font-size: 1.2em;
                color: #666;
                margin-bottom: 20px;
            }

            .confidence-bar {
                background: #e0e0e0;
                border-radius: 10px;
                height: 25px;
                overflow: hidden;
                margin-bottom: 20px;
            }

            .confidence-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                transition: width 0.5s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 600;
            }

            .probabilities {
                margin-top: 15px;
            }

            .prob-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px 0;
                border-bottom: 1px solid #e0e0e0;
            }

            .prob-item:last-child {
                border-bottom: none;
            }

            .prob-label {
                font-weight: 500;
                color: #333;
            }

            .prob-value {
                color: #667eea;
                font-weight: 600;
            }

            .loading {
                text-align: center;
                padding: 20px;
                color: #667eea;
                display: none;
            }

            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            .error {
                background: #ffe0e0;
                color: #cc0000;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🖼️ Image Classifier</h1>
            <p class="subtitle">Upload an image to classify</p>

            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📤</div>
                <div class="upload-text">Click to upload or drag and drop</div>
                <div class="upload-hint">Supports: JPG, PNG (Max 5MB)</div>
                <input type="file" id="fileInput" accept="image/*">
            </div>

            <img id="preview" alt="Preview">

            <button id="classifyBtn" disabled>Classify Image</button>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <div>Classifying...</div>
            </div>

            <div class="error" id="error"></div>

            <div id="result">
                <div class="prediction" id="prediction"></div>
                <div class="confidence">
                    Confidence: <span id="confidenceText"></span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" id="confidenceFill"></div>
                </div>
                <div class="probabilities" id="probabilities"></div>
            </div>
        </div>

        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const preview = document.getElementById('preview');
            const classifyBtn = document.getElementById('classifyBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            let selectedFile = null;

            // Click to upload
            uploadArea.addEventListener('click', () => fileInput.click());

            // Drag and drop
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            });

            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFile(e.target.files[0]);
                }
            });

            function handleFile(file) {
                if (!file.type.startsWith('image/')) {
                    showError('Please select an image file');
                    return;
                }

                if (file.size > 5 * 1024 * 1024) {
                    showError('File size should be less than 5MB');
                    return;
                }

                selectedFile = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                    classifyBtn.disabled = false;
                    result.style.display = 'none';
                    error.style.display = 'none';
                };
                reader.readAsDataURL(file);
            }

            classifyBtn.addEventListener('click', async () => {
                if (!selectedFile) return;

                const formData = new FormData();
                formData.append('file', selectedFile);

                loading.style.display = 'block';
                result.style.display = 'none';
                error.style.display = 'none';
                classifyBtn.disabled = true;

                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        throw new Error('Classification failed');
                    }

                    const data = await response.json();
                    displayResult(data);
                } catch (err) {
                    showError('Failed to classify image: ' + err.message);
                } finally {
                    loading.style.display = 'none';
                    classifyBtn.disabled = false;
                }
            });

            function displayResult(data) {
                document.getElementById('prediction').textContent =
                    `Predicted: ${data.predicted_class}`;

                const confidence = (data.confidence * 100).toFixed(2);
                document.getElementById('confidenceText').textContent = confidence + '%';
                document.getElementById('confidenceFill').style.width = confidence + '%';
                document.getElementById('confidenceFill').textContent = confidence + '%';

                // Display all probabilities
                const probsHtml = data.all_probabilities
                    .map(item => `
                        <div class="prob-item">
                            <span class="prob-label">${item.class}</span>
                            <span class="prob-value">${(item.probability * 100).toFixed(2)}%</span>
                        </div>
                    `)
                    .join('');

                document.getElementById('probabilities').innerHTML =
                    '<h3 style="margin-bottom: 10px; color: #333;">All Classes:</h3>' + probsHtml;

                result.style.display = 'block';
            }

            function showError(message) {
                error.textContent = message;
                error.style.display = 'block';
                setTimeout(() => {
                    error.style.display = 'none';
                }, 5000);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device) if device else "not initialized",
        "dataset": current_dataset,
    }


@app.post("/predict")
async def predict_image_api(file: UploadFile = File(...)) -> Dict:
    """
    Predict the class of an uploaded image.

    Args:
        file: Uploaded image file

    Returns:
        Dictionary containing prediction results
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Save temporarily for preprocessing
        temp_path = "/tmp/temp_image.jpg"
        image.save(temp_path)

        # Preprocess and predict
        image_tensor = preprocess_image(temp_path, dataset=current_dataset)
        pred_class, confidence, probs = predict(model, image_tensor, str(device), classes)

        # Prepare response
        all_probs = [
            {"class": cls, "probability": float(prob)} for cls, prob in zip(classes, probs)
        ]
        # Sort by probability
        all_probs.sort(key=lambda x: x["probability"], reverse=True)

        return {
            "predicted_class": pred_class,
            "confidence": float(confidence),
            "all_probabilities": all_probs,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict_batch")
async def predict_batch_api(files: List[UploadFile] = File(...)) -> Dict:
    """
    Predict classes for multiple uploaded images.

    Args:
        files: List of uploaded image files

    Returns:
        Dictionary containing batch prediction results
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    results = []

    for file in files:
        if not file.content_type.startswith("image/"):
            results.append({"filename": file.filename, "error": "Not an image file"})
            continue

        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))

            temp_path = f"/tmp/{file.filename}"
            image.save(temp_path)

            image_tensor = preprocess_image(temp_path, dataset=current_dataset)
            pred_class, confidence, _ = predict(model, image_tensor, str(device), classes)

            results.append(
                {
                    "filename": file.filename,
                    "predicted_class": pred_class,
                    "confidence": float(confidence),
                }
            )

        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})

    return {"results": results}


@app.get("/classes")
async def get_classes():
    """Get list of available classes."""
    return {"dataset": current_dataset, "classes": classes}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
