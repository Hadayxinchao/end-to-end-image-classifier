# Project Overview

End-to-end image classification project following MLOps best practices.

## Project Goals

This project demonstrates a production-ready machine learning pipeline with:

1. **Reproducibility**: Fixed seeds, versioned data, documented configurations
2. **Scalability**: Modular architecture supporting multiple models and datasets
3. **Maintainability**: Clean code, comprehensive tests, full documentation
4. **Automation**: CI/CD pipelines, automated testing, model versioning
5. **Best Practices**: DVC data versioning, Hydra config management, Docker containerization

## What's Included

### 1. Core Components

- **Data Management**: Automatic CIFAR-10 & MNIST loading with preprocessing
- **Model Architectures**: SimpleCNN and ResNet for image classification
- **Training Pipeline**: Configurable training with multiple optimizers and schedulers
- **Inference**: Batch and single-image prediction utilities
- **Evaluation**: Comprehensive metrics and visualization tools

### 2. MLOps Infrastructure

- **Configuration Management**: Hydra for reproducible experiments
- **Data Versioning**: DVC integration for dataset tracking
- **Unit Testing**: 30+ pytest tests covering data, models, and training
- **CI/CD**: GitHub Actions workflows for automated testing
- **Containerization**: Docker setup for reproducible environments
- **Documentation**: MkDocs with comprehensive guides and API reference

### 3. Code Quality

- **Code Formatting**: Black for consistent style
- **Import Sorting**: isort for organized imports
- **Linting**: flake8 for code quality checks
- **Type Checking**: mypy for static type verification

## Quick Start

### Installation

```bash
# Clone repository
git clone <repository-url>
cd end-to-end-image-classifier

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Training

```bash
# Train on CIFAR-10 (default)
python src/training/train.py

# Train on MNIST
python src/training/train.py data=mnist

# Custom configuration
python src/training/train.py \
    hyperparameters.learning_rate=0.001 \
    hyperparameters.num_epochs=100
```

### Making Predictions

```python
from src.models.model import get_model
from src.models.predict import predict_batch
from src.data.make_dataset import load_cifar10
import torch

# Load model and data
model = get_model("simple_cnn", num_classes=10, image_size=32)
checkpoint = torch.load("models/simple_cnn_best.pth")
model.load_state_dict(checkpoint['model_state_dict'])

_, _, test_loader = load_cifar10()

# Make predictions
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
predictions, labels = predict_batch(model, test_loader, device)
```

## Project Structure

```
.
├── src/                      # Source code
│   ├── data/                # Data loading and preprocessing
│   ├── models/              # Model architectures
│   ├── training/            # Training scripts
│   └── utils/               # Utility functions
├── tests/                    # Unit and integration tests
├── configs/                  # Hydra configuration files
├── data/                     # Data directory (gitignored)
├── models/                   # Model checkpoints (gitignored)
├── reports/                  # Training reports and visualizations
├── docs/                     # Documentation (MkDocs)
├── .github/workflows/        # CI/CD pipelines
├── Dockerfile                # Container setup
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project configuration
└── mkdocs.yml               # Documentation configuration
```

## Technology Stack

- **Framework**: PyTorch 2.0+
- **Configuration**: Hydra 1.3+
- **Data Versioning**: DVC 3.0+
- **Testing**: pytest 7.4+
- **CI/CD**: GitHub Actions
- **Container**: Docker
- **Documentation**: MkDocs Material
- **Code Quality**: Black, isort, flake8, mypy

## Performance

### Model Accuracy

- **CIFAR-10**: ~85% (SimpleCNN), ~90%+ (ResNet)
- **MNIST**: ~98%+ (both architectures)

### Training Time (CIFAR-10, SimpleCNN)

- **GPU**: ~2-3 minutes for 50 epochs
- **CPU**: ~15-20 minutes for 50 epochs

## Key Features

### Hydra Configuration Management

Easily modify training via command line or YAML configs:

```bash
python src/training/train.py \
    data=cifar10 \
    model=resnet \
    hyperparameters.learning_rate=0.001 \
    hyperparameters.batch_size=64
```

### Reproducibility

- Fixed random seeds for data and model
- Version control for code and configurations
- Data versioning with DVC
- Containerization for consistent environments

### Modular Architecture

- Easy to add new models in `src/models/`
- Simple to support new datasets in `src/data/`
- Extensible training pipeline in `src/training/`

### Comprehensive Testing

- Data loading tests
- Model architecture tests
- Training pipeline tests
- 90%+ code coverage

### Continuous Integration

Automated testing on every commit:
- Multi-Python version support (3.9, 3.10, 3.11, 3.12, 3.13)
- Linting and type checking
- Unit test execution

## Getting Started

See [Getting Started](../getting-started/installation.md) for installation instructions.

## Documentation

Full documentation available at:
- [Installation & Setup](../getting-started/installation.md)
- [Quick Start Guide](../getting-started/quickstart.md)
- [Configuration Guide](../getting-started/configuration.md)
- [Training Guide](../guide/training.md)
- [Inference Guide](../guide/inference.md)
- [API Reference](../api/data.md)

## Contributing

We welcome contributions! See [Contributing Guide](../development/contributing.md) for details.

## License

This project is licensed under the MIT License. See [License](license.md) for details.

## Authors

- Created as part of MLOps best practices demonstration
- Maintaining: Open to community contributions

## Acknowledgments

- PyTorch team for the excellent deep learning framework
- Hydra team for configuration management
- DVC team for data versioning
- GitHub for CI/CD infrastructure

## Citation

If you use this project in your research, please cite:

```bibtex
@misc{image-classifier-mlops,
  title={End-to-End Image Classifier with MLOps},
  author={Hoang Ha},
  year={2025},
  url={https://github.com/Hadayxinchao/end-to-end-image-classifier}
}
```

## Contact

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: [your-email]

## Roadmap

- [ ] Add more model architectures (EfficientNet, Vision Transformer)
- [ ] Support additional datasets (ImageNet, COCO)
- [ ] MLflow integration for experiment tracking
- [ ] Model serving with FastAPI
- [ ] Batch inference optimization
- [ ] GPU optimization (mixed precision training)
- [ ] Model quantization
- [ ] Federated learning support

## Related Resources

- [PyTorch Documentation](https://pytorch.org/docs/)
- [Hydra Documentation](https://hydra.cc/)
- [DVC Documentation](https://dvc.org/)
- [MLOps Guide](https://ml-ops.systems/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
