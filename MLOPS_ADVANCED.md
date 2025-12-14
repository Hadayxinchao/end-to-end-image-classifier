# MLOps Advanced Features Guide

This guide covers advanced MLOps features including model serving, experiment tracking, data validation, and code quality automation.

## 📑 Table of Contents

1. [Pre-commit Hooks](#1-pre-commit-hooks)
2. [FastAPI Model Serving](#2-fastapi-model-serving)
3. [MLflow Experiment Tracking](#3-mlflow-experiment-tracking)
4. [Weights & Biases Integration](#4-weights--biases-integration)
5. [Data Validation (Great Expectations)](#5-data-validation)

---

## 1. Pre-commit Hooks

Automatically format and check code quality before each commit.

### Setup

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### What it does

- ✅ Format code with Black
- ✅ Sort imports with isort
- ✅ Lint with flake8
- ✅ Type check with mypy
- ✅ Security scan with bandit
- ✅ Check YAML/JSON syntax
- ✅ Remove trailing whitespace
- ✅ Detect large files and secrets

### Configuration

Edit `.pre-commit-config.yaml` to customize hooks.

---

## 2. FastAPI Model Serving

REST API for serving trained models.

### Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn python-multipart

# Start server
python serve/app.py

# Or with auto-reload
uvicorn serve.app:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Predict image
curl -X POST "http://localhost:8000/predict" \
  -F "file=@image.jpg"

# Get available classes
curl http://localhost:8000/classes

# Get model info
curl http://localhost:8000/model-info
```

### Test the API

```bash
# Run test script
python serve/test_api.py

# Test with custom image
python serve/test_api.py --image path/to/image.jpg
```

### Docker Deployment

```bash
# Build image
docker build -f serve/Dockerfile -t image-classifier-api .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models:ro \
  image-classifier-api
```

See `serve/README.md` for more details.

---

## 3. MLflow Experiment Tracking

Track experiments, parameters, metrics, and models.

### Setup

```bash
# Install MLflow
pip install mlflow

# Setup tracking
python scripts/setup_mlflow.py

# Start MLflow UI
mlflow ui --port 5000
```

### Usage in Training

Add to `src/training/train.py`:

```python
import mlflow

# Start run
with mlflow.start_run():
    # Log parameters
    mlflow.log_params({
        "learning_rate": cfg.hyperparameters.learning_rate,
        "batch_size": cfg.hyperparameters.batch_size,
        "optimizer": cfg.hyperparameters.optimizer,
    })
    
    # Training loop
    for epoch in range(num_epochs):
        train_loss, train_acc = train_epoch(...)
        val_loss, val_acc = validate(...)
        
        # Log metrics
        mlflow.log_metrics({
            "train_loss": train_loss,
            "train_acc": train_acc,
            "val_loss": val_loss,
            "val_acc": val_acc,
        }, step=epoch)
    
    # Log model
    mlflow.pytorch.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifacts("reports/figures")
```

### View Results

Open http://localhost:5000 to view:
- Experiment runs
- Parameter comparison
- Metric plots
- Model artifacts

---

## 4. Weights & Biases Integration

Advanced experiment tracking with W&B.

### Setup

```bash
# Install wandb
pip install wandb

# Login
wandb login

# Or setup with script
python scripts/setup_wandb.py --login
```

### Usage in Training

Add to `src/training/train.py`:

```python
import wandb

# Initialize run
wandb.init(
    project="image-classifier",
    config={
        "learning_rate": cfg.hyperparameters.learning_rate,
        "batch_size": cfg.hyperparameters.batch_size,
        "architecture": cfg.model.name,
    }
)

# Training loop
for epoch in range(num_epochs):
    train_loss, train_acc = train_epoch(...)
    val_loss, val_acc = validate(...)
    
    # Log metrics
    wandb.log({
        "epoch": epoch,
        "train/loss": train_loss,
        "train/accuracy": train_acc,
        "val/loss": val_loss,
        "val/accuracy": val_acc,
    })

# Log images
wandb.log({"confusion_matrix": wandb.Image("reports/figures/confusion_matrix.png")})

# Save model
wandb.save("models/model_best.pth")

wandb.finish()
```

### Features

- 📊 Real-time metric visualization
- 🔄 Model versioning
- 👥 Team collaboration
- 📈 Hyperparameter optimization
- 🎨 Custom charts and reports

---

## 5. Data Validation

Validate data quality with Great Expectations (Coming soon).

### Setup

```bash
# Install Great Expectations
pip install great-expectations

# Initialize
great_expectations init
```

### Create Expectations

```python
import great_expectations as gx

# Create data context
context = gx.get_context()

# Create expectations
validator = context.sources.pandas_default.read_csv("data/processed/train.csv")

validator.expect_column_values_to_not_be_null("image_path")
validator.expect_column_values_to_be_in_set("label", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# Save expectations
validator.save_expectation_suite()
```

---

## 📦 Installation Summary

Install all optional features:

```bash
# Development dependencies (includes all tools)
pip install -r requirements-dev.txt

# Individual installations
pip install pre-commit          # Code quality hooks
pip install fastapi uvicorn     # Model serving
pip install mlflow              # Experiment tracking
pip install wandb               # Advanced tracking
pip install great-expectations  # Data validation
```

---

## 🚀 Complete Workflow Example

```bash
# 1. Setup pre-commit hooks
pre-commit install

# 2. Train model with MLflow tracking
python src/training/train.py

# 3. View experiments
mlflow ui --port 5000

# 4. Serve model
uvicorn serve.app:app --reload

# 5. Test API
python serve/test_api.py --image test.jpg

# 6. Deploy with Docker
docker build -f serve/Dockerfile -t model-api .
docker run -p 8000:8000 model-api
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Weights & Biases Documentation](https://docs.wandb.ai/)
- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Pre-commit Documentation](https://pre-commit.com/)

---

## 🤝 Contributing

When contributing, ensure all pre-commit hooks pass:

```bash
pre-commit run --all-files
pytest tests/ -v
```
