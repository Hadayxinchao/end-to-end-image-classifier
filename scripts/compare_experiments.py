"""
Compare experiments across different runs.

This script helps you compare metrics and parameters across multiple MLflow runs.
"""

import argparse
from pathlib import Path

import mlflow
import pandas as pd


def list_experiments():
    """List all available experiments."""
    client = mlflow.tracking.MlflowClient()
    experiments = client.search_experiments()

    print("\nAvailable Experiments:")
    print("=" * 80)
    for exp in experiments:
        print(f"ID: {exp.experiment_id}")
        print(f"Name: {exp.name}")
        print(f"Location: {exp.artifact_location}")
        print("-" * 80)


def compare_runs(experiment_name=None, metric="val_acc", top_n=10):
    """Compare runs within an experiment."""
    # Set tracking URI
    mlflow.set_tracking_uri("./mlruns")

    # Get experiment
    if experiment_name:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if not experiment:
            print(f"Experiment '{experiment_name}' not found!")
            return
        experiment_id = experiment.experiment_id
    else:
        # Use default experiment
        experiment_id = "0"

    # Search runs
    runs = mlflow.search_runs(
        experiment_ids=[experiment_id], order_by=[f"metrics.{metric} DESC"], max_results=top_n
    )

    if runs.empty:
        print("No runs found!")
        return

    # Select important columns
    columns = ["run_id", "start_time", "status"]

    # Add metric columns
    metric_cols = [col for col in runs.columns if col.startswith("metrics.")]
    columns.extend(metric_cols)

    # Add parameter columns
    param_cols = [col for col in runs.columns if col.startswith("params.")]
    columns.extend(param_cols[:10])  # Limit to first 10 params

    # Filter and sort
    comparison_df = runs[columns].copy()
    comparison_df.columns = [col.replace("metrics.", "").replace("params.", "") for col in columns]

    print(f"\n🏆 Top {len(comparison_df)} Runs by {metric}")
    print("=" * 120)
    print(comparison_df.to_string())

    # Print best run details
    best_run = runs.iloc[0]
    print(f"\n✨ Best Run Details:")
    print(f"Run ID: {best_run['run_id']}")
    print(f"Start Time: {best_run['start_time']}")

    print("\nMetrics:")
    for col in metric_cols:
        metric_name = col.replace("metrics.", "")
        print(f"  {metric_name}: {best_run[col]:.4f}")

    print("\nParameters:")
    for col in param_cols[:10]:
        param_name = col.replace("params.", "")
        print(f"  {param_name}: {best_run[col]}")


def export_comparison(experiment_name, output_file="comparison.csv"):
    """Export run comparison to CSV."""
    mlflow.set_tracking_uri("./mlruns")

    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        print(f"Experiment '{experiment_name}' not found!")
        return

    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

    # Export to CSV
    output_path = Path(output_file)
    runs.to_csv(output_path, index=False)
    print(f"✅ Comparison exported to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Compare MLflow experiment runs")
    parser.add_argument("--list", action="store_true", help="List all experiments")
    parser.add_argument("--experiment", type=str, help="Experiment name to compare")
    parser.add_argument("--metric", type=str, default="val_acc", help="Metric to sort by")
    parser.add_argument("--top-n", type=int, default=10, help="Number of top runs to show")
    parser.add_argument("--export", type=str, help="Export comparison to CSV file")

    args = parser.parse_args()

    if args.list:
        list_experiments()
    elif args.export:
        export_comparison(args.experiment, args.export)
    else:
        compare_runs(args.experiment, args.metric, args.top_n)


if __name__ == "__main__":
    main()
