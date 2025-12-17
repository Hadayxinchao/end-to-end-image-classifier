#!/bin/bash
# Example training runs with experiment tracking

echo "🚀 Example Training Runs with Experiment Tracking"
echo "=================================================="
echo ""

# Example 1: Train with MLflow
echo "Example 1: Training with MLflow"
echo "--------------------------------"
echo "Command: python src/training/train.py tracking=mlflow"
echo ""
read -p "Run this example? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python src/training/train.py tracking=mlflow hyperparameters=fast
    echo ""
    echo "✅ Training complete! View results with: mlflow ui"
    echo ""
fi

# Example 2: Train with W&B
echo "Example 2: Training with Weights & Biases"
echo "------------------------------------------"
echo "Command: python src/training/train.py tracking=wandb"
echo ""
read -p "Run this example? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python src/training/train.py tracking=wandb hyperparameters=fast
    echo ""
    echo "✅ Training complete! Check W&B dashboard for results"
    echo ""
fi

# Example 3: Compare different models
echo "Example 3: Compare Different Models"
echo "------------------------------------"
echo "Training Simple CNN and ResNet with MLflow"
echo ""
read -p "Run this example? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Training Simple CNN..."
    python src/training/train.py model=simple_cnn tracking=mlflow hyperparameters=fast
    
    echo ""
    echo "Training ResNet..."
    python src/training/train.py model=resnet tracking=mlflow hyperparameters=fast
    
    echo ""
    echo "✅ Both models trained! Compare in MLflow UI"
    echo ""
fi

# Example 4: Hyperparameter tuning
echo "Example 4: Hyperparameter Tuning"
echo "---------------------------------"
echo "Trying different learning rates"
echo ""
read -p "Run this example? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    for lr in 0.001 0.005 0.01; do
        echo "Training with learning_rate=$lr..."
        python src/training/train.py \
            hyperparameters.learning_rate=$lr \
            tracking=mlflow \
            hyperparameters=fast
    done
    
    echo ""
    echo "✅ Hyperparameter tuning complete! Compare in MLflow UI"
    echo ""
fi

echo ""
echo "🎉 Examples complete!"
echo ""
echo "Next steps:"
echo "1. View MLflow results: mlflow ui"
echo "2. View W&B results: visit your W&B dashboard"
echo "3. Compare experiments: python scripts/compare_experiments.py"
