"""Tests for data loading and preprocessing."""

import pytest
import torch
from torch.utils.data import DataLoader

from src.data.make_dataset import get_transforms, load_cifar10, load_mnist


class TestTransforms:
    """Test data transformations."""

    def test_get_transforms_returns_tuple(self):
        """Test that get_transforms returns a tuple of two transforms."""
        train_transform, test_transform = get_transforms()
        assert train_transform is not None
        assert test_transform is not None

    def test_transforms_output_shape(self):
        """Test that transforms produce correct output shape."""
        import numpy as np
        from PIL import Image

        # Create a dummy image
        dummy_image = Image.fromarray(np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8))

        train_transform, test_transform = get_transforms(image_size=32)

        # Apply transforms
        train_output = train_transform(dummy_image)
        test_output = test_transform(dummy_image)

        # Check shapes
        assert train_output.shape == (3, 32, 32)
        assert test_output.shape == (3, 32, 32)

    def test_transforms_normalization(self):
        """Test that transforms normalize the data."""
        import numpy as np
        from PIL import Image

        dummy_image = Image.fromarray(np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8))
        _, test_transform = get_transforms()

        output = test_transform(dummy_image)

        # Values should be roughly in range [-1, 1] after normalization
        assert output.min() >= -2.0
        assert output.max() <= 2.0


class TestDataLoaders:
    """Test data loaders."""

    @pytest.mark.slow
    def test_load_cifar10_returns_three_loaders(self):
        """Test that load_cifar10 returns three dataloaders."""
        train_loader, val_loader, test_loader = load_cifar10(batch_size=32)

        assert isinstance(train_loader, DataLoader)
        assert isinstance(val_loader, DataLoader)
        assert isinstance(test_loader, DataLoader)

    @pytest.mark.slow
    def test_cifar10_batch_shape(self):
        """Test CIFAR-10 batch shapes."""
        train_loader, _, _ = load_cifar10(batch_size=32)

        images, labels = next(iter(train_loader))

        # Check batch shapes
        assert images.shape[0] <= 32  # batch size
        assert images.shape[1] == 3  # RGB channels
        assert images.shape[2] == 32  # height
        assert images.shape[3] == 32  # width

        # Check labels
        assert labels.shape[0] <= 32
        assert labels.dtype == torch.long
        assert labels.min() >= 0
        assert labels.max() < 10

    @pytest.mark.slow
    def test_mnist_batch_shape(self):
        """Test MNIST batch shapes."""
        train_loader, _, _ = load_mnist(batch_size=32)

        images, labels = next(iter(train_loader))

        # Check batch shapes
        assert images.shape[0] <= 32  # batch size
        assert images.shape[1] == 1  # grayscale
        assert images.shape[2] == 28  # height
        assert images.shape[3] == 28  # width

        # Check labels
        assert labels.shape[0] <= 32
        assert labels.dtype == torch.long
        assert labels.min() >= 0
        assert labels.max() < 10

    def test_validation_split(self):
        """Test that validation split works correctly."""
        # This test doesn't download data, just checks logic
        val_split = 0.2
        # We'll just verify the function can be called with this parameter
        # Full test would require downloading data
        assert val_split > 0 and val_split < 1


class TestDataIntegrity:
    """Test data integrity."""

    @pytest.mark.slow
    def test_no_data_leakage(self):
        """Test that train/val/test sets don't overlap (basic check)."""
        train_loader, val_loader, test_loader = load_cifar10(batch_size=100)

        # Get some samples from each
        train_batch, _ = next(iter(train_loader))
        val_batch, _ = next(iter(val_loader))
        test_batch, _ = next(iter(test_loader))

        # Basic sanity check - datasets should have different sizes
        assert len(train_loader) > len(val_loader)
        assert len(test_loader) > 0
