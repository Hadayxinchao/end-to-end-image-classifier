# Experiments & Tracking

Track and manage machine learning experiments.

## Experiment Configuration

### Using Hydra Multi-run

Run multiple experiments with different configurations:

```bash
# Grid search over learning rates
python src/training/train.py -m \
    hyperparameters.learning_rate=0.0001,0.001,0.01

# Different models and datasets
python src/training/train.py -m \
    model=simple_cnn,resnet \
    data=cifar10,mnist
```

### Output Structure

Results are saved in `multirun/` with timestamps:

```
multirun/
├── 2025-12-10/
│   ├── 01-00-00/outputs/
│   ├── 02-00-00/outputs/
│   └── 03-00-00/outputs/
```

## Comparing Results

### Manual Comparison

Compare metrics from different runs:

```python
from pathlib import Path
import json

runs_dir = Path("multirun/2025-12-10")

for run_dir in sorted(runs_dir.iterdir()):
    config_file = run_dir / "outputs" / ".hydra" / "config.yaml"
    if config_file.exists():
        print(f"\nRun: {run_dir.name}")
        with open(config_file) as f:
            print(f.read())
```

## Experiment Logs

Training logs are saved in `outputs/` with timestamps:

```
outputs/
├── 2025-12-10/
│   ├── .hydra/
│   │   ├── config.yaml
│   │   ├── hydra.yaml
│   │   └── launcher.yaml
│   └── .hydra.log
```

## Model Checkpoints

Best models are saved during training:

```
models/
├── simple_cnn_best.pth
├── resnet_best.pth
└── ...
```

## Tracking with Version Control

### Commit Experiment

```bash
git add .
git commit -m "Exp: SimpleCNN on CIFAR-10, LR=0.001, 50% dropout"
```

### Tag Important Runs

```bash
git tag exp-001-baseline
git tag exp-002-with-augmentation
```

## Analysis & Visualization

### Plot Training History

```python
import matplotlib.pyplot as plt
from pathlib import Path

def plot_experiment(run_dir):
    history_file = run_dir / "reports" / "training_history.png"
    confusion_file = run_dir / "reports" / "confusion_matrix.png"

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Load and display images
    from PIL import Image
    axes[0].imshow(Image.open(history_file))
    axes[1].imshow(Image.open(confusion_file))

    plt.show()
```

### Compare Multiple Runs

```python
import pandas as pd
from pathlib import Path

def compare_runs(experiment_dir):
    results = []

    for run_dir in experiment_dir.iterdir():
        config = run_dir / ".hydra" / "config.yaml"
        metrics_file = run_dir / "reports" / "metrics.json"

        if config.exists() and metrics_file.exists():
            results.append({
                'run': run_dir.name,
                'config': config,
                'metrics': metrics_file
            })

    return pd.DataFrame(results)
```

## Best Practices

1. **Name experiments clearly**
   ```bash
   git commit -m "Exp: SimpleCNN with batch norm, LR=0.001"
   ```

2. **Track hyperparameters in config**
   - Use Hydra for consistent tracking
   - Save config.yaml with each run

3. **Save model and logs**
   - All runs save to timestamped directories
   - Easy to reproduce past experiments

4. **Document findings**
   - Keep experiment notes in README or wiki
   - Record best configurations

5. **Version control checkpoints**
   ```bash
   dvc add models/simple_cnn_best.pth
   git add models/simple_cnn_best.pth.dvc
   ```

## Integration with MLflow (Optional)

To add MLflow tracking:

```bash
pip install mlflow
```

Then modify `src/training/train.py`:

```python
import mlflow

with mlflow.start_run():
    mlflow.log_params(OmegaConf.to_container(cfg))
    # ... training code ...
    mlflow.log_metrics({'val_acc': val_acc})
    mlflow.pytorch.log_model(model, "models")
```

View results:

```bash
mlflow ui
```

Then open `http://localhost:5000`
