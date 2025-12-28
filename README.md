# End-to-End Image Classifier with MLOps

A complete MLOps pipeline for image classification demonstrating best practices in ML engineering.

## 🎯 Project Overview

This project implements a full MLOps workflow for image classification, covering:
- ✅ Standardized project structure
- ✅ Configuration management with Hydra
- ✅ Data versioning with DVC
- ✅ **Experiment tracking with MLflow and W&B**
- ✅ **Pre-commit hooks & Auto-formatting**
- ✅ **Security scanning with Bandit**
- ✅ **Dependency vulnerability checking**
- ✅ **Docker optimization (multi-stage)**
- ✅ **Kubernetes deployment (production-ready)**
- ✅ **Weights & Biases tracking**
- ✅ Unit testing with pytest
- ✅ CI/CD with GitHub Actions
- ✅ Docker containerization
- ✅ Documentation with MkDocs

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/Hadayxinchao/end-to-end-image-classifier.git
cd end-to-end-image-classifier

# 2. Install dependencies
pip install -r requirements.txt
pip install -e .

# 3. Setup pre-commit hooks
make setup-precommit

# 4. Setup W&B
make wandb-setup

# 5. Start training with W&B tracking
make train-wandb
```

## 📚 Documentation

- **[MLOPS_AUTOMATION_GUIDE.md](MLOPS_AUTOMATION_GUIDE.md)** - Comprehensive automation guide
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete setup instructions
- **[DOCKER.md](DOCKER.md)** - Docker usage guide
- **[DVC_SETUP.md](DVC_SETUP.md)** - Data versioning setup
- **[EXPERIMENT_TRACKING.md](EXPERIMENT_TRACKING.md)** - Experiment tracking guide
- **[Online Documentation](https://hadayxinchao.github.io/end-to-end-image-classifier/)** - Full MkDocs documentation

## 📁 Project Structure

```
end-to-end-image-classifier/
│
├── .github/
│   └── workflows/          # GitHub Actions workflows
│       ├── tests.yaml      # CI pipeline
│       └── cml.yaml        # CML pipeline
│
├── configs/                # Hydra configuration files
│   ├── config.yaml         # Main config
│   ├── model/              # Model configs
│   ├── data/               # Data configs
│   └── hyperparameters/    # Training hyperparameters
│
├── data/
│   ├── raw/                # Original immutable data
│   ├── processed/          # Processed data
│   └── .gitkeep
│
├── docs/                   # MkDocs documentation
│   ├── index.md
│   └── ...
│
├── models/                 # Trained models
│   └── .gitkeep
│
├── notebooks/              # Jupyter notebooks for exploration
│   └── exploratory/
│
├── reports/                # Generated reports and figures
│   └── figures/
│
├── src/                    # Source code
│   ├── __init__.py
│   ├── data/               # Data loading and processing
│   │   ├── __init__.py
│   │   └── make_dataset.py
│   ├── models/             # Model architectures
│   │   ├── __init__.py
│   │   ├── model.py
│   │   └── predict.py
│   ├── training/           # Training scripts
│   │   ├── __init__.py
│   │   └── train.py
│   └── utils/              # Utility functions
│       ├── __init__.py
│       └── metrics.py
│
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_model.py
│   └── test_training.py
│
├── .dvcignore
├── .gitignore
├── Dockerfile
├── requirements.txt
├── setup.py
├── mkdocs.yml
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone git@github.com:Hadayxinchao/end-to-end-image-classifier.git
cd end-to-end-image-classifier
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize DVC:
```bash
dvc init
```

### Usage

#### Training

```bash
# Train with default config
python src/training/train.py

# Train with experiment tracking (MLflow)
python src/training/train.py tracking=mlflow

# Train with Weights & Biases
python src/training/train.py tracking=wandb

# Override parameters
python src/training/train.py hyperparameters.learning_rate=0.001 hyperparameters.batch_size=64

# Use different config
python src/training/train.py model=resnet data=mnist
```

#### Experiment Tracking

```bash
# Setup experiment tracking
./scripts/setup_tracking.sh

# View MLflow UI
mlflow ui

# Compare experiments
python scripts/compare_experiments.py --experiment image_classifier

# Run hyperparameter sweep (W&B)
python scripts/wandb_sweep.py
```

See [EXPERIMENT_TRACKING.md](EXPERIMENT_TRACKING.md) for detailed usage.

#### Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_model.py -v

# Run with coverage
pytest --cov=src tests/
```

#### Inference

```bash
python src/models/predict.py --model_path models/best_model.pth --image_path data/test/image.jpg
```

## 🐳 Docker

Build and run the Docker container:

```bash
# Build image
docker build -t image-classifier:latest .

# Run container
docker run -p 8000:8000 image-classifier:latest
```

## 📊 DVC - Data Version Control

```bash
# Track data
dvc add data/raw/

# Push to remote storage
dvc push

# Pull data
dvc pull
```

## 🧪 Testing

The project includes comprehensive unit tests:
- Data loading and preprocessing
- Model architecture and output shapes
- Loss function behavior
- Training utilities

## 📈 Continuous ML (CML)

CML automatically generates reports on each pull request:
- Training metrics
- Confusion matrix
- Classification report
- Model performance comparison

## 📚 Documentation

Documentation is built with MkDocs:

```bash
# Serve locally
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## 🔧 Configuration Management

Hydra manages all configurations in `configs/` directory. You can:
- Override any parameter from command line
- Create experiment configs
- Use config composition

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/`
5. Submit a pull request

## 📝 License

MIT License

## 👤 Author

Bui Ha - MLOps Course Project

## 🙏 Acknowledgments

- Cookiecutter Data Science template
- MLOps best practices from industry
