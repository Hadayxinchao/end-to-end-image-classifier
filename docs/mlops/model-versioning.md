# Model Versioning

Manage and version trained models for reproducibility and deployment.

## Model Storage

### Local Storage

Models are saved to `models/` directory:

```
models/
├── simple_cnn_best.pth      # Best SimpleCNN checkpoint
├── resnet_best.pth          # Best ResNet checkpoint
└── archived/
    ├── simple_cnn_v1.pth    # Previous version
    └── resnet_v1.pth
```

### Model Checkpoint Format

Each checkpoint contains:

```python
{
    'epoch': int,                       # Training epoch
    'model_state_dict': dict,          # Model weights
    'optimizer_state_dict': dict,      # Optimizer state
    'val_acc': float,                  # Validation accuracy
    'config': dict                     # Training configuration
}
```

## Model Versioning with Git

### Tag Model Releases

```bash
# Create tag for model version
git tag model-v1.0 -m "SimpleCNN on CIFAR-10: 85% accuracy"

# List tags
git tag -l

# Push tags
git push origin --tags
```

### Store Model Info

Create `MODELS.md` to track model versions:

```markdown
# Model Registry

## SimpleCNN v1.0
- Dataset: CIFAR-10
- Accuracy: 85.2%
- Parameters: 1.2M
- Training Time: 2.5 hours
- Config: learning_rate=0.001, epochs=50
- Commit: abc123def456
- Date: 2025-12-10

## ResNet v1.0
- Dataset: CIFAR-10
- Accuracy: 91.5%
- Parameters: 2.1M
- Training Time: 4 hours
- Config: learning_rate=0.0001, epochs=100
```

## Version Control with DVC

### Track Model Files

```bash
# Add model to DVC
dvc add models/simple_cnn_best.pth

# Commit DVC metadata
git add models/simple_cnn_best.pth.dvc
git commit -m "Add SimpleCNN v1.0 model"
```

### Push to Remote

```bash
# Push model to remote storage
dvc push models/simple_cnn_best.pth.dvc

# Pull model from remote
dvc pull models/simple_cnn_best.pth.dvc
```

## Loading Models

### Load Checkpoint

```python
import torch
from src.models.model import get_model

# Create model
model = get_model(
    model_name="simple_cnn",
    num_classes=10,
    image_size=32
)

# Load checkpoint
checkpoint = torch.load("models/simple_cnn_best.pth")
model.load_state_dict(checkpoint['model_state_dict'])

# Get metadata
epoch = checkpoint['epoch']
val_acc = checkpoint['val_acc']
config = checkpoint['config']

print(f"Model trained at epoch {epoch}: {val_acc:.2%} accuracy")
```

### Load Optimizer State (for resuming training)

```python
import torch
from torch.optim import Adam
from src.models.model import get_model

# Create model and optimizer
model = get_model("simple_cnn", num_classes=10, image_size=32)
optimizer = Adam(model.parameters())

# Load checkpoint
checkpoint = torch.load("models/simple_cnn_best.pth")
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

# Resume training from epoch
start_epoch = checkpoint['epoch'] + 1
```

## Model Comparison

### Compare Multiple Models

```python
import torch
from pathlib import Path
from src.models.model import get_model
import json

def compare_models(models_dir="models"):
    results = []
    
    for model_file in Path(models_dir).glob("*_best.pth"):
        checkpoint = torch.load(model_file)
        
        results.append({
            'model': model_file.stem,
            'epoch': checkpoint['epoch'],
            'val_acc': checkpoint['val_acc'],
            'config': checkpoint['config']
        })
    
    # Sort by accuracy
    results.sort(key=lambda x: x['val_acc'], reverse=True)
    
    print("Model Comparison:")
    for result in results:
        print(f"{result['model']}: {result['val_acc']:.2%}")
    
    return results
```

## Versioning Best Practices

### 1. Semantic Versioning

Follow MAJOR.MINOR.PATCH:

- **MAJOR**: Architecture changes or significant accuracy improvements
- **MINOR**: Hyperparameter tuning, dataset version updates
- **PATCH**: Bug fixes, minor adjustments

```bash
# Version naming
models/simple_cnn_v1.0.0.pth   # MAJOR change
models/simple_cnn_v1.1.0.pth   # MINOR improvement
models/simple_cnn_v1.0.1.pth   # PATCH fix
```

### 2. Metadata Documentation

Store with each model:

```yaml
# models/simple_cnn_v1.0.0_metadata.yaml
name: SimpleCNN
version: 1.0.0
dataset: CIFAR-10
task: image_classification
metrics:
  accuracy: 0.852
  precision: 0.851
  recall: 0.852
  f1_score: 0.851
architecture:
  num_classes: 10
  input_channels: 3
  image_size: 32
  total_params: 1200000
training:
  epochs: 50
  learning_rate: 0.001
  optimizer: adam
  batch_size: 32
  training_time_hours: 2.5
  gpu: NVIDIA RTX 3080
date: 2025-12-10
git_commit: abc123def456
author: Your Name
notes: "Best model on validation set"
```

### 3. Model Registry

Maintain central registry:

```python
# models/registry.json
{
  "models": [
    {
      "id": "simple_cnn_v1.0.0",
      "name": "SimpleCNN v1.0.0",
      "path": "models/simple_cnn_best.pth",
      "accuracy": 0.852,
      "created": "2025-12-10",
      "status": "production"
    },
    {
      "id": "resnet_v1.0.0",
      "name": "ResNet v1.0.0",
      "path": "models/resnet_best.pth",
      "accuracy": 0.915,
      "created": "2025-12-10",
      "status": "production"
    }
  ]
}
```

## Integration with MLflow (Optional)

Track models with MLflow:

```bash
pip install mlflow
```

```python
import mlflow
from src.models.model import get_model

mlflow.start_run()

model = get_model("simple_cnn", num_classes=10, image_size=32)
# ... training code ...

# Log metrics
mlflow.log_metrics({'val_acc': 0.852, 'val_loss': 0.450})

# Log model
mlflow.pytorch.log_model(model, "models/simple_cnn")

# Log artifacts
mlflow.log_artifact("models/simple_cnn_best.pth")

mlflow.end_run()
```

View models:

```bash
mlflow ui
```

## Deployment

### Export Model for Production

```python
import torch
from src.models.model import get_model

# Load trained model
checkpoint = torch.load("models/simple_cnn_best.pth")
model = get_model("simple_cnn", num_classes=10, image_size=32)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Export to TorchScript for faster inference
scripted_model = torch.jit.script(model)
scripted_model.save("models/simple_cnn_scripted.pt")

# Export to ONNX for cross-platform support
dummy_input = torch.randn(1, 3, 32, 32)
torch.onnx.export(
    model, dummy_input,
    "models/simple_cnn.onnx",
    input_names=['input'],
    output_names=['output'],
    opset_version=11
)
```

### Model Serving

See Docker section for containerized serving.

## Cleanup & Archival

### Archive Old Models

```bash
# Create archive directory
mkdir -p models/archive
mv models/simple_cnn_old.pth models/archive/

# Compress archives
tar -czf models/archive_2025_12_01.tar.gz models/archive/
```

### Keep Storage Clean

```bash
# Remove intermediate checkpoints (keep only best)
find models/ -name "*_epoch_*.pth" -delete

# Check disk usage
du -sh models/
```

## Troubleshooting

### Model Loading Error

```python
# Check file exists and is accessible
from pathlib import Path
model_path = Path("models/simple_cnn_best.pth")
assert model_path.exists(), "Model file not found"

# Try loading with map_location for cross-device compatibility
device = torch.device("cpu")
checkpoint = torch.load(
    model_path,
    map_location=device
)
```

### Version Mismatch

Ensure PyTorch versions match:

```bash
# Check PyTorch version when saving
python -c "import torch; print(torch.__version__)"

# Specify version in requirements
torch==2.0.0
```

## References

- [PyTorch Model Saving](https://pytorch.org/tutorials/beginner/saving_loading_models.html)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [ONNX Runtime](https://onnxruntime.ai/)
