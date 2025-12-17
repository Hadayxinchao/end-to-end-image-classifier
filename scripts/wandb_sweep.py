"""
Hyperparameter sweep using Weights & Biases.

This script demonstrates how to run a hyperparameter sweep with W&B.
"""

import wandb
from omegaconf import OmegaConf

# Define sweep configuration
sweep_config = {
    "method": "bayes",  # Options: grid, random, bayes
    "metric": {"name": "val_acc", "goal": "maximize"},
    "parameters": {
        "learning_rate": {
            "distribution": "log_uniform_values",
            "min": 0.0001,
            "max": 0.1,
        },
        "batch_size": {"values": [32, 64, 128]},
        "optimizer": {"values": ["adam", "sgd"]},
        "dropout": {
            "distribution": "uniform",
            "min": 0.1,
            "max": 0.5,
        },
        "weight_decay": {
            "distribution": "log_uniform_values",
            "min": 0.00001,
            "max": 0.001,
        },
    },
}


def train_with_sweep():
    """Training function for sweep."""
    # Initialize W&B
    wandb.init()

    # Get sweep parameters
    config = wandb.config

    # Build command with sweep parameters
    cmd = f"""
    python src/training/train.py \
        tracking=wandb \
        hyperparameters.learning_rate={config.learning_rate} \
        hyperparameters.batch_size={config.batch_size} \
        hyperparameters.optimizer={config.optimizer} \
        hyperparameters.dropout={config.dropout} \
        hyperparameters.weight_decay={config.weight_decay}
    """

    print(f"Running: {cmd}")

    # Execute training
    import os

    os.system(cmd)


def main():
    """Main function to start sweep."""
    print("🔍 Starting Hyperparameter Sweep with W&B")
    print("=" * 80)

    # Initialize sweep
    sweep_id = wandb.sweep(sweep_config, project="image-classifier")

    print(f"\n✅ Sweep created: {sweep_id}")
    print(f"\nTo run sweep agent:")
    print(f"  wandb agent {sweep_id}")
    print(f"\nOr run multiple agents in parallel:")
    print(f"  wandb agent {sweep_id} --count 5")
    print()

    # Ask if user wants to start agent now
    response = input("Start sweep agent now? (y/n): ")
    if response.lower() == "y":
        wandb.agent(sweep_id, function=train_with_sweep, count=5)
    else:
        print("You can start the agent later with the command above.")


if __name__ == "__main__":
    main()
