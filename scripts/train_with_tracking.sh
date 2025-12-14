#!/bin/bash
# Training script with experiment tracking

set -e

echo "=================================="
echo "Training with Experiment Tracking"
echo "=================================="

# Check if MLflow is available
if command -v mlflow &> /dev/null; then
    echo "✅ MLflow is installed"
    
    # Set MLflow tracking URI if not set
    if [ -z "$MLFLOW_TRACKING_URI" ]; then
        export MLFLOW_TRACKING_URI="file://$(pwd)/mlruns"
        echo "📊 MLflow tracking URI: $MLFLOW_TRACKING_URI"
    fi
    
    # Start MLflow UI in background (optional)
    if [ "$START_MLFLOW_UI" = "true" ]; then
        echo "🚀 Starting MLflow UI on port 5000..."
        mlflow ui --port 5000 &
        MLFLOW_PID=$!
        echo "   MLflow UI PID: $MLFLOW_PID"
        echo "   Access at: http://localhost:5000"
    fi
else
    echo "⚠️  MLflow not installed. Install with: pip install mlflow"
fi

# Check if W&B is available
if command -v wandb &> /dev/null; then
    echo "✅ W&B is installed"
    
    if [ -z "$WANDB_API_KEY" ]; then
        echo "⚠️  WANDB_API_KEY not set. Run: wandb login"
    else
        echo "📊 W&B tracking enabled"
    fi
else
    echo "⚠️  W&B not installed. Install with: pip install wandb"
fi

echo ""
echo "🎯 Starting training..."
echo ""

# Run training with all arguments passed to this script
python src/training/train.py "$@"

EXIT_CODE=$?

# Cleanup
if [ ! -z "$MLFLOW_PID" ]; then
    echo ""
    echo "🛑 Stopping MLflow UI..."
    kill $MLFLOW_PID 2>/dev/null || true
fi

echo ""
echo "=================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Training completed successfully!"
else
    echo "❌ Training failed with exit code: $EXIT_CODE"
fi
echo "=================================="

exit $EXIT_CODE
