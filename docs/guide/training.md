# Training Models

This guide explains how to train image classification models using this project.

## Basic Training

### CIFAR-10

Train on CIFAR-10 dataset with default configuration:

```bash
python src/training/train.py data=cifar10
```

### MNIST

Train on MNIST dataset:

```bash
python src/training/train.py data=mnist
```

## Configuration Override

Override hyperparameters via command line:

```bash
# Custom learning rate
python src/training/train.py hyperparameters.learning_rate=0.001

# Custom batch size
python src/training/train.py hyperparameters.batch_size=128

# Different optimizer
python src/training/train.py hyperparameters.optimizer=adam

# Multiple overrides
python src/training/train.py \
  data=cifar10 \
  hyperparameters.num_epochs=100 \
  hyperparameters.learning_rate=0.001 \
  model=resnet
```

## Learning Rate Schedulers

### Step Decay

```bash
python src/training/train.py \
  hyperparameters.use_scheduler=true \
  hyperparameters.scheduler_type=step \
  hyperparameters.step_size=30 \
  hyperparameters.gamma=0.1
```

### Cosine Annealing

```bash
python src/training/train.py \
  hyperparameters.use_scheduler=true \
  hyperparameters.scheduler_type=cosine \
  hyperparameters.min_lr=1e-5
```

### Reduce on Plateau

```bash
python src/training/train.py \
  hyperparameters.use_scheduler=true \
  hyperparameters.scheduler_type=plateau
```

## Model Selection

### SimpleCNN

```bash
python src/training/train.py model=simple_cnn
```

### ResNet

```bash
python src/training/train.py model=resnet
```

## Training Output

Training generates:
- **Best model**: `models/simple_cnn_best.pth`
- **Reports**: `reports/` directory with:
  - `confusion_matrix.png` - Confusion matrix visualization
  - `classification_report.txt` - Detailed metrics
  - `training_history.png` - Loss and accuracy curves

## Early Stopping

Configure early stopping patience:

```bash
python src/training/train.py early_stopping_patience=10
```

## Device Configuration

### Auto-detect (default)

```bash
python src/training/train.py device=auto
```

### Explicit GPU

```bash
python src/training/train.py device=cuda:0
```

### CPU only

```bash
python src/training/train.py device=cpu
```

## Monitoring Training

The training script provides real-time updates:
- Loss and accuracy per epoch
- Learning rate schedule
- Best validation accuracy
- Training history plots

## Tips for Better Results

1. **Data augmentation**: Adjust in `src/data/make_dataset.py`
2. **Batch size**: Larger batches for better GPU utilization
3. **Learning rate**: Start with 0.001 and tune based on results
4. **Epochs**: Use early stopping to avoid overfitting
5. **Optimizer**: Adam for adaptive learning, SGD for stable training
