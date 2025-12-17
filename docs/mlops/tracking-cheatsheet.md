# MLflow and Weights & Biases Cheat Sheet

## MLflow Commands

### Start MLflow UI
```bash
mlflow ui
mlflow ui --port 5000
mlflow ui --host 0.0.0.0  # Make accessible from network
```

### Remote Tracking Server
```bash
# Start server
mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db

# Connect from client
export MLFLOW_TRACKING_URI=http://localhost:5000
```

### CLI Commands
```bash
# List experiments
mlflow experiments list

# Search runs
mlflow runs list --experiment-id 0

# Delete experiment
mlflow experiments delete --experiment-id 1

# Restore experiment
mlflow experiments restore --experiment-id 1
```

## Weights & Biases Commands

### Login
```bash
wandb login
wandb login --relogin
wandb login --host=http://your-server.com  # Self-hosted
```

### Offline Mode
```bash
# Set offline mode
export WANDB_MODE=offline

# Or in Python
wandb.init(mode="offline")

# Sync later
wandb sync ./wandb/offline-run-*
wandb sync --sync-all
```

### Project Management
```bash
# List runs
wandb runs list your-project

# Pull run data
wandb pull your-run-id

# Restore run
wandb restore your-run-id
```

### Sweeps
```bash
# Create sweep
wandb sweep sweep_config.yaml

# Run agent
wandb agent your-sweep-id

# Run multiple agents
wandb agent your-sweep-id --count 10
```

## Python API Examples

### MLflow

```python
import mlflow

# Set tracking URI
mlflow.set_tracking_uri("./mlruns")

# Create experiment
mlflow.create_experiment("my_experiment")

# Start run
with mlflow.start_run():
    # Log params
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_params({"batch_size": 32, "epochs": 10})
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05, step=1)
    
    # Log model
    mlflow.pytorch.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("plot.png")
    mlflow.log_artifacts("./reports")

# Load model
model = mlflow.pytorch.load_model("runs:/run-id/model")
model = mlflow.pytorch.load_model("models:/model-name/production")
```

### Weights & Biases

```python
import wandb

# Initialize run
wandb.init(
    project="my-project",
    name="my-run",
    config={"learning_rate": 0.01, "batch_size": 32}
)

# Log metrics
wandb.log({"accuracy": 0.95, "loss": 0.05})
wandb.log({"accuracy": 0.96, "loss": 0.04}, step=1)

# Log images
wandb.log({"predictions": wandb.Image(image_array)})

# Log plots
wandb.log({"confusion_matrix": wandb.plot.confusion_matrix(
    y_true=y_true, 
    preds=preds,
    class_names=class_names
)})

# Watch model
wandb.watch(model, log="all", log_freq=100)

# Save files
wandb.save("model.pth")
wandb.save("./reports/*")

# Finish run
wandb.finish()
```

## Configuration Examples

### Train with Different Backends
```bash
# MLflow
python src/training/train.py tracking=mlflow

# Weights & Biases
python src/training/train.py tracking=wandb

# Both
python src/training/train.py tracking=both

# None
python src/training/train.py tracking=null
```

### Override Tracking Settings
```bash
# MLflow with custom experiment
python src/training/train.py \
    tracking=mlflow \
    tracking.experiment_name=my_experiment \
    tracking.run_name=my_run

# W&B with custom project
python src/training/train.py \
    tracking=wandb \
    tracking.project=my-project \
    tracking.entity=my-team
```

## Comparison

| Feature | MLflow | Weights & Biases |
|---------|--------|------------------|
| **Setup** | Easy (local) | Requires account |
| **UI** | Basic, functional | Beautiful, interactive |
| **Hosting** | Self-hosted by default | Cloud by default |
| **Storage** | Local files | Cloud storage |
| **Collaboration** | Limited | Excellent |
| **Model Registry** | Yes | Yes |
| **Sweeps** | Basic | Advanced |
| **System Monitoring** | Basic | Excellent |
| **Free Tier** | Unlimited | 100GB, unlimited runs |
| **Cost** | Free (self-hosted) | Free tier + paid plans |

## Best Practices

### MLflow
1. Use consistent experiment names
2. Tag runs with meaningful metadata
3. Use Model Registry for production models
4. Backup mlruns directory regularly
5. Use remote tracking server for teams

### Weights & Biases
1. Use groups to organize related runs
2. Add tags for easy filtering
3. Write detailed run notes
4. Use sweeps for hyperparameter tuning
5. Create reports for sharing results

## Troubleshooting

### MLflow

**Cannot connect to tracking server**
```bash
# Check if server is running
ps aux | grep mlflow

# Check firewall
sudo ufw status

# Test connection
curl http://localhost:5000
```

**Database locked error**
```bash
# Stop all MLflow processes
pkill -f mlflow

# If using SQLite, check file permissions
ls -la mlflow.db
```

### Weights & Biases

**Login issues**
```bash
# Check API key
cat ~/.netrc | grep wandb

# Reset login
rm ~/.netrc
wandb login
```

**Sync issues**
```bash
# Check sync status
wandb sync --show

# Force sync
wandb sync --sync-all --include-offline
```

## Resources

### MLflow
- Docs: https://mlflow.org/docs/latest/
- GitHub: https://github.com/mlflow/mlflow
- Tracking: https://mlflow.org/docs/latest/tracking.html
- Models: https://mlflow.org/docs/latest/models.html

### Weights & Biases
- Docs: https://docs.wandb.ai/
- GitHub: https://github.com/wandb/wandb
- Quickstart: https://docs.wandb.ai/quickstart
- Sweeps: https://docs.wandb.ai/guides/sweeps
