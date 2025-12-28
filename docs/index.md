# End-to-End Image Classifier with MLOps

Welcome to the documentation for the End-to-End Image Classifier project! This project demonstrates complete MLOps best practices with full automation for building, training, and deploying image classification models.

## 🎯 Project Overview

This project implements a comprehensive MLOps pipeline for image classification, demonstrating:

- **Standardized Project Structure**: Clean, maintainable codebase following industry standards
- **Configuration Management**: Flexible experiment configuration with Hydra
- **Data Versioning**: Track datasets with DVC
- **Experiment Tracking**: MLflow and Weights & Biases integration
- **Pre-commit Hooks**: Automated code formatting and quality checks
- **Security Scanning**: Bandit for vulnerability detection
- **Dependency Checking**: Safety and pip-audit for package vulnerabilities
- **Docker Optimization**: Multi-stage builds for production
- **Kubernetes Deployment**: Production-ready K8s manifests with auto-scaling
- **Automated Testing**: Comprehensive test suite with pytest
- **CI/CD**: Complete GitHub Actions workflows
- **Documentation**: Full documentation with MkDocs

## 🚀 Quick Start

Get started in 3 simple steps:

```bash
# 1. Clone the repository
git clone https://github.com/Hadayxinchao/end-to-end-image-classifier.git
cd end-to-end-image-classifier

# 2. Run automated setup
./scripts/quickstart.sh

# 3. Train with W&B tracking
make train-wandb
```

## ✨ Automation Features

### 🔧 Pre-commit Hooks
Automatically format and check your code before every commit:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting with docstring checks
- **Bandit** - Security scanning
- **mypy** - Type checking
- **detect-secrets** - Secret detection

```bash
make setup-precommit
# Now every commit automatically checks and formats code!
```

### 🔒 Security & Quality
Comprehensive security and quality checks:

```bash
# Security scan
make security-scan

# Check dependency vulnerabilities
make vulnerability-check

# All quality checks
make quality-check
```

### 🐳 Production-Ready Deployment
Deploy with confidence:

**Docker:**
- Multi-stage optimized builds
- Non-root user for security
- Health checks
- Complete monitoring stack (MLflow, Prometheus, Grafana)

```bash
make docker-build-optimized
make docker-compose-up
```

**Kubernetes:**
- Auto-scaling (2-10 pods)
- LoadBalancer service
- HTTPS ingress
- Persistent storage
- Resource limits
- Prometheus monitoring

```bash
make k8s-deploy
make k8s-status
```

### 📊 Enhanced Experiment Tracking
Track everything with Weights & Biases:

- Model architecture and hyperparameters
- Training/validation metrics
- Weight and bias histograms
- Gradient distributions
- Model checkpoints
- Code versioning

```bash
# Setup W&B
make wandb-setup

# Train with tracking
make train-wandb

# Run hyperparameter sweeps
python scripts/wandb_sweep.py
```

## 📚 Key Features

### Smart Configuration Management

Use Hydra to manage all configurations without touching code:

```bash
# Override learning rate
python src/training/train.py hyperparameters.learning_rate=0.001

# Use different model
python src/training/train.py model=resnet

# Track with W&B
python src/training/train.py tracking=wandb

# Use both MLflow and W&B
python src/training/train.py tracking=wandb tracking.backend=both
```

### Data Version Control

Never lose track of your datasets:

```bash
# Track data with DVC
dvc add data/raw

# Push to remote storage
dvc push

# Pull data from any commit
git checkout <commit>
dvc pull
```

### Automated Testing

Ensure code quality with comprehensive tests:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Quick tests only
pytest tests/ -m "not slow"
```

### Experiment Tracking

Track and compare experiments:

```bash
# MLflow UI
mlflow ui
# Visit http://localhost:5000

# W&B Dashboard
# Visit https://wandb.ai/your-username/image-classifier

# Compare experiments
python scripts/compare_experiments.py
```

## 💻 Development Workflow

### 1. Start a New Feature

```bash
# Create branch
git checkout -b feature/new-feature

# Make changes
# Pre-commit hooks run automatically on commit!
```

### 2. Run Quality Checks

```bash
# Format code
make format

# Check linting
make lint

# Run tests
make test

# Security checks
make security-all
```

### 3. Train and Experiment

```bash
# Train with tracking
make train-wandb

# Try different configs
python src/training/train.py model=resnet hyperparameters.learning_rate=0.01
```

### 4. Deploy

```bash
# Build Docker image
make docker-build-optimized

# Deploy to Kubernetes
make k8s-deploy

# Monitor deployment
make k8s-status
```

## 📖 Documentation Structure

- **[Getting Started](getting-started/installation.md)** - Installation and setup
- **[User Guide](guide/training.md)** - Training, inference, and data management
- **[MLOps](mlops/automation.md)** - Complete automation guide
  - [Automation Guide](mlops/automation.md) - Pre-commit, security, deployment
  - [CI/CD Pipeline](mlops/cicd.md) - GitHub Actions workflows
  - [Data Versioning](mlops/dvc.md) - DVC setup and usage
  - [Experiment Tracking](mlops/experiment-tracking.md) - MLflow and W&B
  - [Docker](mlops/docker.md) - Docker usage and optimization
  - [Tracking Cheatsheet](mlops/tracking-cheatsheet.md) - Quick reference
- **[API Reference](api/data.md)** - Code documentation
- **[Development](development/contributing.md)** - Contributing guidelines

## 🎯 Common Tasks

### Training

```bash
# Quick test training
make train-fast

# Full training with W&B
make train-wandb

# Offline W&B mode
make train-wandb-offline

# Both MLflow and W&B
make train-both
```

### Code Quality

```bash
# Format all code
make format

# Check linting
make lint

# Type checking
make type-check

# All checks
make quality-check
```

### Docker

```bash
# Build optimized image
make docker-build-optimized

# Start full stack
make docker-compose-up

# Stop stack
make docker-compose-down
```

### Kubernetes

```bash
# Deploy
make k8s-deploy

# Check status
make k8s-status

# View logs
make k8s-logs

# Port forward
make k8s-port-forward

# Delete deployment
make k8s-delete
```

### Help

```bash
# View all available commands
make help
```

## 🛠️ Tech Stack

**ML/DL:**
- PyTorch
- torchvision
- scikit-learn

**MLOps:**
- Hydra (configuration)
- DVC (data versioning)
- MLflow (experiment tracking)
- Weights & Biases (experiment tracking)
- CML (continuous ML)

**Code Quality:**
- Black (formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- pytest (testing)
- Bandit (security)
- Safety (dependency checking)

**DevOps:**
- Docker
- Kubernetes
- GitHub Actions
- Prometheus
- Grafana

**Documentation:**
- MkDocs
- Material theme

## 📊 Project Metrics

- **Code Coverage**: 80%+
- **Security Scans**: Automated with Bandit
- **Type Coverage**: mypy enabled
- **Documentation**: 100% coverage
- **Pre-commit Hooks**: 12 hooks
- **CI/CD**: 4 automated jobs

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](development/contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [License](about/license.md) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/Hadayxinchao/end-to-end-image-classifier)
- [Documentation](https://hadayxinchao.github.io/end-to-end-image-classifier/)
- [Issues](https://github.com/Hadayxinchao/end-to-end-image-classifier/issues)

## 🙏 Acknowledgments

This project demonstrates MLOps best practices and industry-standard tools for production ML systems.

---

**Ready to get started?** Head to the [Installation Guide](getting-started/installation.md)!
