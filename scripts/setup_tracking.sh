#!/bin/bash
# Setup script for experiment tracking

echo "🚀 Setting up Experiment Tracking for Image Classifier"
echo "========================================================"

# Check if running in virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Warning: Not running in a virtual environment"
    echo "   Consider activating a venv first: source venv/bin/activate"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "📦 Installing dependencies..."
pip install mlflow wandb

echo ""
echo "✅ Dependencies installed!"
echo ""

# MLflow setup
echo "🔧 MLflow Setup"
echo "==============="
echo ""
echo "MLflow will track experiments locally in ./mlruns directory."
echo ""
read -p "Do you want to start MLflow UI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting MLflow UI on http://localhost:5000"
    echo "Press Ctrl+C to stop"
    mlflow ui &
    echo ""
fi

# W&B setup
echo ""
echo "🌐 Weights & Biases Setup"
echo "========================="
echo ""
echo "To use W&B, you need to:"
echo "1. Create an account at https://wandb.ai"
echo "2. Get your API key from https://wandb.ai/authorize"
echo "3. Login using 'wandb login'"
echo ""
read -p "Do you want to login to W&B now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    wandb login
else
    echo "You can login later with: wandb login"
fi

echo ""
echo "✨ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Configure tracking in configs/config.yaml"
echo "2. Update W&B project settings in configs/tracking/wandb.yaml"
echo "3. Run training: python src/training/train.py"
echo ""
echo "View results:"
echo "- MLflow UI: http://localhost:5000"
echo "- W&B Dashboard: https://wandb.ai/your-username/image-classifier"
echo ""
echo "For more information, see docs/mlops/experiment-tracking.md"
