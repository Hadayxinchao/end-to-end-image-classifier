# Configuration Management with Hydra

This project uses [Hydra](https://hydra.cc/) for configuration management, making it easy to run experiments without modifying code.

## Configuration Structure

```
configs/
├── config.yaml              # Main configuration
├── model/
│   ├── simple_cnn.yaml     # Simple CNN config
│   └── resnet.yaml         # ResNet config
├── data/
│   ├── cifar10.yaml        # CIFAR-10 dataset config
│   └── mnist.yaml          # MNIST dataset config
└── hyperparameters/
    ├── default.yaml        # Default hyperparameters
    └── fast.yaml           # Fast training config
```

## Basic Usage

### Override Single Parameter

```bash
python src/training/train.py hyperparameters.learning_rate=0.01
```

### Override Multiple Parameters

```bash
python src/training/train.py \
  hyperparameters.learning_rate=0.01 \
  hyperparameters.batch_size=128 \
  hyperparameters.num_epochs=20
```

### Use Different Config Group

```bash
# Use ResNet model
python src/training/train.py model=resnet

# Use MNIST dataset
python src/training/train.py data=mnist

# Use fast hyperparameters
python src/training/train.py hyperparameters=fast
```

### Combine Overrides

```bash
python src/training/train.py \
  model=resnet \
  data=mnist \
  hyperparameters=fast
```

## Configuration Files

### Main Config (`config.yaml`)

```yaml
defaults:
  - model: simple_cnn
  - data: cifar10
  - hyperparameters: default
  - _self_

seed: 42
device: auto
num_workers: 2

output_dir: ./outputs
model_save_dir: ./models
report_dir: ./reports

log_interval: 10
save_best_only: true
early_stopping_patience: 10

experiment_name: image_classifier
run_name: ${now:%Y-%m-%d_%H-%M-%S}
```

### Model Configs

**Simple CNN** (`model/simple_cnn.yaml`):
```yaml
name: simple_cnn
num_classes: 10
input_channels: 3
dropout: 0.5
```

**ResNet** (`model/resnet.yaml`):
```yaml
name: resnet
num_classes: 10
input_channels: 3
```

### Data Configs

**CIFAR-10** (`data/cifar10.yaml`):
```yaml
name: cifar10
data_dir: ./data/raw
batch_size: 64
val_split: 0.1
image_size: 32
num_classes: 10
input_channels: 3

mean: [0.5, 0.5, 0.5]
std: [0.5, 0.5, 0.5]

classes:
  - airplane
  - automobile
  - bird
  # ... etc
```

### Hyperparameter Configs

**Default** (`hyperparameters/default.yaml`):
```yaml
learning_rate: 0.001
weight_decay: 1e-4
momentum: 0.9
optimizer: adam

num_epochs: 50
batch_size: 64

use_scheduler: true
scheduler_type: step
step_size: 10
gamma: 0.1
min_lr: 1e-6

dropout: 0.5
label_smoothing: 0.0
clip_grad_norm: 1.0
```

## Advanced Usage

### Create Custom Experiment Config

Create `configs/experiment/my_exp.yaml`:

```yaml
# @package _global_

defaults:
  - override /model: resnet
  - override /data: cifar10
  - override /hyperparameters: default

# Override specific values
hyperparameters:
  learning_rate: 0.005
  num_epochs: 100
  batch_size: 128
  use_scheduler: true
  scheduler_type: cosine

seed: 1234
experiment_name: resnet_cifar10_cosine
```

Run it:

```bash
python src/training/train.py --config-name=experiment/my_exp
```

### Access Config in Code

```python
import hydra
from omegaconf import DictConfig

@hydra.main(version_base=None, config_path="../configs", config_name="config")
def main(cfg: DictConfig):
    print(cfg.hyperparameters.learning_rate)
    print(cfg.model.name)
    # Access nested configs easily
```

### Print Configuration

```bash
# Print full config
python src/training/train.py --cfg job

# Print specific group
python src/training/train.py --cfg job model
```

### Composition

Create different combinations:

```bash
# Experiment 1: Simple CNN on CIFAR-10
python src/training/train.py \
  model=simple_cnn \
  data=cifar10 \
  experiment_name=exp1_simple_cifar

# Experiment 2: ResNet on MNIST
python src/training/train.py \
  model=resnet \
  data=mnist \
  experiment_name=exp2_resnet_mnist
```

## Common Patterns

### Learning Rate Tuning

```bash
# Try different learning rates
python src/training/train.py hyperparameters.learning_rate=0.0001
python src/training/train.py hyperparameters.learning_rate=0.001
python src/training/train.py hyperparameters.learning_rate=0.01
```

### Batch Size Tuning

```bash
python src/training/train.py \
  hyperparameters.batch_size=32 \
  data.batch_size=32
```

### Scheduler Experiments

```bash
# Step scheduler
python src/training/train.py \
  hyperparameters.scheduler_type=step \
  hyperparameters.step_size=15

# Cosine annealing
python src/training/train.py \
  hyperparameters.scheduler_type=cosine

# No scheduler
python src/training/train.py \
  hyperparameters.use_scheduler=false
```

### Regularization Tuning

```bash
python src/training/train.py \
  hyperparameters.dropout=0.3 \
  hyperparameters.weight_decay=1e-5 \
  hyperparameters.label_smoothing=0.1
```

## Multi-Run

Run multiple experiments with different parameters:

```bash
python src/training/train.py -m \
  hyperparameters.learning_rate=0.001,0.01,0.1
```

This creates separate runs for each learning rate.

## Environment Variables

Use environment variables in configs:

```yaml
data_dir: ${oc.env:DATA_DIR,./data/raw}
```

Then:

```bash
export DATA_DIR=/path/to/data
python src/training/train.py
```

## Tips & Best Practices

1. **Never hardcode values** - Use configs for everything
2. **Create experiment configs** - Document your experiments
3. **Use meaningful names** - `experiment_name: resnet_lr001_bs128`
4. **Version configs with git** - Track what worked
5. **Use defaults** - Override only what you need

## Troubleshooting

### Config Not Found

Make sure you're in the project root:

```bash
cd /path/to/end-to-end-image-classifier
python src/training/train.py
```

### Override Not Working

Use correct syntax:

```bash
# ✅ Correct
python src/training/train.py hyperparameters.learning_rate=0.01

# ❌ Wrong
python src/training/train.py --learning_rate=0.01
```

### Nested Override

For nested values:

```bash
python src/training/train.py model.dropout=0.3
```

## Learn More

- [Hydra Documentation](https://hydra.cc/)
- [OmegaConf Documentation](https://omegaconf.readthedocs.io/)
- [Configuration Patterns](https://hydra.cc/docs/patterns/configuring_experiments/)
