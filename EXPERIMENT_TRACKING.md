# Experiment Tracking Quick Start

## Installation

```bash
# Install dependencies
pip install mlflow wandb

# Or run setup script
./scripts/setup_tracking.sh
```

## Quick Usage

### 1. Train with MLflow
```bash
python src/training/train.py tracking=mlflow
```

View results:
```bash
mlflow ui
# Open http://localhost:5000
```

### 2. Train with Weights & Biases
```bash
# Login first
wandb login

# Train
python src/training/train.py tracking=wandb
```

### 3. Compare Different Configurations
```bash
# Try different models
python src/training/train.py model=simple_cnn tracking=mlflow
python src/training/train.py model=resnet tracking=mlflow

# Try different learning rates
python src/training/train.py hyperparameters.learning_rate=0.001 tracking=mlflow
python src/training/train.py hyperparameters.learning_rate=0.01 tracking=mlflow
```

## Utility Scripts

```bash
# Compare MLflow experiments
python scripts/compare_experiments.py --experiment image_classifier --top-n 5

# List all experiments
python scripts/compare_experiments.py --list

# Manage MLflow models
python scripts/mlflow_models.py --list

# Run W&B hyperparameter sweep
python scripts/wandb_sweep.py
```

## Configuration Files

- `configs/tracking/mlflow.yaml` - MLflow settings
- `configs/tracking/wandb.yaml` - W&B settings
- `configs/config.yaml` - Main config (set default tracking backend)

## Full Documentation

See [docs/mlops/experiment-tracking.md](docs/mlops/experiment-tracking.md) for complete documentation.
