# Installation Guide

This guide will help you set up the Image Classifier project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads/)
- **pip**: Python package installer (usually comes with Python)
- **(Optional) Docker**: [Download Docker](https://www.docker.com/get-started)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/end-to-end-image-classifier.git
cd end-to-end-image-classifier
```

### 2. Create Virtual Environment

It's recommended to use a virtual environment to avoid dependency conflicts.

=== "Linux/Mac"
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

=== "Windows"
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

### 4. Verify Installation

Run the tests to ensure everything is working:

```bash
pytest tests/ -v -m "not slow"
```

If all tests pass, you're ready to go! ✅

## Optional: Setup DVC

If you want to use Data Version Control:

```bash
# Initialize DVC
dvc init

# Add remote storage (example: local storage)
dvc remote add -d storage /tmp/dvc-storage
```

For more details, see the [Data Versioning Guide](../mlops/dvc.md).

## Optional: Setup Docker

Build the Docker image:

```bash
docker build -t image-classifier:latest .
```

Test the Docker image:

```bash
docker run --rm image-classifier:latest python --version
```

## Development Setup

If you plan to contribute to the project:

### Install Development Dependencies

```bash
pip install -r requirements.txt
```

This includes:
- `pytest` - Testing framework
- `black` - Code formatter
- `flake8` - Linter
- `mypy` - Type checker

### Setup Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

## Troubleshooting

### Issue: PyTorch Installation Fails

If you have GPU and want CUDA support:

```bash
# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

For CPU-only:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Permission Denied

On Linux/Mac, you might need to use `sudo` or fix permissions:

```bash
sudo chown -R $USER:$USER .
```

### Issue: Module Not Found

Make sure you installed the package:

```bash
pip install -e .
```

And that your virtual environment is activated.

## Next Steps

Now that you've installed the project, check out:

- [Quick Start Guide](quickstart.md) - Train your first model
- [Configuration Guide](configuration.md) - Learn about Hydra configs
- [User Guide](../guide/training.md) - Detailed training instructions

## System Requirements

### Minimum Requirements

- **CPU**: Dual-core processor
- **RAM**: 4 GB
- **Storage**: 2 GB free space
- **OS**: Linux, macOS, or Windows 10+

### Recommended Requirements

- **CPU**: Quad-core processor or better
- **RAM**: 8 GB or more
- **GPU**: NVIDIA GPU with CUDA support (for faster training)
- **Storage**: 10 GB free space (for datasets and models)
- **OS**: Ubuntu 20.04+ or equivalent

## Getting Help

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search [GitHub Issues](https://github.com/yourusername/end-to-end-image-classifier/issues)
3. Create a new issue with details about your problem
