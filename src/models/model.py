"""CNN model architecture for image classification."""

from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleCNN(nn.Module):
    """Simple CNN for image classification."""

    def __init__(
        self,
        num_classes: int = 10,
        input_channels: int = 3,
        dropout: float = 0.5,
        image_size: int = 32,
    ):
        """
        Initialize the CNN model.

        Args:
            num_classes: Number of output classes
            input_channels: Number of input channels (3 for RGB, 1 for grayscale)
            dropout: Dropout probability
            image_size: Input image size (height and width)
        """
        super(SimpleCNN, self).__init__()

        self.num_classes = num_classes
        self.input_channels = input_channels

        # Convolutional layers
        self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)

        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)

        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)

        # Pooling and dropout
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(dropout)

        # Calculate size after conv layers
        # After 3 pooling layers (each divides by 2): image_size / 8
        conv_output_size = image_size // 8
        fc_input_size = 128 * conv_output_size * conv_output_size

        # Fully connected layers
        self.fc1 = nn.Linear(fc_input_size, 256)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.

        Args:
            x: Input tensor of shape (batch_size, channels, height, width)

        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        # Conv block 1
        x = self.conv1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.pool(x)  # 32x32 -> 16x16 (for CIFAR-10)

        # Conv block 2
        x = self.conv2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.pool(x)  # 16x16 -> 8x8

        # Conv block 3
        x = self.conv3(x)
        x = self.bn3(x)
        x = F.relu(x)
        x = self.pool(x)  # 8x8 -> 4x4

        # Flatten
        x = x.view(x.size(0), -1)

        # FC layers
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)

        return x


class ResidualBlock(nn.Module):
    """Residual block for deeper CNN."""

    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        """
        Initialize residual block.

        Args:
            in_channels: Number of input channels
            out_channels: Number of output channels
            stride: Stride for convolution
        """
        super(ResidualBlock, self).__init__()

        self.conv1 = nn.Conv2d(
            in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False
        )
        self.bn1 = nn.BatchNorm2d(out_channels)

        self.conv2 = nn.Conv2d(
            out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with residual connection."""
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet(nn.Module):
    """Simple ResNet-style architecture."""

    def __init__(self, num_classes: int = 10, input_channels: int = 3):
        """
        Initialize ResNet model.

        Args:
            num_classes: Number of output classes
            input_channels: Number of input channels
        """
        super(ResNet, self).__init__()

        self.in_channels = 64

        self.conv1 = nn.Conv2d(input_channels, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)

        self.layer1 = self._make_layer(64, 2, stride=1)
        self.layer2 = self._make_layer(128, 2, stride=2)
        self.layer3 = self._make_layer(256, 2, stride=2)

        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(256, num_classes)

    def _make_layer(self, out_channels: int, num_blocks: int, stride: int):
        """Create a layer with multiple residual blocks."""
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(ResidualBlock(self.in_channels, out_channels, stride))
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.avg_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


def get_model(
    model_name: str = "simple_cnn",
    num_classes: int = 10,
    input_channels: int = 3,
    image_size: int = 32,
    **kwargs: Any,
) -> nn.Module:
    """
    Factory function to get model by name.

    Args:
        model_name: Name of the model ('simple_cnn' or 'resnet')
        num_classes: Number of output classes
        input_channels: Number of input channels
        image_size: Input image size
        **kwargs: Additional arguments for model

    Returns:
        PyTorch model
    """
    if model_name == "simple_cnn":
        return SimpleCNN(
            num_classes=num_classes, input_channels=input_channels, image_size=image_size, **kwargs
        )
    elif model_name == "resnet":
        return ResNet(num_classes=num_classes, input_channels=input_channels)
    else:
        raise ValueError(f"Unknown model name: {model_name}")
