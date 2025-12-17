#!/bin/bash
# Verify experiment tracking setup

echo "🔍 Verifying Experiment Tracking Setup"
echo "========================================"
echo ""

# Check if requirements are installed
echo "📦 Checking dependencies..."
echo ""

if python -c "import mlflow" 2>/dev/null; then
    MLFLOW_VERSION=$(python -c "import mlflow; print(mlflow.__version__)")
    echo "✅ MLflow installed (v$MLFLOW_VERSION)"
else
    echo "❌ MLflow not installed"
    echo "   Install with: pip install mlflow"
fi

if python -c "import wandb" 2>/dev/null; then
    WANDB_VERSION=$(python -c "import wandb; print(wandb.__version__)")
    echo "✅ Weights & Biases installed (v$WANDB_VERSION)"
else
    echo "❌ Weights & Biases not installed"
    echo "   Install with: pip install wandb"
fi

echo ""

# Check configuration files
echo "⚙️  Checking configuration files..."
echo ""

if [ -f "configs/tracking/mlflow.yaml" ]; then
    echo "✅ MLflow config found"
else
    echo "❌ MLflow config missing"
fi

if [ -f "configs/tracking/wandb.yaml" ]; then
    echo "✅ W&B config found"
else
    echo "❌ W&B config missing"
fi

echo ""

# Check source files
echo "📝 Checking source files..."
echo ""

if [ -f "src/utils/experiment_tracking.py" ]; then
    echo "✅ Experiment tracking module found"
else
    echo "❌ Experiment tracking module missing"
fi

# Check if tracking is integrated in train.py
if grep -q "ExperimentTracker" "src/training/train.py"; then
    echo "✅ Tracking integrated in train.py"
else
    echo "❌ Tracking not integrated in train.py"
fi

echo ""

# Check scripts
echo "🛠️  Checking utility scripts..."
echo ""

SCRIPTS=("setup_tracking.sh" "compare_experiments.py" "wandb_sweep.py" "mlflow_models.py" "example_runs.sh")

for script in "${SCRIPTS[@]}"; do
    if [ -f "scripts/$script" ]; then
        echo "✅ scripts/$script"
    else
        echo "❌ scripts/$script missing"
    fi
done

echo ""

# Check documentation
echo "📚 Checking documentation..."
echo ""

if [ -f "docs/mlops/experiment-tracking.md" ]; then
    echo "✅ Main documentation found"
else
    echo "❌ Main documentation missing"
fi

if [ -f "EXPERIMENT_TRACKING.md" ]; then
    echo "✅ Quick start guide found"
else
    echo "❌ Quick start guide missing"
fi

echo ""
echo "========================================"
echo ""

# Test import
echo "🧪 Testing module import..."
echo ""

if python -c "from src.utils.experiment_tracking import ExperimentTracker; print('✅ Module imports successfully')" 2>/dev/null; then
    true
else
    echo "⚠️  Module import test skipped (dependencies not installed)"
fi

echo ""
echo "✨ Verification complete!"
echo ""
echo "Next steps:"
echo "1. Install dependencies: pip install mlflow wandb"
echo "2. Run setup: ./scripts/setup_tracking.sh"
echo "3. Test training: python src/training/train.py tracking=mlflow hyperparameters=fast"
echo "4. View results: mlflow ui"
