# API Reference - Models Module

Auto-generated API documentation for the models module.

## Model Factory

### Get Model

::: src.models.model.get_model

## Model Classes

### SimpleCNN

::: src.models.model.SimpleCNN

### ResNet

::: src.models.model.ResNet

## Inference

### Batch Prediction

::: src.models.predict.predict_batch

## Module Contents

```
src/models/
├── __init__.py
├── model.py
│   ├── get_model()
│   ├── SimpleCNN
│   └── ResNet
├── predict.py
│   ├── predict_batch()
│   └── predict_single()
└── ...
```

## Model Architecture

### SimpleCNN

```
SimpleCNN(
    num_classes=10,
    input_channels=3,
    dropout=0.5,
    image_size=32
)
```

Structure:
- Conv Layer 1: 3 → 64 channels
- Conv Layer 2: 64 → 128 channels
- Conv Layer 3: 128 → 128 channels
- Fully Connected: 128*4*4 → 256 → num_classes

### ResNet

Standard ResNet architecture adapted for CIFAR-10/MNIST with:
- Residual blocks
- Batch normalization
- Global average pooling

## Example Usage

```python
import torch
from src.models.model import get_model

# Create model
model = get_model(
    model_name="simple_cnn",
    num_classes=10,
    input_channels=3,
    image_size=32,
    dropout=0.5
)

# Forward pass
batch = torch.randn(32, 3, 32, 32)
output = model(batch)
print(output.shape)  # [32, 10]

# Load checkpoint
checkpoint = torch.load("models/simple_cnn_best.pth")
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Predictions
with torch.no_grad():
    predictions = model(batch)
    probs = torch.softmax(predictions, dim=1)
    class_ids = predictions.argmax(dim=1)
```

## Model Properties

- **Total Parameters**: Varies by architecture
- **Input Size**: Configurable (32x32 for CIFAR-10, 28x28 for MNIST)
- **Output Size**: Number of classes (10)
- **Device**: CPU/CUDA compatible
