# API Reference - Utils Module

Auto-generated API documentation for the utilities module.

## Metrics

### Calculate Metrics

::: src.utils.metrics.calculate_metrics

### Confusion Matrix

::: src.utils.metrics.plot_confusion_matrix

### Classification Report

::: src.utils.metrics.save_classification_report

### Training History Plot

::: src.utils.metrics.plot_training_history

## Utilities

### Average Meter

::: src.utils.metrics.AverageMeter

## Module Contents

```
src/utils/
├── __init__.py
├── metrics.py
│   ├── AverageMeter
│   ├── calculate_metrics()
│   ├── plot_confusion_matrix()
│   ├── save_classification_report()
│   └── plot_training_history()
└── ...
```

## Metrics Calculation

Supported metrics:
- **Accuracy**: Overall correctness
- **Precision**: True positives / (true positives + false positives)
- **Recall**: True positives / (true positives + false negatives)
- **F1 Score**: Harmonic mean of precision and recall

## Example Usage

```python
from src.utils.metrics import (
    AverageMeter, calculate_metrics,
    plot_confusion_matrix
)
import numpy as np

# Track average loss
loss_meter = AverageMeter()
for batch_loss in losses:
    loss_meter.update(batch_loss, batch_size)

print(f"Average loss: {loss_meter.avg:.4f}")

# Calculate metrics
predictions = np.array([...])  # Predicted labels
labels = np.array([...])  # True labels

metrics = calculate_metrics(predictions, labels)
print(f"Accuracy: {metrics['accuracy']:.4f}")
print(f"Precision: {metrics['precision']:.4f}")
print(f"Recall: {metrics['recall']:.4f}")
print(f"F1 Score: {metrics['f1_score']:.4f}")

# Generate visualizations
plot_confusion_matrix(
    predictions, labels,
    class_names=['class_0', 'class_1', ...],
    save_path="reports/confusion_matrix.png"
)
```

## AverageMeter Class

Track running average of a metric:

```python
meter = AverageMeter()
meter.update(value, n)  # n = batch size
print(meter.avg)  # Get average
```

## Visualization Functions

### Confusion Matrix

Heatmap showing prediction vs true labels.

### Classification Report

Text report with precision, recall, F1-score per class.

### Training History

Line plots of loss and accuracy over epochs.
