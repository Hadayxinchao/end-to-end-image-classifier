"""Setup Weights & Biases for experiment tracking."""

import os
import wandb


def setup_wandb(project_name: str = "image-classifier", entity: str = None):
    """
    Setup Weights & Biases tracking.

    Args:
        project_name: W&B project name
        entity: W&B entity (username or team)
    """
    # Check if API key is set
    if not os.getenv("WANDB_API_KEY"):
        print("\n⚠️  WANDB_API_KEY not found in environment")
        print("Please run: wandb login")
        print("Or set environment variable: export WANDB_API_KEY=your_key")
        return False

    # Initialize wandb
    try:
        wandb.init(
            project=project_name,
            entity=entity,
            config={
                "framework": "pytorch",
                "project": "end-to-end-image-classifier",
            },
        )
        print(f"✅ W&B initialized: {project_name}")
        print(f"   Dashboard: {wandb.run.get_url()}")
        wandb.finish()
        return True
    except Exception as e:
        print(f"❌ Error initializing W&B: {e}")
        return False


def wandb_login():
    """Interactive W&B login."""
    try:
        wandb.login()
        print("✅ Successfully logged in to W&B")
        return True
    except Exception as e:
        print(f"❌ Error logging in: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup W&B tracking")
    parser.add_argument(
        "--project", type=str, default="image-classifier", help="Project name"
    )
    parser.add_argument("--entity", type=str, default=None, help="W&B entity")
    parser.add_argument("--login", action="store_true", help="Login to W&B")

    args = parser.parse_args()

    if args.login:
        wandb_login()
    else:
        setup_wandb(args.project, args.entity)
