# Scripts

Utility scripts for training, experiment tracking, and deployment.

## Training Scripts

### `train_with_tracking.py`

Python script to run training with automatic experiment tracking setup.

```bash
# Basic training
python scripts/train_with_tracking.py

# With Hydra overrides
python scripts/train_with_tracking.py hyperparameters=fast

# With custom config
python scripts/train_with_tracking.py \
  model=resnet \
  data=mnist \
  hyperparameters.learning_rate=0.001
```

### `train_with_tracking.sh`

Bash script with MLflow UI auto-start.

```bash
# Make executable
chmod +x scripts/train_with_tracking.sh

# Run training (MLflow UI will not start by default)
./scripts/train_with_tracking.sh

# Run with MLflow UI
START_MLFLOW_UI=true ./scripts/train_with_tracking.sh

# With Hydra overrides
./scripts/train_with_tracking.sh hyperparameters=fast
```

## Experiment Tracking Setup

### `setup_mlflow.py`

Setup MLflow experiment tracking.

```bash
# Initialize MLflow
python scripts/setup_mlflow.py

# Custom experiment name
python scripts/setup_mlflow.py --experiment-name my-experiment

# Custom tracking URI
python scripts/setup_mlflow.py --tracking-uri http://mlflow-server:5000
```

### `setup_wandb.py`

Setup Weights & Biases tracking.

```bash
# Login to W&B
python scripts/setup_wandb.py --login

# Initialize project
python scripts/setup_wandb.py --project my-project

# With entity (team/username)
python scripts/setup_wandb.py --project my-project --entity my-team
```

## Environment Variables

### MLflow

```bash
# Local file storage
export MLFLOW_TRACKING_URI="file:///path/to/mlruns"

# Remote MLflow server
export MLFLOW_TRACKING_URI="http://mlflow-server:5000"
```

### Weights & Biases

```bash
# Get API key from: https://wandb.ai/authorize
export WANDB_API_KEY="your_api_key_here"

# Optional: Set entity
export WANDB_ENTITY="your-username-or-team"
```

## Quick Start Examples

### Train with MLflow only

```bash
# Set MLflow URI
export MLFLOW_TRACKING_URI="file://$(pwd)/mlruns"

# Train
python scripts/train_with_tracking.py

# View results
mlflow ui --port 5000
```

### Train with W&B only

```bash
# Login once
wandb login

# Train (WANDB_API_KEY is saved)
python scripts/train_with_tracking.py
```

### Train with both MLflow and W&B

```bash
# Setup both
export MLFLOW_TRACKING_URI="file://$(pwd)/mlruns"
wandb login

# Train
python scripts/train_with_tracking.py

# View MLflow
mlflow ui --port 5000

# View W&B
# Open https://wandb.ai/
```

## CI/CD Integration

In GitHub Actions or other CI:

```yaml
env:
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
  WANDB_API_KEY: ${{ secrets.WANDB_API_KEY }}

steps:
  - name: Train with tracking
    run: python scripts/train_with_tracking.py
```
