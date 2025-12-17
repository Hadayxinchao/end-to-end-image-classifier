# Experiment Tracking

This project supports experiment tracking with both **MLflow** and **Weights & Biases (W&B)**. This allows you to track, compare, and visualize your machine learning experiments.

## Features

- 📊 **Metric Tracking**: Automatically log training/validation metrics
- 🔧 **Hyperparameter Logging**: Track all configuration parameters
- 📈 **Visualization**: Interactive plots and dashboards
- 🎯 **Model Versioning**: Save and version your trained models
- 📁 **Artifact Management**: Store confusion matrices, plots, and reports
- 🔄 **Comparison**: Compare multiple experiments side-by-side
- 🌐 **Remote Tracking**: Support for both local and remote tracking servers

## Setup

### Install Dependencies

```bash
pip install mlflow wandb
```

Or install from requirements:

```bash
pip install -r requirements.txt
```

### MLflow Setup

MLflow works out of the box with local tracking. The tracking data is stored in `./mlruns` by default.

#### Remote MLflow Server (Optional)

To use a remote MLflow server:

1. Start MLflow server:
```bash
mlflow server --host 0.0.0.0 --port 5000
```

2. Update `configs/tracking/mlflow.yaml`:
```yaml
tracking_uri: http://localhost:5000
```

### Weights & Biases Setup

1. **Create a W&B account**: Sign up at [wandb.ai](https://wandb.ai)

2. **Login to W&B**:
```bash
wandb login
```

3. **Update configuration** in `configs/tracking/wandb.yaml`:
```yaml
project: your-project-name
entity: your-username-or-team
```

## Configuration

### Choose Tracking Backend

In `configs/config.yaml`, set the tracking backend:

```yaml
defaults:
  - tracking: mlflow  # Options: mlflow, wandb, or null (to disable)
```

### MLflow Configuration

Edit `configs/tracking/mlflow.yaml`:

```yaml
# MLflow Configuration
enabled: true
tracking_uri: ./mlruns  # Local tracking
experiment_name: ${experiment_name}
run_name: ${run_name}

# What to log
log_params: true
log_metrics: true
log_models: true
log_artifacts: true

# Model Registry
register_model: false
registered_model_name: ${model.name}_${data.name}

# Autologging (logs everything automatically)
autolog: false
```

### W&B Configuration

Edit `configs/tracking/wandb.yaml`:

```yaml
# Weights & Biases Configuration
enabled: true
project: image-classifier
entity: null  # Your username/team

# Mode: online, offline, or disabled
mode: online

# What to log
log_params: true
log_metrics: true
log_gradients: false
log_model: true
log_artifacts: true

# Model watching (log gradients/parameters)
watch_model: false
watch_log: "gradients"  # "gradients", "parameters", or "all"
watch_freq: 100
```

## Usage

### Basic Training with Tracking

```bash
# Train with MLflow
python src/training/train.py tracking=mlflow

# Train with W&B
python src/training/train.py tracking=wandb

# Train without tracking
python src/training/train.py tracking=null
```

### View MLflow UI

```bash
mlflow ui
```

Then open http://localhost:5000 in your browser.

### View W&B Dashboard

After training, W&B will print a URL to your run. You can also visit your project page at:
```
https://wandb.ai/your-username/your-project
```

## What Gets Logged

### Metrics
- `train_loss`, `train_acc` (per epoch)
- `val_loss`, `val_acc` (per epoch)
- `test_loss`, `test_acc` (final)
- `learning_rate` (per epoch)
- Test metrics: `precision`, `recall`, `f1_score`, `accuracy`

### Parameters
- Model architecture
- Dataset name
- Hyperparameters (learning rate, batch size, optimizer, etc.)
- Number of parameters (total and trainable)
- Device (CPU/GPU)

### Artifacts
- 📊 Confusion matrix
- 📈 Training history plots
- 📝 Classification report
- 🎯 Best model checkpoint

### Models
- Best model (based on validation accuracy)
- Model architecture and state dict
- Optimizer state

## Advanced Usage

### Custom Experiment Names

```bash
python src/training/train.py \
  experiment_name=cifar10_resnet \
  run_name=resnet50_lr0.001
```

### Enable W&B Model Watching

To log gradients and parameters during training:

```yaml
# configs/tracking/wandb.yaml
watch_model: true
watch_log: "all"  # Log both gradients and parameters
watch_freq: 100   # Log every 100 batches
```

⚠️ **Warning**: This can significantly slow down training and use more storage.

### MLflow Model Registry

To register your model in MLflow Model Registry:

```yaml
# configs/tracking/mlflow.yaml
register_model: true
registered_model_name: resnet_cifar10
```

### Offline Mode (W&B)

Train without internet connection:

```yaml
# configs/tracking/wandb.yaml
mode: offline
```

Then sync later:
```bash
wandb sync ./wandb/offline-run-*
```

## Comparing Experiments

### MLflow

1. Open MLflow UI: `mlflow ui`
2. Select multiple runs using checkboxes
3. Click "Compare" to see side-by-side comparison
4. Use the chart view for metric comparisons

### W&B

1. Go to your project dashboard
2. All runs are automatically tracked and displayed
3. Use the table view to compare metrics
4. Create custom panels and reports

## Examples

### Example 1: Compare Different Models

```bash
# Train Simple CNN
python src/training/train.py model=simple_cnn experiment_name=model_comparison

# Train ResNet
python src/training/train.py model=resnet experiment_name=model_comparison
```

All runs will be grouped under the same experiment for easy comparison.

### Example 2: Hyperparameter Sweep

```bash
# Try different learning rates
python src/training/train.py hyperparameters.learning_rate=0.001
python src/training/train.py hyperparameters.learning_rate=0.01
python src/training/train.py hyperparameters.learning_rate=0.1
```

### Example 3: Grid Search with W&B Sweeps

Create `sweep_config.yaml`:

```yaml
program: src/training/train.py
method: grid
parameters:
  hyperparameters.learning_rate:
    values: [0.001, 0.01, 0.1]
  hyperparameters.batch_size:
    values: [32, 64, 128]
  model.name:
    values: [simple_cnn, resnet]
```

Run sweep:
```bash
wandb sweep sweep_config.yaml
wandb agent <sweep-id>
```

## Best Practices

1. **Use Descriptive Names**: Give your experiments and runs meaningful names
2. **Tag Your Runs**: Use tags to organize experiments (W&B)
3. **Document Changes**: Add notes about what you're testing (W&B)
4. **Regular Cleanup**: Archive old experiments you don't need
5. **Save Important Models**: Use model registry for production models
6. **Track Everything**: Log all hyperparameters and configuration

## Troubleshooting

### MLflow Connection Issues

```bash
# Check if MLflow server is running
mlflow server --help

# Test connection
mlflow runs list --experiment-id 0
```

### W&B Login Issues

```bash
# Re-login
wandb login --relogin

# Check status
wandb status
```

### Disk Space Issues

MLflow and W&B can use significant storage. To clean up:

```bash
# MLflow (be careful!)
rm -rf mlruns/

# W&B
wandb artifact cache cleanup
```

## Integration with Code

The experiment tracking is integrated through the `ExperimentTracker` class:

```python
from utils.experiment_tracking import ExperimentTracker

# Initialize tracker
tracker = ExperimentTracker(cfg, tracking_backend="mlflow")

# Log parameters
tracker.log_params({"learning_rate": 0.001, "batch_size": 32})

# Log metrics
tracker.log_metrics({"train_loss": 0.5, "val_acc": 0.95}, step=epoch)

# Log artifacts
tracker.log_artifact("reports/confusion_matrix.png")

# Log model
tracker.log_model(model, model_path="models/best.pth")

# Finish tracking
tracker.finish()
```

## Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [W&B Documentation](https://docs.wandb.ai/)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [W&B Sweeps](https://docs.wandb.ai/guides/sweeps)

## Next Steps

- Set up CI/CD pipeline with experiment tracking
- Implement automated hyperparameter tuning
- Create custom dashboards for model monitoring
- Integrate with model deployment pipelines
