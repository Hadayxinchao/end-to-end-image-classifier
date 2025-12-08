# Data Versioning with DVC

Learn how to use Data Version Control (DVC) to track datasets, models, and experiments.

## Why DVC?

- **Version large files** - Git can't handle large datasets efficiently
- **Share data** - Use remote storage (S3, Google Drive, etc.)
- **Reproduce experiments** - Track exact data versions
- **Save storage** - Don't duplicate data across branches

## Installation

DVC is already included in `requirements.txt`. If not installed:

```bash
pip install dvc dvc-gdrive  # Or dvc-s3, dvc-azure, etc.
```

## Quick Start

### 1. Initialize DVC

```bash
dvc init
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

### 2. Track Data

```bash
# Track the data directory
dvc add data/raw

# This creates data/raw.dvc
git add data/raw.dvc data/.gitignore
git commit -m "Track data with DVC"
```

### 3. Setup Remote Storage

Choose a remote storage backend:

=== "Google Drive"
    ```bash
    dvc remote add -d storage gdrive://FOLDER_ID
    git add .dvc/config
    git commit -m "Configure remote storage"
    ```

=== "AWS S3"
    ```bash
    dvc remote add -d storage s3://mybucket/path
    dvc remote modify storage region us-west-2
    ```

=== "Local Storage"
    ```bash
    dvc remote add -d storage /tmp/dvc-storage
    # Or network drive
    dvc remote add -d storage /mnt/shared/dvc-storage
    ```

### 4. Push Data

```bash
dvc push
```

## Common Workflows

### Clone Repository and Get Data

```bash
# Clone repo
git clone https://github.com/username/repo.git
cd repo

# Install dependencies
pip install -r requirements.txt

# Pull data
dvc pull
```

### Update Dataset

```bash
# 1. Modify your data
cp new_data/* data/raw/

# 2. Update DVC tracking
dvc add data/raw

# 3. Commit changes
git add data/raw.dvc
git commit -m "Update dataset with new images"

# 4. Push to remote
dvc push
git push
```

### Switch Between Versions

```bash
# Go to a specific commit
git checkout <commit-hash>

# Pull the corresponding data
dvc pull
```

### Check Status

```bash
# Check what's changed
dvc status

# Check DVC cache
dvc cache dir
```

## Track Models

### Track Trained Models

```bash
# Add models directory
dvc add models/

git add models.dvc
git commit -m "Track trained models"
dvc push
```

### Version Models with Experiments

Create a pipeline:

```yaml
# dvc.yaml
stages:
  train:
    cmd: python src/training/train.py
    deps:
      - src/training/train.py
      - data/raw
    params:
      - config.yaml:hyperparameters.learning_rate
      - config.yaml:hyperparameters.num_epochs
    outs:
      - models/simple_cnn_best.pth
    metrics:
      - reports/classification_report.txt:
          cache: false
```

Run pipeline:

```bash
dvc repro
```

## Remote Storage Options

### Google Drive

1. Create a folder in Google Drive
2. Get the folder ID from the URL
3. Configure DVC:

```bash
dvc remote add -d storage gdrive://FOLDER_ID
```

First push will open browser for authentication.

### AWS S3

```bash
# Add remote
dvc remote add -d storage s3://mybucket/path

# Configure credentials
dvc remote modify storage access_key_id YOUR_KEY
dvc remote modify storage secret_access_key YOUR_SECRET

# Or use AWS CLI credentials
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
```

### Azure Blob Storage

```bash
dvc remote add -d storage azure://container/path
dvc remote modify storage account_name myaccount
```

### SSH/Local

```bash
# SSH
dvc remote add -d storage ssh://user@server:/path/to/storage

# Local or network drive
dvc remote add -d storage /mnt/shared/dvc-storage
```

## DVC with GitHub Actions

### Setup

Add secrets to GitHub:

1. Go to Settings → Secrets
2. Add necessary credentials (AWS keys, etc.)

### Workflow Example

```yaml
name: DVC Pipeline

on: [push]

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Pull data
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          dvc pull
      
      - name: Train model
        run: |
          dvc repro
      
      - name: Push results
        run: |
          dvc push
```

## Best Practices

### 1. Organize Data

```
data/
├── raw/           # Original immutable data - track with DVC
├── processed/     # Processed data - track with DVC
└── interim/       # Temporary data - don't track
```

### 2. Use .dvcignore

Exclude files you don't want to track:

```
# .dvcignore
*.log
*.tmp
__pycache__/
.ipynb_checkpoints/
```

### 3. Track Different Versions

```bash
# Tag important versions
git tag -a v1.0 -m "Dataset version 1.0"
git push --tags
dvc push
```

### 4. Share Specific Versions

```bash
# Create branch for experiment
git checkout -b experiment/new_data
dvc add data/raw
git add data/raw.dvc
git commit -m "Add new dataset"
dvc push
git push -u origin experiment/new_data
```

## Advanced Features

### DVC Pipelines

Define reproducible workflows:

```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: python src/data/preprocess.py
    deps:
      - data/raw
    outs:
      - data/processed
  
  train:
    cmd: python src/training/train.py
    deps:
      - data/processed
      - src/training/train.py
    params:
      - configs/config.yaml:hyperparameters
    outs:
      - models/model.pth
    metrics:
      - reports/metrics.json:
          cache: false
```

Run entire pipeline:

```bash
dvc repro
```

### Experiments

Track experiments:

```bash
# Run experiment
dvc exp run

# Compare experiments
dvc exp show

# Apply best experiment
dvc exp apply <exp-name>
```

### Metrics Tracking

```yaml
# dvc.yaml
stages:
  train:
    metrics:
      - reports/metrics.json:
          cache: false
    plots:
      - reports/confusion_matrix.png:
          cache: false
```

Compare metrics:

```bash
dvc metrics show
dvc metrics diff
```

## Troubleshooting

### Large Files Not Tracked

Check `.gitignore`:

```bash
cat data/.gitignore
# Should contain /raw (added by dvc add)
```

### Permission Denied

For remote storage, check credentials:

```bash
dvc remote list
dvc remote modify storage --local access_key_id YOUR_KEY
```

### Cache Issues

Clear and rebuild cache:

```bash
dvc cache dir  # Show cache location
rm -rf .dvc/cache
dvc pull
```

### Slow Push/Pull

Use parallel transfers:

```bash
dvc config cache.type symlink
dvc push --jobs 4
```

## DVC vs Git LFS

| Feature | DVC | Git LFS |
|---------|-----|---------|
| Storage backends | Many (S3, Azure, GDrive, SSH, etc.) | Git LFS server |
| Versioning | Full versioning | Full versioning |
| Pipeline support | Yes | No |
| Metrics tracking | Yes | No |
| Free tier | Depends on storage | GitHub: 1GB |

## Learn More

- [DVC Documentation](https://dvc.org/doc)
- [DVC Tutorial](https://dvc.org/doc/start)
- [DVC with CI/CD](https://dvc.org/doc/use-cases/ci-cd-for-machine-learning)
- [Example Projects](https://github.com/iterative/example-get-started)

## Summary

```bash
# Essential commands
dvc init              # Initialize DVC
dvc add data/         # Track data
dvc push              # Upload to remote
dvc pull              # Download from remote
dvc status            # Check status
dvc repro             # Run pipeline
```
