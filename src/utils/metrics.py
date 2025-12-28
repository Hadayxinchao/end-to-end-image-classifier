"""Metrics and evaluation utilities."""

from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

matplotlib.use("Agg")  # Use non-interactive backend for headless environments


def calculate_metrics(predictions: np.ndarray, labels: np.ndarray, average: str = "macro") -> dict:
    """
    Calculate classification metrics.

    Args:
        predictions: Predicted labels
        labels: True labels
        average: Averaging strategy for multi-class metrics

    Returns:
        Dictionary containing metrics
    """
    metrics = {
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(labels, predictions, average=average, zero_division=0),
        "recall": recall_score(labels, predictions, average=average, zero_division=0),
        "f1_score": f1_score(labels, predictions, average=average, zero_division=0),
    }

    return metrics


def plot_confusion_matrix(
    predictions: np.ndarray,
    labels: np.ndarray,
    class_names: List[str],
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8),
):
    """
    Plot confusion matrix.

    Args:
        predictions: Predicted labels
        labels: True labels
        class_names: List of class names
        save_path: Path to save figure
        figsize: Figure size
    """
    cm = confusion_matrix(labels, predictions)

    plt.figure(figsize=figsize)
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names
    )
    plt.title("Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Confusion matrix saved to {save_path}")

    plt.close()


def save_classification_report(
    predictions: np.ndarray, labels: np.ndarray, class_names: List[str], save_path: str
):
    """
    Save classification report to file.

    Args:
        predictions: Predicted labels
        labels: True labels
        class_names: List of class names
        save_path: Path to save report
    """
    report = classification_report(labels, predictions, target_names=class_names, digits=4)

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w") as f:
        f.write("Classification Report\n")
        f.write("=" * 80 + "\n\n")
        f.write(report)
        f.write("\n\n")

        # Add overall metrics
        metrics = calculate_metrics(predictions, labels)
        f.write("Overall Metrics\n")
        f.write("-" * 80 + "\n")
        for metric_name, metric_value in metrics.items():
            f.write(f"{metric_name}: {metric_value:.4f}\n")

    print(f"Classification report saved to {save_path}")


def plot_training_history(
    history: dict, save_path: Optional[str] = None, figsize: Tuple[int, int] = (12, 4)
):
    """
    Plot training history (loss and accuracy).

    Args:
        history: Dictionary containing 'train_loss', 'val_loss', 'train_acc', 'val_acc'
        save_path: Path to save figure
        figsize: Figure size
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Plot loss
    axes[0].plot(history["train_loss"], label="Train Loss")
    if "val_loss" in history:
        axes[0].plot(history["val_loss"], label="Val Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Training and Validation Loss")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot accuracy
    axes[1].plot(history["train_acc"], label="Train Accuracy")
    if "val_acc" in history:
        axes[1].plot(history["val_acc"], label="Val Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].set_title("Training and Validation Accuracy")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Training history plot saved to {save_path}")

    plt.close()


class AverageMeter:
    """Computes and stores the average and current value."""

    def __init__(self):
        """Initialize the AverageMeter."""
        self.reset()

    def reset(self):
        """Reset all statistics."""
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val: float, n: int = 1) -> None:
        """
        Update statistics.

        Args:
            val: Value to add
            n: Number of items
        """
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count if self.count != 0 else 0
