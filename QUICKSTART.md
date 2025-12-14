# Quick Reference Guide

Fast commands for common tasks.

## 🚀 Training

```bash
# Basic training
python src/training/train.py

# Fast training for testing
python src/training/train.py hyperparameters=fast

# Train with experiment tracking
python scripts/train_with_tracking.py

# Train with different model/dataset
python src/training/train.py model=resnet data=mnist
```

## 📊 Experiment Tracking

```bash
# Setup MLflow
export MLFLOW_TRACKING_URI="file://$(pwd)/mlruns"
mlflow ui --port 5000

# Setup W&B
wandb login

# Train with tracking
python scripts/train_with_tracking.py
```

## 🔧 Model Serving

```bash
# Start FastAPI server
uvicorn serve.app:app --reload --host 0.0.0.0 --port 8000

# Test API
python serve/test_api.py

# Predict single image
curl -X POST "http://localhost:8000/predict" -F "file=@image.jpg"
```

## 🐳 Docker

```bash
# Build training image
docker build -t image-classifier .

# Build serving image
docker build -f serve/Dockerfile -t image-classifier-api .

# Run training
docker run image-classifier

# Run API server
docker run -p 8000:8000 -v $(pwd)/models:/app/models:ro image-classifier-api
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_model.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term --cov-report=html

# Run only fast tests
pytest tests/ -v -m "not slow"
```

## 🎨 Code Quality

```bash
# Format code
black src tests
isort src tests

# Lint
flake8 src tests --max-line-length=135

# Type check
mypy src --ignore-missing-imports

# Run all pre-commit hooks
pre-commit run --all-files
```

## 📦 Installation

```bash
# Development setup
pip install -r requirements-dev.txt
pre-commit install

# Production setup
pip install -r requirements.txt
pip install -e .

# CI/CD setup (lightweight)
pip install -r requirements-ci.txt
pip install -e .
```

## 🔍 Model Inference

```bash
# Predict single image
python src/models/predict.py \
  --model_path models/simple_cnn_best.pth \
  --image_path image.jpg \
  --dataset cifar10

# Using API
curl -X POST "http://localhost:8000/predict" \
  -F "file=@image.jpg" | jq
```

## 📈 View Results

```bash
# MLflow UI
mlflow ui --port 5000
# Open: http://localhost:5000

# W&B dashboard
# Open: https://wandb.ai/

# FastAPI docs
# Open: http://localhost:8000/docs
```

## 🗂️ Directory Structure

```bash
# Create necessary directories
mkdir -p data/raw data/processed models reports/figures outputs

# Check disk usage
du -sh data/ models/ outputs/

# Clean outputs
rm -rf outputs/* reports/figures/*
```

## 🌐 GitHub Actions

```bash
# Trigger tests manually
gh workflow run tests.yaml

# Trigger CML workflow
gh workflow run cml.yaml

# View workflow runs
gh run list

# View specific run
gh run view <run-id>
```

## 💡 Tips

```bash
# Train with GPU
python src/training/train.py device=cuda

# Train with custom batch size
python src/training/train.py hyperparameters.batch_size=256

# Override multiple configs
python src/training/train.py \
  model=resnet \
  data=mnist \
  hyperparameters=fast \
  hyperparameters.num_epochs=10

# Debug mode (small data)
python src/training/train.py \
  hyperparameters.batch_size=4 \
  hyperparameters.num_epochs=1

# View Hydra config without training
python src/training/train.py --cfg job
```

## 🔑 Environment Variables

```bash
# MLflow
export MLFLOW_TRACKING_URI="file://$(pwd)/mlruns"
export MLFLOW_TRACKING_URI="http://mlflow-server:5000"

# W&B
export WANDB_API_KEY="your_key"
export WANDB_ENTITY="your_username"

# Model path
export MODEL_PATH="models/simple_cnn_best.pth"
```

## 📚 Documentation

```bash
# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve
# Open: http://localhost:8000

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## 🐛 Debugging

```bash
# Show detailed Hydra errors
HYDRA_FULL_ERROR=1 python src/training/train.py

# Run with Python debugger
python -m pdb src/training/train.py

# Check CUDA availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Check package versions
pip list | grep -E "torch|hydra|mlflow|wandb"
```
