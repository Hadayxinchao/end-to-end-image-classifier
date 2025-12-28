#!/bin/bash
# Setup and configure Weights & Biases

set -e

echo "🔧 Setting up Weights & Biases (W&B)..."

# Check if wandb is installed
if ! python -c "import wandb" 2>/dev/null; then
    echo "Installing wandb..."
    pip install wandb
fi

echo ""
echo "📊 W&B Installation verified!"

# Login to W&B
echo ""
echo "🔐 W&B Login"
echo "If you haven't logged in yet, you'll be prompted for your API key"
echo "Get your API key from: https://wandb.ai/authorize"
echo ""

wandb login || echo "⚠️  W&B login skipped or failed. You can login later with: wandb login"

# Initialize a test project
echo ""
echo "🧪 Testing W&B integration..."

cat > /tmp/test_wandb.py << 'EOF'
import wandb
import torch
import torch.nn as nn

# Initialize wandb
run = wandb.init(
    project="image-classifier-test",
    name="setup-test",
    config={
        "learning_rate": 0.001,
        "epochs": 1,
        "batch_size": 32
    }
)

# Create a simple model
model = nn.Sequential(
    nn.Linear(10, 5),
    nn.ReLU(),
    nn.Linear(5, 2)
)

# Watch model
wandb.watch(model, log="all", log_freq=10)

# Log some metrics
for i in range(10):
    wandb.log({
        "loss": 1.0 / (i + 1),
        "accuracy": i * 10,
        "step": i
    })

# Log model weights histogram
for name, param in model.named_parameters():
    wandb.log({f"weights/{name}": wandb.Histogram(param.data.cpu().numpy())})

print("✅ W&B test successful!")
wandb.finish()
EOF

python /tmp/test_wandb.py

echo ""
echo "✅ W&B setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Set your W&B API key (if not done): export WANDB_API_KEY=your-key"
echo "  2. Run training with W&B: python src/training/train.py tracking=wandb"
echo "  3. View results at: https://wandb.ai"
echo ""
echo "📖 Configuration file: configs/tracking/wandb.yaml"
