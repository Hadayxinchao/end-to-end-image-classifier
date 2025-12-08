"""Data loading and preprocessing utilities."""

import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from pathlib import Path
from typing import Tuple


def get_transforms(image_size: int = 32, mean: Tuple = (0.5, 0.5, 0.5), 
                   std: Tuple = (0.5, 0.5, 0.5)) -> Tuple[transforms.Compose, transforms.Compose]:
    """
    Get train and test transforms.
    
    Args:
        image_size: Size to resize images to
        mean: Mean for normalization
        std: Standard deviation for normalization
        
    Returns:
        Tuple of (train_transform, test_transform)
    """
    train_transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])
    
    test_transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])
    
    return train_transform, test_transform


def load_cifar10(data_dir: str = "./data/raw", batch_size: int = 64, 
                 val_split: float = 0.1, num_workers: int = 2) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Load CIFAR-10 dataset.
    
    Args:
        data_dir: Directory to store/load data
        batch_size: Batch size for dataloaders
        val_split: Fraction of training data to use for validation
        num_workers: Number of workers for data loading
        
    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)
    
    # Get transforms
    train_transform, test_transform = get_transforms()
    
    # Load datasets
    train_dataset = datasets.CIFAR10(
        root=data_dir, train=True, download=True, transform=train_transform
    )
    
    test_dataset = datasets.CIFAR10(
        root=data_dir, train=False, download=True, transform=test_transform
    )
    
    # Split training into train and validation
    val_size = int(len(train_dataset) * val_split)
    train_size = len(train_dataset) - val_size
    
    train_dataset, val_dataset = random_split(
        train_dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(42)
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, 
        num_workers=num_workers, pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=True
    )
    
    return train_loader, val_loader, test_loader


def load_mnist(data_dir: str = "./data/raw", batch_size: int = 64,
               val_split: float = 0.1, num_workers: int = 2) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Load MNIST dataset.
    
    Args:
        data_dir: Directory to store/load data
        batch_size: Batch size for dataloaders
        val_split: Fraction of training data to use for validation
        num_workers: Number of workers for data loading
        
    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)
    
    # MNIST-specific transforms
    train_transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    test_transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    # Load datasets
    train_dataset = datasets.MNIST(
        root=data_dir, train=True, download=True, transform=train_transform
    )
    
    test_dataset = datasets.MNIST(
        root=data_dir, train=False, download=True, transform=test_transform
    )
    
    # Split training into train and validation
    val_size = int(len(train_dataset) * val_split)
    train_size = len(train_dataset) - val_size
    
    train_dataset, val_dataset = random_split(
        train_dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(42)
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
        num_workers=num_workers, pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=True
    )
    
    return train_loader, val_loader, test_loader
