# API Reference - Training Module

Auto-generated API documentation for the training module.

## Training Functions

### Main Training Loop

::: src.training.train.main

### Train Epoch

::: src.training.train.train_epoch

### Validation

::: src.training.train.validate

## Utilities

### Set Seed

::: src.training.train.set_seed

### Get Device

::: src.training.train.get_device

### Get Optimizer

::: src.training.train.get_optimizer

### Get Scheduler

::: src.training.train.get_scheduler

## Module Contents

```
src/training/
├── __init__.py
├── train.py
│   ├── main()
│   ├── train_epoch()
│   ├── validate()
│   ├── set_seed()
│   ├── get_device()
│   ├── get_optimizer()
│   └── get_scheduler()
└── ...
```

## Training Configuration

### Hydra Configuration

Configure training via YAML files in `configs/`:

```yaml
# Main config
hyperparameters:
  optimizer: adam
  learning_rate: 0.001
  batch_size: 32
  num_epochs: 50
  dropout: 0.5
  label_smoothing: 0.1
  clip_grad_norm: 1.0
```

## Supported Optimizers

- **Adam**: Adaptive learning rates
- **SGD**: Stochastic gradient descent

## Supported Schedulers

- **Step**: Decay learning rate by gamma every step_size epochs
- **Cosine**: Cosine annealing schedule
- **Plateau**: Reduce learning rate on metric plateau

## Example Usage

```python
from src.training.train import (
    train_epoch, validate, set_seed,
    get_device, get_optimizer
)
import torch
import torch.nn as nn

# Setup
set_seed(42)
device = get_device("auto")
model = ...  # Create model
criterion = nn.CrossEntropyLoss()
optimizer = get_optimizer(model, config)

# Train one epoch
train_loss, train_acc = train_epoch(
    model, train_loader, criterion,
    optimizer, device
)

# Validate
val_loss, val_acc = validate(
    model, val_loader, criterion, device
)

print(f"Train: loss={train_loss:.4f}, acc={train_acc:.2f}%")
print(f"Val: loss={val_loss:.4f}, acc={val_acc:.2f}%")
```

## Training Outputs

During training, the script saves:
- **Best model**: `models/{model_name}_best.pth`
- **Reports**: `reports/` directory
  - `confusion_matrix.png`
  - `classification_report.txt`
  - `training_history.png`

## Checkpoint Format

```python
checkpoint = {
    'epoch': int,
    'model_state_dict': dict,
    'optimizer_state_dict': dict,
    'val_acc': float,
    'config': dict
}
```

Load checkpoint:

```python
checkpoint = torch.load('models/simple_cnn_best.pth')
model.load_state_dict(checkpoint['model_state_dict'])
epoch = checkpoint['epoch']
```
