# Contributing

Guidelines for contributing to this project.

## Getting Started

### Fork and Clone

```bash
# Fork on GitHub, then
git clone https://github.com/Hadayxinchao/end-to-end-image-classifier.git
cd end-to-end-image-classifier
git remote add upstream https://github.com/original/end-to-end-image-classifier.git
```

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

## Development Workflow

### Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Make Changes

Follow the code style guidelines (see [Code Style](code-style.md)).

### Write Tests

Add tests in `tests/` directory:

```python
# tests/test_my_feature.py
import pytest
from src.module import function

def test_function():
    assert function(input) == expected_output
```

### Run Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_my_feature.py

# With coverage
pytest --cov=src tests/
```

### Commit Changes

```bash
git add .
git commit -m "Add feature: description"
```

### Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Standards

### Python Style

Follow PEP 8 and use:
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

### Type Hints

Use type hints for all functions:

```python
from typing import List, Tuple
import numpy as np

def process_batch(
    images: np.ndarray,
    labels: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """Process a batch of images and labels.

    Args:
        images: Image array of shape (B, C, H, W)
        labels: Label array of shape (B,)

    Returns:
        Processed images and labels
    """
    return images, labels
```

### Docstrings

Use Google-style docstrings:

```python
def train_model(
    train_loader,
    val_loader,
    num_epochs: int = 50,
    learning_rate: float = 0.001
) -> dict:
    """Train a model.

    Args:
        train_loader: Training data loader
        val_loader: Validation data loader
        num_epochs: Number of training epochs
        learning_rate: Learning rate for optimizer

    Returns:
        Dictionary containing training history

    Raises:
        ValueError: If num_epochs <= 0

    Example:
        >>> history = train_model(train_loader, val_loader)
        >>> print(history['accuracy'])
    """
    if num_epochs <= 0:
        raise ValueError("num_epochs must be positive")

    # Implementation
    return {}
```

## Testing Guidelines

### Test Structure

```python
# tests/test_models.py
import pytest
import torch
from src.models.model import SimpleCNN, get_model

class TestSimpleCNN:
    """Test SimpleCNN model."""

    @pytest.fixture
    def model(self):
        """Create test model."""
        return SimpleCNN(num_classes=10, image_size=32)

    def test_initialization(self, model):
        """Test model initialization."""
        assert model is not None

    def test_forward_pass(self, model):
        """Test forward pass."""
        x = torch.randn(2, 3, 32, 32)
        y = model(x)
        assert y.shape == (2, 10)

    @pytest.mark.parametrize("image_size", [28, 32, 64])
    def test_different_sizes(self, image_size):
        """Test model with different input sizes."""
        model = SimpleCNN(num_classes=10, image_size=image_size)
        x = torch.randn(2, 3, image_size, image_size)
        y = model(x)
        assert y.shape == (2, 10)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test class
pytest tests/test_models.py::TestSimpleCNN

# Run specific test
pytest tests/test_models.py::TestSimpleCNN::test_forward_pass

# Run with coverage report
pytest --cov=src --cov-report=html tests/
```

## Documentation

### Update Documentation

1. Update relevant `.md` file in `docs/`
2. Follow Markdown format
3. Include code examples where applicable

### Build Documentation Locally

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

Then visit `http://localhost:8000`

## Reporting Issues

### Bug Reports

Create an issue with:
- **Title**: Clear, concise description
- **Description**: What happened, what should happen
- **Reproduction**: Steps to reproduce
- **Environment**: Python version, OS, packages

### Feature Requests

Describe:
- **Use case**: Why it's needed
- **Proposed solution**: How to implement
- **Alternatives**: Other approaches considered

## PR Review Process

1. **Check automated tests**: Must pass all CI/CD checks
2. **Code review**: 2 approvals required
3. **Documentation**: Updated if needed
4. **Merge**: Squash and merge to main

## Getting Help

- **Discussions**: GitHub Discussions
- **Issues**: GitHub Issues
- **Documentation**: Read the docs site
- **Email**: Contact maintainers

## Code of Conduct

- Be respectful and inclusive
- No harassment or discrimination
- Assume good faith
- Give and accept constructive feedback

Thank you for contributing! 🎉
