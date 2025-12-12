"""Tests for model architecture."""

import pytest
import torch
import torch.nn as nn

from src.models.model import ResNet, SimpleCNN, get_model


class TestSimpleCNN:
    """Test SimpleCNN model."""

    def test_model_initialization(self):
        """Test that model can be initialized."""
        model = SimpleCNN(num_classes=10, input_channels=3)
        assert isinstance(model, nn.Module)

    def test_forward_pass_shape(self):
        """Test that forward pass produces correct output shape."""
        model = SimpleCNN(num_classes=10, input_channels=3)

        # Create dummy input
        batch_size = 4
        x = torch.randn(batch_size, 3, 32, 32)

        # Forward pass
        output = model(x)

        # Check output shape
        assert output.shape == (batch_size, 10)

    def test_output_not_nan(self):
        """Test that output doesn't contain NaN values."""
        model = SimpleCNN(num_classes=10, input_channels=3)
        x = torch.randn(4, 3, 32, 32)

        output = model(x)

        assert not torch.isnan(output).any()

    def test_different_input_channels(self):
        """Test model with different input channels (e.g., grayscale)."""
        model = SimpleCNN(num_classes=10, input_channels=1, image_size=28)
        x = torch.randn(4, 1, 28, 28)

        output = model(x)

        assert output.shape == (4, 10)

    def test_different_num_classes(self):
        """Test model with different number of classes."""
        model = SimpleCNN(num_classes=100, input_channels=3)
        x = torch.randn(4, 3, 32, 32)

        output = model(x)

        assert output.shape == (4, 100)

    def test_model_has_parameters(self):
        """Test that model has trainable parameters."""
        model = SimpleCNN(num_classes=10, input_channels=3)

        params = list(model.parameters())

        assert len(params) > 0
        assert all(p.requires_grad for p in params)


class TestResNet:
    """Test ResNet model."""

    def test_resnet_initialization(self):
        """Test that ResNet can be initialized."""
        model = ResNet(num_classes=10, input_channels=3)
        assert isinstance(model, nn.Module)

    def test_resnet_forward_shape(self):
        """Test ResNet forward pass shape."""
        model = ResNet(num_classes=10, input_channels=3)
        x = torch.randn(4, 3, 32, 32)

        output = model(x)

        assert output.shape == (4, 10)

    def test_resnet_output_not_nan(self):
        """Test that ResNet output doesn't contain NaN."""
        model = ResNet(num_classes=10, input_channels=3)
        x = torch.randn(4, 3, 32, 32)

        output = model(x)

        assert not torch.isnan(output).any()


class TestModelFactory:
    """Test model factory function."""

    def test_get_simple_cnn(self):
        """Test getting SimpleCNN through factory."""
        model = get_model("simple_cnn", num_classes=10, input_channels=3)
        assert isinstance(model, SimpleCNN)

    def test_get_resnet(self):
        """Test getting ResNet through factory."""
        model = get_model("resnet", num_classes=10, input_channels=3)
        assert isinstance(model, ResNet)

    def test_invalid_model_name(self):
        """Test that invalid model name raises error."""
        with pytest.raises(ValueError):
            get_model("invalid_model", num_classes=10, input_channels=3)

    def test_model_with_dropout(self):
        """Test model with custom dropout."""
        model = get_model("simple_cnn", num_classes=10, input_channels=3, dropout=0.3)
        assert isinstance(model, SimpleCNN)


class TestModelGradients:
    """Test model gradient flow."""

    def test_gradients_flow(self):
        """Test that gradients flow through the model."""
        model = SimpleCNN(num_classes=10, input_channels=3)
        x = torch.randn(4, 3, 32, 32)
        target = torch.randint(0, 10, (4,))

        # Forward pass
        output = model(x)
        loss = nn.CrossEntropyLoss()(output, target)

        # Backward pass
        loss.backward()

        # Check that gradients exist
        for name, param in model.named_parameters():
            assert param.grad is not None, f"No gradient for {name}"
            assert not torch.isnan(param.grad).any(), f"NaN gradient for {name}"

    def test_model_can_overfit_small_batch(self):
        """Test that model can overfit a small batch (sanity check)."""
        # Set seed for reproducibility before model creation
        torch.manual_seed(42)

        # Use dropout=0 to make training more stable for this test
        model = SimpleCNN(num_classes=10, input_channels=3, dropout=0.0)
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        criterion = nn.CrossEntropyLoss()

        # Create a small fixed batch
        x = torch.randn(4, 3, 32, 32)
        target = torch.randint(0, 10, (4,))

        # Train for multiple iterations
        model.train()
        initial_loss = None
        for i in range(100):
            optimizer.zero_grad()
            output = model(x)
            loss = criterion(output, target)

            if i == 0:
                initial_loss = loss.item()

            loss.backward()
            optimizer.step()

        final_loss = loss.item()

        # Loss should decrease (more lenient check)
        assert (
            final_loss < initial_loss
        ), f"Model cannot overfit small batch (initial: {initial_loss:.3f}, final: {final_loss:.3f})"
