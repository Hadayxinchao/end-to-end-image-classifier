# API Reference - Data Module

Auto-generated API documentation for the data module.

## Loading Datasets

### CIFAR-10 Dataset

::: src.data.make_dataset.load_cifar10

### MNIST Dataset

::: src.data.make_dataset.load_mnist

## Data Utilities

### Transform Functions

Data preprocessing and augmentation utilities:

::: src.data.make_dataset.get_transforms

## Class Reference

### DataLoader Configuration

```python
from torch.utils.data import DataLoader

# Default parameters
DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)
```

## Module Contents

```
src/data/
├── __init__.py
├── make_dataset.py
│   ├── load_cifar10()
│   ├── load_mnist()
│   └── get_transforms()
└── ...
```

## Example Usage

```python
from src.data.make_dataset import load_cifar10

# Load datasets
train_loader, val_loader, test_loader = load_cifar10(
    data_dir="data/raw",
    batch_size=32,
    val_split=0.2,
    num_workers=4
)

# Iterate through batches
for images, labels in train_loader:
    print(f"Batch shape: {images.shape}")
    print(f"Labels shape: {labels.shape}")
    break
```
