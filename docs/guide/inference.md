# Making Predictions

This guide explains how to use trained models for inference.

## Batch Prediction

Predict on a batch of images:

```python
import torch
from pathlib import Path
from src.models.model import get_model
from src.models.predict import predict_batch
from src.data.make_dataset import load_cifar10

# Load model
model = get_model(
    model_name="simple_cnn",
    num_classes=10,
    input_channels=3,
    image_size=32
)

# Load checkpoint
checkpoint = torch.load("models/simple_cnn_best.pth")
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Load data
_, _, test_loader = load_cifar10(batch_size=32)

# Make predictions
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
predictions, true_labels = predict_batch(model, test_loader, device)
```

## Single Image Prediction

Predict on a single image:

```python
import torch
import torchvision.transforms as transforms
from PIL import Image
from src.models.model import get_model

# Load model
model = get_model(
    model_name="simple_cnn",
    num_classes=10,
    input_channels=3,
    image_size=32
)

# Load checkpoint
checkpoint = torch.load("models/simple_cnn_best.pth")
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Prepare image
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

image = Image.open("path/to/image.jpg")
image_tensor = transform(image).unsqueeze(0)

# Predict
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
image_tensor = image_tensor.to(device)

with torch.no_grad():
    output = model(image_tensor)
    probabilities = torch.softmax(output, dim=1)
    prediction = output.argmax(dim=1).item()
    confidence = probabilities[0][prediction].item()

print(f"Prediction: {prediction}, Confidence: {confidence:.2%}")
```

## Command Line Inference

Use the prediction script:

```bash
python src/models/predict.py \
    --model_path models/simple_cnn_best.pth \
    --image_path path/to/image.jpg \
    --device cuda
```

## Batch Processing

Process multiple images:

```python
import torch
from pathlib import Path
from src.models.model import get_model
from src.models.predict import predict_batch
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import torchvision.transforms as transforms

# Prepare data
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

dataset = ImageFolder("path/to/images", transform=transform)
data_loader = DataLoader(dataset, batch_size=32, num_workers=4)

# Load model
model = get_model(
    model_name="simple_cnn",
    num_classes=10,
    input_channels=3,
    image_size=32
)

checkpoint = torch.load("models/simple_cnn_best.pth")
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Predict
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
predictions, labels = predict_batch(model, data_loader, device)
```

## Output Format

Predictions are returned as:
- **predictions**: Numpy array of predicted class indices
- **true_labels**: Numpy array of true labels (if available)
- **probabilities**: Softmax probabilities for each class

## Class Labels

CIFAR-10 classes:
- 0: airplane
- 1: automobile
- 2: bird
- 3: cat
- 4: deer
- 5: dog
- 6: frog
- 7: horse
- 8: ship
- 9: truck

MNIST classes:
- 0-9: Digits

## Performance Metrics

Calculate prediction metrics:

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

accuracy = accuracy_score(true_labels, predictions)
precision = precision_score(true_labels, predictions, average='macro')
recall = recall_score(true_labels, predictions, average='macro')
f1 = f1_score(true_labels, predictions, average='macro')

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print("\nClassification Report:")
print(classification_report(true_labels, predictions))
```
