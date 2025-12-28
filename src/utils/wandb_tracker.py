"""Enhanced experiment tracking with W&B support."""

from pathlib import Path
from typing import Any, Dict, Optional

import torch
import torch.nn as nn
from omegaconf import DictConfig, OmegaConf

try:
    import wandb

    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False
    print("Warning: W&B not available. Install with: pip install wandb")

try:
    import mlflow
    import mlflow.pytorch

    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("Warning: MLflow not available.")


class WandBTracker:
    """Weights & Biases experiment tracker with model artifact logging."""

    def __init__(self, cfg: DictConfig, project: str = "image-classifier"):
        """Initialize W&B tracker."""
        if not WANDB_AVAILABLE:
            raise ImportError("wandb not installed. Install with: pip install wandb")

        # Initialize wandb
        self.run = wandb.init(
            project=project,
            name=cfg.get("experiment_name", None),
            config=OmegaConf.to_container(cfg, resolve=True),  # type: ignore[arg-type]
            tags=[cfg.model.name, cfg.data.name],
            notes=cfg.get("description", ""),
            reinit=True,
            settings=wandb.Settings(start_method="thread"),
        )

        self.cfg = cfg
        self.best_metric = float("inf")

    def log_params(self, params: Dict[str, Any]):
        """Log parameters."""
        wandb.config.update(params)

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics."""
        wandb.log(metrics, step=step)

    def log_model_architecture(self, model: nn.Module):
        """Log model architecture and watch gradients."""
        # Watch model for gradient tracking
        wandb.watch(model, log="all", log_freq=100)

        # Log model architecture as text
        model_str = str(model)
        wandb.log({"model_architecture": wandb.Html(f"<pre>{model_str}</pre>")})

    def log_weights_histograms(self, model: nn.Module, step: int):
        """Log weight and bias histograms."""
        histograms = {}
        for name, param in model.named_parameters():
            if param.requires_grad:
                histograms[f"weights/{name}"] = wandb.Histogram(param.data.cpu().numpy())
                if param.grad is not None:
                    histograms[f"gradients/{name}"] = wandb.Histogram(param.grad.cpu().numpy())

        wandb.log(histograms, step=step)

    def log_learning_rate(self, lr: float, step: int):
        """Log learning rate."""
        wandb.log({"learning_rate": lr}, step=step)

    def log_image(self, key: str, image, caption: str = ""):
        """Log an image."""
        wandb.log({key: wandb.Image(image, caption=caption)})

    def log_artifact(self, artifact_path: str, artifact_type: str = "model", name: str = None):
        """Log an artifact (model checkpoint, dataset, etc)."""
        artifact_name = name or Path(artifact_path).stem
        artifact = wandb.Artifact(artifact_name, type=artifact_type)
        artifact.add_file(artifact_path)
        self.run.log_artifact(artifact)

    def log_model_checkpoint(
        self,
        model: nn.Module,
        checkpoint_path: str,
        metrics: Dict[str, float],
        is_best: bool = False,
    ):
        """Log model checkpoint with metadata."""
        # Save model state
        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "metrics": metrics,
                "config": OmegaConf.to_container(self.cfg, resolve=True),
            },
            checkpoint_path,
        )

        # Create artifact
        artifact_name = f"model-{self.run.id}" if not is_best else f"model-{self.run.id}-best"
        artifact = wandb.Artifact(
            artifact_name,
            type="model",
            metadata={
                **metrics,
                "is_best": is_best,
                "model_name": self.cfg.model.name,
                "dataset": self.cfg.data.name,
            },
        )
        artifact.add_file(checkpoint_path)
        self.run.log_artifact(artifact, aliases=["latest"] + (["best"] if is_best else []))

    def finish(self):
        """Finish the run."""
        wandb.finish()


class MLflowTracker:
    """MLflow experiment tracker (existing implementation)."""

    def __init__(self, cfg: DictConfig):
        """Initialize MLflow tracker."""
        if not MLFLOW_AVAILABLE:
            raise ImportError("mlflow not installed")

        # Set tracking URI if specified
        if hasattr(cfg.tracking, "uri"):
            mlflow.set_tracking_uri(cfg.tracking.uri)

        # Set experiment
        experiment_name = cfg.get("experiment_name", "image-classifier")
        mlflow.set_experiment(experiment_name)

        # Start run
        self.run = mlflow.start_run(run_name=cfg.get("run_name", None))
        self.cfg = cfg

    def log_params(self, params: Dict[str, Any]):
        """Log parameters."""
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics."""
        mlflow.log_metrics(metrics, step=step)

    def log_model_architecture(self, model: nn.Module):
        """Log model architecture."""
        mlflow.log_text(str(model), "model_architecture.txt")

    def log_artifact(self, artifact_path: str):
        """Log an artifact."""
        mlflow.log_artifact(artifact_path)

    def log_model_checkpoint(
        self,
        model: nn.Module,
        checkpoint_path: str,
        metrics: Dict[str, float],
        is_best: bool = False,
    ):
        """Log model checkpoint."""
        mlflow.log_artifact(checkpoint_path)
        if is_best:
            mlflow.pytorch.log_model(model, "best_model")

    def finish(self):
        """End the run."""
        mlflow.end_run()


class ExperimentTracker:
    """Unified experiment tracker supporting both MLflow and W&B."""

    def __init__(self, cfg: DictConfig, tracking_backend: str = "wandb"):
        """Initialize experiment tracker.

        Args:
            cfg: Hydra configuration
            tracking_backend: 'wandb', 'mlflow', or 'both'
        """
        self.cfg = cfg
        self.backend = tracking_backend.lower()
        self.trackers = []

        # Initialize W&B
        if self.backend in ["wandb", "both"]:
            if WANDB_AVAILABLE:
                try:
                    project = (
                        cfg.tracking.get("project", "image-classifier")
                        if hasattr(cfg, "tracking")
                        else "image-classifier"
                    )
                    self.wandb_tracker = WandBTracker(cfg, project=project)
                    self.trackers.append(self.wandb_tracker)
                    print("✅ W&B tracker initialized")
                except Exception as e:
                    print(f"⚠️  Failed to initialize W&B: {e}")

        # Initialize MLflow
        if self.backend in ["mlflow", "both"]:
            if MLFLOW_AVAILABLE:
                try:
                    self.mlflow_tracker = MLflowTracker(cfg)
                    self.trackers.append(self.mlflow_tracker)  # type: ignore
                    print("✅ MLflow tracker initialized")
                except Exception as e:
                    print(f"⚠️  Failed to initialize MLflow: {e}")

        if not self.trackers:
            print("⚠️  No tracking backends initialized")

    def log_params(self, params: Dict[str, Any]):
        """Log parameters to all trackers."""
        for tracker in self.trackers:
            tracker.log_params(params)

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics to all trackers."""
        for tracker in self.trackers:
            tracker.log_metrics(metrics, step=step)

    def log_model_architecture(self, model: nn.Module):
        """Log model architecture to all trackers."""
        for tracker in self.trackers:
            tracker.log_model_architecture(model)

    def log_weights_histograms(self, model: nn.Module, step: int):
        """Log weight histograms (W&B only)."""
        if hasattr(self, "wandb_tracker"):
            self.wandb_tracker.log_weights_histograms(model, step)

    def log_learning_rate(self, lr: float, step: int):
        """Log learning rate."""
        if hasattr(self, "wandb_tracker"):
            self.wandb_tracker.log_learning_rate(lr, step)

    def log_image(self, key: str, image, caption: str = ""):
        """Log image (W&B only)."""
        if hasattr(self, "wandb_tracker"):
            self.wandb_tracker.log_image(key, image, caption)

    def log_artifact(self, artifact_path: str, artifact_type: str = "model", name: str = None):
        """Log artifact to all trackers."""
        for tracker in self.trackers:
            if isinstance(tracker, WandBTracker):
                tracker.log_artifact(artifact_path, artifact_type, name)
            else:
                tracker.log_artifact(artifact_path)

    def log_model_checkpoint(
        self,
        model: nn.Module,
        checkpoint_path: str,
        metrics: Dict[str, float],
        is_best: bool = False,
    ):
        """Log model checkpoint to all trackers."""
        for tracker in self.trackers:
            tracker.log_model_checkpoint(model, checkpoint_path, metrics, is_best)

    def finish(self):
        """Finish all tracking runs."""
        for tracker in self.trackers:
            tracker.finish()
