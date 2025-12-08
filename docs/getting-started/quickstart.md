# Quick Start Guide

Get up and running with the Image Classifier in just a few minutes!

## Train Your First Model

### Using Default Configuration

The simplest way to start:

```bash
python src/training/train.py
```

This will:

- Download the CIFAR-10 dataset automatically
- Train a simple CNN model
- Save the best model to `models/`
- Generate reports in `reports/`

### Training Output

You'll see output like this:

```
================================================================================
Configuration:
data:
  batch_size: 64
  name: cifar10
  num_classes: 10
hyperparameters:
  learning_rate: 0.001
  num_epochs: 50
...
================================================================================

Using device: cuda

Loading cifar10 dataset...
Train batches: 704
Val batches: 79
Test batches: 157

Creating simple_cnn model...
Total parameters: 1,234,567
Trainable parameters: 1,234,567

Starting training for 50 epochs...
```

## Quick Experiments

### Change Learning Rate

```bash
python src/training/train.py hyperparameters.learning_rate=0.01
```

### Use Different Model

```bash
python src/training/train.py model=resnet
```

### Train on MNIST Instead

```bash
python src/training/train.py data=mnist
```

### Fast Training (for testing)

```bash
python src/training/train.py hyperparameters=fast
```

This uses:
- 5 epochs instead of 50
- Larger batch size (128)
- No learning rate scheduler

## View Results

After training, check the results:

### Training Report

```bash
cat reports/classification_report.txt
```

### Confusion Matrix

The confusion matrix is saved as an image:

```bash
# Linux/Mac
xdg-open reports/figures/confusion_matrix.png

# Mac
open reports/figures/confusion_matrix.png

# Windows
start reports/figures/confusion_matrix.png
```

### Training History

View the training curves:

```bash
# Linux/Mac
xdg-open reports/figures/training_history.png
```

## Make Predictions

### On a Single Image

```bash
python src/models/predict.py \
  --model_path models/simple_cnn_best.pth \
  --image_path path/to/your/image.jpg \
  --dataset cifar10
```

Example output:

```
Prediction: cat
Confidence: 0.9234

All class probabilities:
  airplane: 0.0012
  automobile: 0.0045
  bird: 0.0234
  cat: 0.9234
  deer: 0.0123
  ...
```

## Run Tests

Make sure everything works:

```bash
# Run fast tests only
pytest tests/ -m "not slow"

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Next Steps

### Learn Configuration Management

Hydra makes it easy to manage experiments. Learn more:

```bash
# See all config options
python src/training/train.py --help

# Use different config group
python src/training/train.py --config-name=experiment1
```

Read the [Configuration Guide](configuration.md) for details.

### Experiment Tracking

Create a new experiment config:

```bash
mkdir -p configs/experiment
```

Create `configs/experiment/my_experiment.yaml`:

```yaml
# @package _global_

defaults:
  - override /model: resnet
  - override /hyperparameters: default

hyperparameters:
  learning_rate: 0.005
  num_epochs: 30
  batch_size: 128

experiment_name: my_first_experiment
```

Run it:

```bash
python src/training/train.py --config-name=experiment/my_experiment
```

### Use Docker

Train in a container:

```bash
# Build image
docker build -t image-classifier .

# Run training
docker run --rm \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/reports:/app/reports \
  image-classifier
```

### Version Your Data

Track datasets with DVC:

```bash
# Initialize DVC
dvc init

# Track data
dvc add data/raw

# Commit to git
git add data/raw.dvc .dvc/config
git commit -m "Track data with DVC"
```

## Common Workflows

### Workflow 1: Quick Iteration

```bash
# Fast training for debugging
python src/training/train.py \
  hyperparameters=fast \
  hyperparameters.num_epochs=2

# Check results
cat reports/classification_report.txt
```

### Workflow 2: Production Training

```bash
# Full training with best settings
python src/training/train.py \
  model=resnet \
  hyperparameters.num_epochs=100 \
  hyperparameters.learning_rate=0.001 \
  hyperparameters.use_scheduler=true
```

### Workflow 3: Hyperparameter Search

```bash
# Try different learning rates
for lr in 0.0001 0.001 0.01; do
  python src/training/train.py \
    hyperparameters.learning_rate=$lr \
    experiment_name=lr_search_$lr
done
```

## Tips & Tricks

### Monitor GPU Usage

```bash
# While training, in another terminal:
watch -n 1 nvidia-smi
```

### Save Outputs to Custom Directory

```bash
python src/training/train.py \
  output_dir=./outputs/experiment_1 \
  model_save_dir=./models/experiment_1
```

### Use Multiple GPUs

PyTorch will automatically use all available GPUs. To restrict:

```bash
CUDA_VISIBLE_DEVICES=0 python src/training/train.py
```

### Resume Training

Currently not implemented, but you can add this feature! See [Contributing](../development/contributing.md).

## Troubleshooting

### Out of Memory

Reduce batch size:

```bash
python src/training/train.py hyperparameters.batch_size=32
```

### Training Too Slow

Use fast config or fewer epochs:

```bash
python src/training/train.py hyperparameters.num_epochs=10
```

### Can't Find Model File

Check the model save directory:

```bash
ls -la models/
```

Models are saved as `{model_name}_best.pth`.

## What's Next?

- [Configuration Guide](configuration.md) - Master Hydra configuration
- [Training Guide](../guide/training.md) - Advanced training techniques
- [CI/CD Setup](../mlops/cicd.md) - Automate your workflow
