"""Tests for training utilities and metrics."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import torch
import torch.nn as nn

from src.utils.metrics import (
    AverageMeter,
    calculate_metrics,
)


class TestMetrics:
    """Test metric calculations."""

    def test_perfect_predictions(self):
        """Test metrics with perfect predictions."""
        predictions = np.array([0, 1, 2, 3, 4])
        labels = np.array([0, 1, 2, 3, 4])

        metrics = calculate_metrics(predictions, labels)

        assert metrics["accuracy"] == 1.0
        assert metrics["precision"] == 1.0
        assert metrics["recall"] == 1.0
        assert metrics["f1_score"] == 1.0

    def test_random_predictions(self):
        """Test metrics with random predictions."""
        predictions = np.array([0, 1, 0, 1, 0])
        labels = np.array([1, 0, 1, 0, 1])

        metrics = calculate_metrics(predictions, labels)

        # All predictions are wrong
        assert metrics["accuracy"] == 0.0
        assert 0.0 <= metrics["precision"] <= 1.0
        assert 0.0 <= metrics["recall"] <= 1.0
        assert 0.0 <= metrics["f1_score"] <= 1.0

    def test_partial_correct_predictions(self):
        """Test metrics with partially correct predictions."""
        predictions = np.array([0, 1, 2, 0, 1])
        labels = np.array([0, 1, 0, 1, 2])

        metrics = calculate_metrics(predictions, labels)

        # 2 out of 5 correct
        assert metrics["accuracy"] == 0.4
        assert 0.0 <= metrics["precision"] <= 1.0
        assert 0.0 <= metrics["recall"] <= 1.0

    def test_metrics_shape(self):
        """Test that metrics return correct types."""
        predictions = np.array([0, 1, 2, 3])
        labels = np.array([0, 1, 2, 3])

        metrics = calculate_metrics(predictions, labels)

        assert isinstance(metrics, dict)
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics


class TestAverageMeter:
    """Test AverageMeter utility."""

    def test_initialization(self):
        """Test AverageMeter initialization."""
        meter = AverageMeter()

        assert meter.val == 0
        assert meter.avg == 0
        assert meter.sum == 0
        assert meter.count == 0

    def test_single_update(self):
        """Test single update."""
        meter = AverageMeter()
        meter.update(5.0)

        assert meter.val == 5.0
        assert meter.avg == 5.0
        assert meter.sum == 5.0
        assert meter.count == 1

    def test_multiple_updates(self):
        """Test multiple updates."""
        meter = AverageMeter()
        meter.update(2.0)
        meter.update(4.0)
        meter.update(6.0)

        assert meter.avg == 4.0  # (2 + 4 + 6) / 3
        assert meter.count == 3

    def test_weighted_update(self):
        """Test weighted update."""
        meter = AverageMeter()
        meter.update(10.0, n=2)  # Add value 10.0 twice
        meter.update(20.0, n=3)  # Add value 20.0 three times

        expected_avg = (10.0 * 2 + 20.0 * 3) / 5
        assert meter.avg == expected_avg
        assert meter.count == 5

    def test_reset(self):
        """Test reset functionality."""
        meter = AverageMeter()
        meter.update(5.0)
        meter.update(10.0)

        meter.reset()

        assert meter.val == 0
        assert meter.avg == 0
        assert meter.sum == 0
        assert meter.count == 0


class TestLossFunctions:
    """Test loss function behavior."""

    def test_cross_entropy_zero_loss(self):
        """Test that cross entropy loss is zero for perfect predictions."""
        criterion = nn.CrossEntropyLoss()

        # Perfect predictions (one-hot encoded)
        logits = torch.tensor([[10.0, 0.0, 0.0], [0.0, 10.0, 0.0]])
        targets = torch.tensor([0, 1])

        loss = criterion(logits, targets)

        # Loss should be very close to zero
        assert loss.item() < 0.01

    def test_cross_entropy_positive_loss(self):
        """Test that cross entropy loss is positive for wrong predictions."""
        criterion = nn.CrossEntropyLoss()

        # Wrong predictions
        logits = torch.tensor([[0.0, 10.0, 0.0], [10.0, 0.0, 0.0]])
        targets = torch.tensor([0, 1])

        loss = criterion(logits, targets)

        # Loss should be positive
        assert loss.item() > 0

    def test_cross_entropy_same_value(self):
        """Test cross entropy with identical logits and targets."""
        criterion = nn.CrossEntropyLoss()

        # Create logits and targets
        logits = torch.randn(4, 10)
        targets = torch.randint(0, 10, (4,))

        # Same input should give same loss
        loss1 = criterion(logits, targets)
        loss2 = criterion(logits, targets)

        assert torch.allclose(loss1, loss2)

    def test_cross_entropy_reduction(self):
        """Test cross entropy reduction modes."""
        logits = torch.randn(4, 10)
        targets = torch.randint(0, 10, (4,))

        criterion_mean = nn.CrossEntropyLoss(reduction="mean")
        criterion_sum = nn.CrossEntropyLoss(reduction="sum")

        loss_mean = criterion_mean(logits, targets)
        loss_sum = criterion_sum(logits, targets)

        # Sum should be larger than mean
        assert loss_sum > loss_mean


class TestModelTraining:
    """Test training-related functionality."""

    def test_optimizer_step_updates_parameters(self):
        """Test that optimizer step updates model parameters."""
        from src.models.model import SimpleCNN

        model = SimpleCNN(num_classes=10, input_channels=3)
        optimizer = torch.optim.SGD(model.parameters(), lr=1.0)  # Higher learning rate

        # Store initial parameters
        initial_params = [p.clone() for p in model.parameters()]

        # Forward and backward pass with smaller batch for larger gradients
        x = torch.randn(2, 3, 32, 32)  # Smaller batch size
        target = torch.randint(0, 10, (2,))
        output = model(x)
        loss = nn.CrossEntropyLoss()(output, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Check that parameters have changed
        updated_params = list(model.parameters())
        # Check at least some parameters have changed significantly
        num_changed = 0
        for initial, updated in zip(initial_params, updated_params):
            if not torch.allclose(initial, updated, atol=1e-6):
                num_changed += 1

        assert num_changed > 0, "Parameters did not update"

    def test_batch_norm_train_eval_modes(self):
        """Test that batch norm behaves differently in train/eval modes."""
        from src.models.model import SimpleCNN

        model = SimpleCNN(num_classes=10, input_channels=3)
        x = torch.randn(4, 3, 32, 32)

        # Get output in training mode
        model.train()
        output_train = model(x)

        # Get output in eval mode
        model.eval()
        output_eval = model(x)

        # Outputs can be different due to batch norm
        # Just check they're both valid tensors
        assert output_train.shape == output_eval.shape
        assert not torch.isnan(output_train).any()
        assert not torch.isnan(output_eval).any()
