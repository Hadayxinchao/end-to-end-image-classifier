# Data Management

This guide explains how to manage datasets and data versioning.

## Dataset Overview

The project supports two datasets:

### CIFAR-10
- **Resolution**: 32×32 RGB images
- **Classes**: 10 (airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck)
- **Samples**: 50,000 training, 10,000 test
- **Download**: Automatic via torchvision

### MNIST
- **Resolution**: 28×28 grayscale images
- **Classes**: 10 (digits 0-9)
- **Samples**: 60,000 training, 10,000 test
- **Download**: Automatic via torchvision

## Downloading Datasets

### Automatic Download

Data downloads automatically on first run:

```bash
python src/training/train.py data=cifar10
```

### Manual Download

To pre-download datasets:

```python
from src.data.make_dataset import load_cifar10, load_mnist

# Download CIFAR-10
load_cifar10(data_dir="data/raw")

# Download MNIST
load_mnist(data_dir="data/raw")
```

## Data Directory Structure

```
data/
├── raw/                 # Original datasets
│   ├── cifar-10/
│   └── mnist/
└── processed/           # Processed data (if any)
```

## Data Configuration

Configure datasets in `configs/data/`:

**CIFAR-10** (`configs/data/cifar10.yaml`):
```yaml
name: cifar10
num_classes: 10
input_channels: 3
image_size: 32
val_split: 0.2
classes: [airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck]
```

**MNIST** (`configs/data/mnist.yaml`):
```yaml
name: mnist
num_classes: 10
input_channels: 1
image_size: 28
val_split: 0.2
classes: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Data Augmentation

### Training Augmentation

Images are augmented during training:
- Random horizontal flip
- Random rotation (±10 degrees)
- Random crop
- Normalization with ImageNet statistics

### Validation/Test

No augmentation for validation/test sets.

### Custom Augmentation

Modify `src/data/make_dataset.py`:

```python
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.RandomErasing(p=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])
```

## Data Versioning with DVC

### Initialize DVC

```bash
dvc init
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

### Track Data

```bash
dvc add data/raw/cifar10
dvc add data/raw/mnist
git add data/raw/cifar10.dvc data/raw/mnist.dvc
git commit -m "Add dataset versions"
```

### Remote Storage

Configure remote storage:

```bash
# Local storage
dvc remote add -d storage /path/to/storage

# S3
dvc remote add -d storage s3://bucket-name/path

# Google Drive
dvc remote add -d storage gdrive://folder-id
```

### Push Data

```bash
dvc push
```

### Pull Data

```bash
dvc pull
```

## Data Statistics

Calculate dataset statistics:

```python
from src.data.make_dataset import load_cifar10
import numpy as np

train_loader, _, _ = load_cifar10(batch_size=1000)

means = []
stds = []

for images, _ in train_loader:
    means.append(images.mean([0, 2, 3]))
    stds.append(images.std([0, 2, 3]))

mean = np.stack(means).mean(axis=0)
std = np.stack(stds).mean(axis=0)

print(f"Mean: {mean}")
print(f"Std: {std}")
```

## Custom Dataset

To add custom datasets:

1. Create dataset loader in `src/data/make_dataset.py`
2. Add configuration file in `configs/data/`
3. Update training script to support new dataset

Example:

```python
def load_custom_dataset(data_dir, batch_size=32, val_split=0.2):
    dataset = ImageFolder(data_dir, transform=transform)
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    
    train_set, val_set = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )
    
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader
```

## Data Issues & Solutions

### Disk Space
- CIFAR-10: ~170MB
- MNIST: ~12MB
- Ensure sufficient disk space before downloading

### Network Issues
- Use `--offline` flag if data already downloaded
- Check internet connection for automatic downloads

### Corrupted Files
- Delete cached files and re-download:
  ```bash
  rm -rf data/raw
  python src/training/train.py data=cifar10
  ```
