"""Quick start script for training with experiment tracking."""

import os
import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """Check if optional dependencies are available."""
    deps = {"mlflow": False, "wandb": False}

    try:
        import mlflow

        deps["mlflow"] = True
    except ImportError:
        pass

    try:
        import wandb

        deps["wandb"] = True
    except ImportError:
        pass

    return deps


def setup_environment():
    """Setup environment variables for tracking."""
    # Setup MLflow
    if "MLFLOW_TRACKING_URI" not in os.environ:
        mlruns_dir = Path.cwd() / "mlruns"
        mlruns_dir.mkdir(exist_ok=True)
        os.environ["MLFLOW_TRACKING_URI"] = f"file://{mlruns_dir}"
        print(f"📊 MLflow tracking URI: {os.environ['MLFLOW_TRACKING_URI']}")

    # Check W&B
    if "WANDB_API_KEY" not in os.environ:
        print("⚠️  WANDB_API_KEY not set. W&B tracking will be disabled.")
        print("   To enable: wandb login")


def main():
    """Main function."""
    print("=" * 80)
    print("Training with Experiment Tracking")
    print("=" * 80 + "\n")

    # Check dependencies
    deps = check_dependencies()
    print("Dependencies:")
    print(f"  MLflow: {'✅ Available' if deps['mlflow'] else '❌ Not installed'}")
    print(f"  W&B:    {'✅ Available' if deps['wandb'] else '❌ Not installed'}")

    if not any(deps.values()):
        print("\n⚠️  No tracking tools available. Install with:")
        print("  pip install mlflow wandb")
        print("\nContinuing without experiment tracking...\n")

    # Setup environment
    setup_environment()

    # Build training command
    train_cmd = [sys.executable, "src/training/train.py"] + sys.argv[1:]

    print(f"\n🎯 Running: {' '.join(train_cmd)}\n")
    print("=" * 80 + "\n")

    # Run training
    try:
        result = subprocess.run(train_cmd, check=True)
        print("\n" + "=" * 80)
        print("✅ Training completed successfully!")
        print("=" * 80)

        # Print instructions
        if deps["mlflow"]:
            print("\n📊 View MLflow results:")
            print("  mlflow ui --port 5000")
            print("  Then open: http://localhost:5000")

        if deps["wandb"]:
            print("\n📊 View W&B results:")
            print("  https://wandb.ai/")

        return 0
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 80)
        print(f"❌ Training failed with exit code: {e.returncode}")
        print("=" * 80)
        return e.returncode
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        return 130


if __name__ == "__main__":
    sys.exit(main())
