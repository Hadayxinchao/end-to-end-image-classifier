# Code Style

Code style guidelines and standards for this project.

## Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with tools for enforcement:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

## Running Style Checks

### Format Code with Black

```bash
# Format all Python files
black src/ tests/

# Format specific file
black src/training/train.py

# Check without modifying
black --check src/
```

### Sort Imports with isort

```bash
# Sort imports
isort src/ tests/

# Check without modifying
isort --check-only src/
```

### Lint with flake8

```bash
# Run linter
flake8 src/ tests/

# Show statistics
flake8 --statistics src/
```

### Type Check with mypy

```bash
# Run type checker
mypy src/

# Strict mode
mypy --strict src/
```

## Code Style Rules

### Naming Conventions

```python
# Constants: UPPER_CASE
LEARNING_RATE = 0.001
MAX_EPOCHS = 100

# Functions and variables: snake_case
def train_model(data_loader, model):
    pass

# Classes: PascalCase
class SimpleCNN(torch.nn.Module):
    pass

# Private methods: _leading_underscore
def _preprocess_data(data):
    pass
```

### Line Length

Maximum 88 characters (Black default):

```python
# Good - fits within 88 chars
result = some_function(arg1, arg2, arg3)

# Bad - exceeds 88 chars
result = some_very_long_function_name(argument_one, argument_two, argument_three)

# Good - break long lines
result = some_very_long_function_name(
    argument_one,
    argument_two,
    argument_three
)
```

### Imports

```python
# Good - grouped and sorted
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.models.model import SimpleCNN
from src.utils.metrics import calculate_metrics

# Bad - unsorted, mixed order
from src.models.model import SimpleCNN
import sys
import torch
from src.utils.metrics import calculate_metrics
import os
```

### Docstring Format

Use Google-style docstrings:

```python
def train_model(
    model: torch.nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    num_epochs: int = 50,
    learning_rate: float = 0.001
) -> Dict[str, List[float]]:
    """Train a neural network model.

    Long description of what this function does,
    including important details and context.

    Args:
        model: PyTorch model to train
        train_loader: Training data loader
        val_loader: Validation data loader
        num_epochs: Number of training epochs. Defaults to 50.
        learning_rate: Learning rate for optimizer. Defaults to 0.001.

    Returns:
        Dictionary containing training history with keys:
        - 'train_loss': List of training losses
        - 'val_loss': List of validation losses
        - 'train_acc': List of training accuracies
        - 'val_acc': List of validation accuracies

    Raises:
        ValueError: If num_epochs <= 0
        TypeError: If model is not a torch.nn.Module

    Example:
        >>> model = SimpleCNN()
        >>> history = train_model(model, train_loader, val_loader)
        >>> print(history['val_acc'][-1])

    Note:
        This function modifies the model in-place.

    See Also:
        validate() - Function for model validation
    """
    pass
```

### Type Hints

Always use type hints:

```python
# Good
def process_batch(
    images: torch.Tensor,
    labels: torch.Tensor,
    device: torch.device
) -> Tuple[torch.Tensor, torch.Tensor]:
    images = images.to(device)
    labels = labels.to(device)
    return images, labels

# Bad
def process_batch(images, labels, device):
    images = images.to(device)
    labels = labels.to(device)
    return images, labels

# Optional types
from typing import Optional

def train_model(
    model: torch.nn.Module,
    checkpoint_path: Optional[str] = None
) -> Dict[str, Any]:
    if checkpoint_path is not None:
        load_checkpoint(model, checkpoint_path)
    return {}
```

### String Formatting

Use f-strings:

```python
# Good
name = "CIFAR-10"
print(f"Training on {name} dataset")

# OK but less readable
print("Training on {} dataset".format(name))

# Avoid
print("Training on " + name + " dataset")
```

### Whitespace

```python
# Good - proper spacing
def calculate_metrics(predictions: np.ndarray, labels: np.ndarray) -> float:
    accuracy = (predictions == labels).sum() / len(labels)
    return accuracy

# Bad - inconsistent spacing
def calculate_metrics(predictions:np.ndarray,labels:np.ndarray)->float:
    accuracy=(predictions==labels).sum()/len(labels)
    return accuracy
```

### List/Dict Comprehensions

Use comprehensions for readability:

```python
# Good
squares = [x ** 2 for x in range(10)]
even_numbers = {x: x**2 for x in range(10) if x % 2 == 0}

# Acceptable but less readable
squares = []
for x in range(10):
    squares.append(x ** 2)
```

### Comments

```python
# Good - explains WHY, not WHAT
# Use exponential moving average for smoother loss tracking
smoothed_loss = 0.99 * smoothed_loss + 0.01 * current_loss

# Bad - just repeats the code
# Multiply smoothed_loss by 0.99 and add current_loss multiplied by 0.01
smoothed_loss = 0.99 * smoothed_loss + 0.01 * current_loss

# Good - explain non-obvious logic
# We use 32x32 for CIFAR-10 to match standard benchmark size
image_size = 32
```

## File Organization

### Module Structure

```python
# src/models/model.py

"""CNN architectures for image classification."""

import torch
import torch.nn as nn
from typing import Optional

# Constants first
DEFAULT_IMAGE_SIZE = 32
DEFAULT_NUM_CLASSES = 10

# Then functions
def get_model(model_name: str, **kwargs) -> nn.Module:
    """Factory function for creating models."""
    pass

# Then classes
class SimpleCNN(nn.Module):
    """Simple CNN for image classification."""
    pass

class ResNet(nn.Module):
    """ResNet architecture."""
    pass
```

## Linting Configuration

### flake8 Configuration

```ini
# setup.cfg or .flake8
[flake8]
max-line-length = 88
exclude = .git,__pycache__,venv
ignore = E203,W503
```

### isort Configuration

```ini
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_mode = 3
include_trailing_comma = true
```

### mypy Configuration

```ini
# mypy.ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True
```

## Pre-commit Hooks

Automatically format code before commit:

```bash
# Install
pip install pre-commit

# Setup
pre-commit install

# Run manually
pre-commit run --all-files
```

## IDE Integration

### VS Code

Install extensions:
- Python
- Pylance
- Black Formatter
- isort

Add to `.vscode/settings.json`:

```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

## Checklist Before Commit

- [ ] Code formatted with Black
- [ ] Imports sorted with isort
- [ ] No flake8 warnings
- [ ] Type hints added
- [ ] Docstrings present
- [ ] Tests pass
- [ ] No commented-out code
