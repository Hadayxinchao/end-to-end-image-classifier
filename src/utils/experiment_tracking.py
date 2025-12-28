"""Experiment tracking with MLflow and Weights & Biases."""

from pathlib import Path
from typing import Any, Dict, Optional, Union

import matplotlib.pyplot as plt
import torch.nn as nn
from omegaconf import DictConfig, OmegaConf


class ExperimentTracker:
    """Unified interface for experiment tracking with MLflow and Weights & Biases."""

    def __init__(self, cfg: DictConfig, tracking_backend: str = "mlflow"):
        """
        Initialize experiment tracker.

        Args:
            cfg: Configuration object
            tracking_backend: Which backend to use - "mlflow", "wandb", or "both"
        """
        self.cfg = cfg
        self.tracking_backend = tracking_backend.lower()
        self.mlflow_run = None
        self.wandb_run = None

        # Initialize backends
        if self.tracking_backend in ["mlflow", "both"]:
            self._init_mlflow()

        if self.tracking_backend in ["wandb", "both"]:
            self._init_wandb()

    def _init_mlflow(self):
        """Initialize MLflow tracking."""
        try:
            import mlflow

            self.mlflow = mlflow

            if (
                not hasattr(self.cfg, "tracking")
                or not hasattr(self.cfg.tracking, "enabled")
                or not self.cfg.tracking.enabled
            ):
                print("MLflow tracking is disabled in config")
                return

            # Set tracking URI
            tracking_uri = self.cfg.tracking.get("tracking_uri", "./mlruns")
            self.mlflow.set_tracking_uri(tracking_uri)

            # Set experiment
            experiment_name = self.cfg.tracking.get("experiment_name", self.cfg.experiment_name)
            self.mlflow.set_experiment(experiment_name)

            # Start run
            run_name = self.cfg.tracking.get("run_name", self.cfg.run_name)
            self.mlflow_run = self.mlflow.start_run(run_name=run_name)

            print("✓ MLflow tracking initialized")
            print(f"  Tracking URI: {tracking_uri}")
            print(f"  Experiment: {experiment_name}")
            print(f"  Run ID: {self.mlflow_run.info.run_id}")

            # Enable autologging if configured
            if self.cfg.tracking.get("autolog", False):
                self.mlflow.pytorch.autolog(**self.cfg.tracking.get("autolog_params", {}))
                print("  ✓ MLflow autologging enabled")

        except ImportError:
            print("Warning: MLflow not installed. Install with: pip install mlflow")
            self.tracking_backend = (
                self.tracking_backend.replace("mlflow", "").replace("both", "wandb").strip()
            )
        except Exception as e:
            print(f"Warning: Could not initialize MLflow: {e}")

    def _init_wandb(self):
        """Initialize Weights & Biases tracking."""
        try:
            import wandb

            self.wandb = wandb

            if (
                not hasattr(self.cfg, "tracking")
                or not hasattr(self.cfg.tracking, "enabled")
                or not self.cfg.tracking.enabled
            ):
                print("W&B tracking is disabled in config")
                return

            # Prepare config
            wandb_config = OmegaConf.to_container(self.cfg, resolve=True)

            # Initialize run
            self.wandb_run = self.wandb.init(
                project=self.cfg.tracking.get("project", "image-classifier"),
                entity=self.cfg.tracking.get("entity", None),
                name=self.cfg.tracking.get("name", self.cfg.run_name),
                group=self.cfg.tracking.get("group", None),
                job_type=self.cfg.tracking.get("job_type", "train"),
                tags=self.cfg.tracking.get("tags", []),
                config=wandb_config,
                mode=self.cfg.tracking.get("mode", "online"),
                save_code=self.cfg.tracking.get("save_code", True),
                notes=self.cfg.tracking.get("notes", None),
                resume=self.cfg.tracking.get("resume", False),
                id=self.cfg.tracking.get("resume_id", None),
            )

            print("✓ W&B tracking initialized")
            print(f"  Project: {self.cfg.tracking.get('project', 'image-classifier')}")
            print(f"  Run: {self.wandb_run.name}")
            print(f"  URL: {self.wandb_run.get_url()}")

            # Watch model if configured
            if self.cfg.tracking.get("watch_model", False):
                print("  Note: Model watching will be enabled after model creation")

        except ImportError:
            print("Warning: W&B not installed. Install with: pip install wandb")
            self.tracking_backend = (
                self.tracking_backend.replace("wandb", "").replace("both", "mlflow").strip()
            )
        except Exception as e:
            print(f"Warning: Could not initialize W&B: {e}")

    def log_params(self, params: Dict[str, Any]):
        """Log parameters."""
        if self.mlflow_run and self.cfg.tracking.get("log_params", True):
            try:
                # Flatten nested dict
                flat_params = self._flatten_dict(params)
                self.mlflow.log_params(flat_params)
            except Exception as e:
                print(f"Warning: Could not log params to MLflow: {e}")

        # W&B logs params during init, but we can update them
        if self.wandb_run and self.cfg.tracking.get("log_params", True):
            try:
                self.wandb.config.update(params, allow_val_change=True)
            except Exception as e:
                print(f"Warning: Could not log params to W&B: {e}")

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics."""
        if self.mlflow_run and self.cfg.tracking.get("log_metrics", True):
            try:
                for key, value in metrics.items():
                    self.mlflow.log_metric(key, value, step=step)
            except Exception as e:
                print(f"Warning: Could not log metrics to MLflow: {e}")

        if self.wandb_run and self.cfg.tracking.get("log_metrics", True):
            try:
                log_dict = metrics.copy()
                if step is not None:
                    log_dict["epoch"] = step
                self.wandb.log(log_dict, step=step)
            except Exception as e:
                print(f"Warning: Could not log metrics to W&B: {e}")

    def log_artifact(self, local_path: Union[str, Path], artifact_path: Optional[str] = None):
        """Log an artifact (file)."""
        local_path = Path(local_path)

        if self.mlflow_run and self.cfg.tracking.get("log_artifacts", True):
            try:
                if local_path.is_file():
                    self.mlflow.log_artifact(str(local_path), artifact_path=artifact_path)
                elif local_path.is_dir():
                    self.mlflow.log_artifacts(str(local_path), artifact_path=artifact_path)
            except Exception as e:
                print(f"Warning: Could not log artifact to MLflow: {e}")

        if self.wandb_run and self.cfg.tracking.get("log_artifacts", True):
            try:
                if local_path.is_file():
                    self.wandb.save(str(local_path))
            except Exception as e:
                print(f"Warning: Could not log artifact to W&B: {e}")

    def log_model(
        self,
        model: nn.Module,
        model_path: Optional[Union[str, Path]] = None,
        artifact_path: str = "model",
    ):
        """Log a trained model."""
        if self.mlflow_run and self.cfg.tracking.get("log_models", True):
            try:
                # Log model to MLflow
                self.mlflow.pytorch.log_model(
                    model,
                    artifact_path=artifact_path,
                    registered_model_name=(
                        self.cfg.tracking.get("registered_model_name", None)
                        if self.cfg.tracking.get("register_model", False)
                        else None
                    ),
                )
            except Exception as e:
                print(f"Warning: Could not log model to MLflow: {e}")

        if self.wandb_run and self.cfg.tracking.get("log_model", True):
            try:
                if model_path:
                    # Log model file
                    self.wandb.save(str(model_path))
            except Exception as e:
                print(f"Warning: Could not log model to W&B: {e}")

    def log_figure(
        self, figure: plt.Figure, name: str, step: Optional[int] = None, close: bool = True
    ):
        """Log a matplotlib figure."""
        if self.mlflow_run:
            try:
                self.mlflow.log_figure(figure, f"{name}.png")
            except Exception as e:
                print(f"Warning: Could not log figure to MLflow: {e}")

        if self.wandb_run:
            try:
                self.wandb.log({name: self.wandb.Image(figure)}, step=step)
            except Exception as e:
                print(f"Warning: Could not log figure to W&B: {e}")

        if close:
            plt.close(figure)

    def watch_model(self, model: nn.Module):
        """Watch model gradients and parameters (W&B only)."""
        if self.wandb_run and self.cfg.tracking.get("watch_model", False):
            try:
                self.wandb.watch(
                    model,
                    log=self.cfg.tracking.get("watch_log", "gradients"),
                    log_freq=self.cfg.tracking.get("watch_freq", 100),
                    log_graph=self.cfg.tracking.get("watch_log_graph", False),
                )
                print("✓ Model watching enabled (W&B)")
            except Exception as e:
                print(f"Warning: Could not watch model: {e}")

    def log_system_metrics(self):
        """Log system metrics (GPU, CPU, memory)."""
        if self.wandb_run:
            # W&B logs system metrics automatically
            pass

    def finish(self):
        """Finish tracking and cleanup."""
        if self.mlflow_run:
            try:
                self.mlflow.end_run()
                print("✓ MLflow run ended")
            except Exception as e:
                print(f"Warning: Could not end MLflow run: {e}")

        if self.wandb_run:
            try:
                self.wandb.finish()
                print("✓ W&B run finished")
            except Exception as e:
                print(f"Warning: Could not finish W&B run: {e}")

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict:
        """Flatten nested dictionary."""
        items: list = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                # Convert to string if not a simple type
                if not isinstance(v, (int, float, str, bool, type(None))):
                    v = str(v)
                items.append((new_key, v))
        return dict(items)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.finish()
