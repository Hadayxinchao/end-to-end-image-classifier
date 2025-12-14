"""Setup MLflow tracking for experiments."""

import mlflow
from pathlib import Path


def setup_mlflow(experiment_name: str = "image-classifier", tracking_uri: str = None):
    """
    Setup MLflow tracking.

    Args:
        experiment_name: Name of the experiment
        tracking_uri: MLflow tracking URI (default: local file store)
    """
    # Set tracking URI
    if tracking_uri is None:
        tracking_uri = f"file://{Path.cwd() / 'mlruns'}"

    mlflow.set_tracking_uri(tracking_uri)
    print(f"MLflow tracking URI: {mlflow.get_tracking_uri()}")

    # Create or get experiment
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(
            experiment_name,
            tags={
                "project": "end-to-end-image-classifier",
                "framework": "pytorch",
            },
        )
        print(f"✅ Created new experiment: {experiment_name} (ID: {experiment_id})")
    else:
        experiment_id = experiment.experiment_id
        print(f"✅ Using existing experiment: {experiment_name} (ID: {experiment_id})")

    mlflow.set_experiment(experiment_name)

    return experiment_id


def start_mlflow_server(port: int = 5000):
    """
    Instructions to start MLflow UI server.

    Args:
        port: Port for MLflow UI
    """
    print("\n" + "=" * 80)
    print("To view MLflow UI, run:")
    print(f"  mlflow ui --port {port}")
    print(f"  Then open: http://localhost:{port}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup MLflow tracking")
    parser.add_argument(
        "--experiment-name",
        type=str,
        default="image-classifier",
        help="Experiment name",
    )
    parser.add_argument(
        "--tracking-uri", type=str, default=None, help="MLflow tracking URI"
    )

    args = parser.parse_args()

    setup_mlflow(args.experiment_name, args.tracking_uri)
    start_mlflow_server()
