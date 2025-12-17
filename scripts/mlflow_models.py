"""
View and download MLflow models.

This script helps you interact with MLflow Model Registry.
"""

import argparse
from pathlib import Path

import mlflow
from mlflow.tracking import MlflowClient


def list_models():
    """List all registered models."""
    client = MlflowClient()

    try:
        models = client.search_registered_models()

        if not models:
            print("No registered models found.")
            return

        print("\n📦 Registered Models:")
        print("=" * 80)
        for model in models:
            print(f"\nName: {model.name}")
            print(f"Creation Time: {model.creation_timestamp}")
            print(f"Last Updated: {model.last_updated_timestamp}")

            # Get latest versions
            versions = client.get_latest_versions(model.name)
            for version in versions:
                print(f"\n  Version {version.version}:")
                print(f"    Stage: {version.current_stage}")
                print(f"    Status: {version.status}")
                print(f"    Run ID: {version.run_id}")

        print("\n" + "=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        print("Model Registry might not be enabled or no models registered yet.")


def load_model(model_name, version=None, stage=None):
    """Load a model from registry."""
    try:
        if stage:
            model_uri = f"models:/{model_name}/{stage}"
        elif version:
            model_uri = f"models:/{model_name}/{version}"
        else:
            model_uri = f"models:/{model_name}/latest"

        print(f"\n📥 Loading model from: {model_uri}")

        model = mlflow.pytorch.load_model(model_uri)

        print("✅ Model loaded successfully!")
        print(f"Model type: {type(model)}")

        return model

    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def download_artifacts(run_id, artifact_path=None, dst_path="./downloads"):
    """Download artifacts from a run."""
    client = MlflowClient()

    try:
        # Create destination directory
        dst_path = Path(dst_path)
        dst_path.mkdir(parents=True, exist_ok=True)

        # Download artifacts
        print(f"\n📥 Downloading artifacts from run: {run_id}")

        if artifact_path:
            local_path = client.download_artifacts(run_id, artifact_path, dst_path=str(dst_path))
        else:
            local_path = client.download_artifacts(run_id, "", dst_path=str(dst_path))

        print(f"✅ Artifacts downloaded to: {local_path}")

    except Exception as e:
        print(f"Error downloading artifacts: {e}")


def promote_model(model_name, version, stage):
    """Promote a model to a different stage."""
    client = MlflowClient()

    try:
        client.transition_model_version_stage(
            name=model_name, version=version, stage=stage, archive_existing_versions=True
        )

        print(
            f"✅ Model {model_name} version {version} promoted to {stage}"
        )

    except Exception as e:
        print(f"Error promoting model: {e}")


def main():
    parser = argparse.ArgumentParser(description="Manage MLflow models")
    parser.add_argument("--list", action="store_true", help="List all registered models")
    parser.add_argument("--model-name", type=str, help="Model name")
    parser.add_argument("--version", type=int, help="Model version")
    parser.add_argument("--stage", type=str, help="Model stage (Production, Staging, Archived)")
    parser.add_argument("--load", action="store_true", help="Load a model")
    parser.add_argument("--run-id", type=str, help="Run ID to download artifacts from")
    parser.add_argument("--download", action="store_true", help="Download artifacts")
    parser.add_argument("--artifact-path", type=str, help="Specific artifact path to download")
    parser.add_argument("--dst-path", type=str, default="./downloads", help="Destination path")
    parser.add_argument("--promote", action="store_true", help="Promote model to stage")

    args = parser.parse_args()

    # Set MLflow tracking URI
    mlflow.set_tracking_uri("./mlruns")

    if args.list:
        list_models()

    elif args.load and args.model_name:
        load_model(args.model_name, args.version, args.stage)

    elif args.download and args.run_id:
        download_artifacts(args.run_id, args.artifact_path, args.dst_path)

    elif args.promote and args.model_name and args.version and args.stage:
        promote_model(args.model_name, args.version, args.stage)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
