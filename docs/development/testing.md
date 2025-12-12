# Testing

Comprehensive guide to testing in this project.

## Test Structure

```
tests/
├── __init__.py
├── test_data.py         # Data loading tests
├── test_model.py        # Model architecture tests
├── test_training.py     # Training pipeline tests
└── fixtures/            # Test fixtures and mocks
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_model.py
```

### Run Specific Test Class

```bash
pytest tests/test_model.py::TestSimpleCNN
```

### Run Specific Test

```bash
pytest tests/test_model.py::TestSimpleCNN::test_forward_pass
```

### Verbose Output

```bash
pytest -v
```

### Show Print Statements

```bash
pytest -s
```

### Stop on First Failure

```bash
pytest -x
```

## Code Coverage

### Generate Coverage Report

```bash
pytest --cov=src tests/
```

### HTML Coverage Report

```bash
pytest --cov=src --cov-report=html tests/
```

View report in `htmlcov/index.html`

### Coverage Threshold

Configure in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing --cov-fail-under=80"
```

## Test Categories

### Unit Tests

Test individual functions:

```python
# tests/test_utils.py
from src.utils.metrics import AverageMeter

def test_average_meter():
    meter = AverageMeter()
    meter.update(10, 1)
    meter.update(20, 2)
    assert meter.avg == 15.0  # (10*1 + 20*2) / 3
```

### Integration Tests

Test module interactions:

```python
# tests/test_training.py
def test_training_pipeline(train_loader, val_loader):
    model = get_model("simple_cnn", num_classes=10, image_size=32)
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.CrossEntropyLoss()
    
    train_loss, train_acc = train_epoch(
        model, train_loader, criterion, optimizer, device
    )
    
    assert train_loss > 0
    assert 0 <= train_acc <= 100
```

### Parametrized Tests

Test multiple inputs:

```python
import pytest

@pytest.mark.parametrize("model_name", ["simple_cnn", "resnet"])
@pytest.mark.parametrize("image_size", [28, 32])
def test_models(model_name, image_size):
    model = get_model(model_name, num_classes=10, image_size=image_size)
    x = torch.randn(2, 3, image_size, image_size)
    y = model(x)
    assert y.shape == (2, 10)
```

## Test Fixtures

### Common Fixtures

```python
# tests/conftest.py
import pytest
import torch

@pytest.fixture
def device():
    return torch.device("cpu")

@pytest.fixture
def model():
    from src.models.model import SimpleCNN
    return SimpleCNN(num_classes=10, image_size=32)

@pytest.fixture
def sample_batch():
    images = torch.randn(4, 3, 32, 32)
    labels = torch.tensor([0, 1, 2, 3])
    return images, labels
```

### Using Fixtures

```python
def test_model_forward(model, sample_batch, device):
    images, labels = sample_batch
    images = images.to(device)
    
    output = model(images)
    assert output.shape == (4, 10)
```

## Mocking

### Mock External Calls

```python
from unittest.mock import patch, MagicMock

@patch('src.data.make_dataset.torchvision.datasets.CIFAR10')
def test_load_cifar10(mock_cifar10):
    mock_cifar10.return_value = MagicMock()
    
    train_loader, _, _ = load_cifar10()
    mock_cifar10.assert_called_once()
```

## Performance Tests

### Test Execution Time

```python
import pytest
import time

@pytest.mark.performance
def test_training_speed():
    model = get_model("simple_cnn", num_classes=10, image_size=32)
    batch = torch.randn(32, 3, 32, 32)
    
    start = time.time()
    for _ in range(100):
        _ = model(batch)
    elapsed = time.time() - start
    
    # Should complete 100 batches in < 5 seconds
    assert elapsed < 5.0
```

### Skip Slow Tests

```bash
pytest -m "not performance"
```

## Continuous Integration

### GitHub Actions

Tests run on every push/PR:

```yaml
# .github/workflows/tests.yaml
- name: Run tests
  run: pytest --cov=src tests/
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Debugging Tests

### Use pytest Debugger

```bash
pytest --pdb
```

This drops into debugger on failure.

### Use Print Statements

```bash
pytest -s  # Show print output
```

### Verbose Output

```bash
pytest -vv  # Extra verbose
```

## Best Practices

1. **One assertion per test** (when possible)
   ```python
   # Good
   def test_model_output_shape():
       output = model(x)
       assert output.shape == (2, 10)
   
   # Bad
   def test_model():
       output = model(x)
       assert output.shape == (2, 10)
       assert output.dtype == torch.float32
   ```

2. **Use descriptive names**
   ```python
   # Good
   def test_simple_cnn_forward_pass_with_correct_input_shape()
   
   # Bad
   def test_model()
   ```

3. **Test edge cases**
   ```python
   def test_metrics_with_empty_predictions():
       predictions = np.array([])
       labels = np.array([])
       # Should handle gracefully
   ```

4. **Use fixtures for setup**
   ```python
   # Good
   @pytest.fixture
   def model():
       return SimpleCNN()
   
   # Bad
   def test_something():
       model = SimpleCNN()  # Setup in test
   ```

5. **Mock external dependencies**
   ```python
   # Good - Mock network call
   @patch('requests.get')
   def test_download(mock_get)
   
   # Bad - Actually calls network
   def test_download():
       response = requests.get(url)
   ```

## Test Examples

### Data Loading Test

```python
def test_load_cifar10(tmp_path):
    train_loader, val_loader, test_loader = load_cifar10(
        data_dir=str(tmp_path),
        batch_size=32
    )
    
    assert len(train_loader) > 0
    assert len(val_loader) > 0
    
    images, labels = next(iter(train_loader))
    assert images.shape == (32, 3, 32, 32)
    assert labels.shape == (32,)
```

### Model Test

```python
def test_simple_cnn_different_image_sizes():
    for image_size in [28, 32, 64]:
        model = SimpleCNN(num_classes=10, image_size=image_size)
        x = torch.randn(4, 3, image_size, image_size)
        y = model(x)
        assert y.shape == (4, 10)
```

### Training Test

```python
def test_training_improves_loss(train_loader, model):
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    
    initial_loss = None
    final_loss = None
    
    for epoch in range(2):
        loss, _ = train_epoch(
            model, train_loader, criterion, optimizer, device
        )
        if epoch == 0:
            initial_loss = loss
        else:
            final_loss = loss
    
    # Loss should decrease after training
    assert final_loss < initial_loss
```

Enjoy testing! 🧪
