"""Training script with Hydra configuration management."""

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR, ReduceLROnPlateau
import hydra
from omegaconf import DictConfig, OmegaConf
from pathlib import Path
from tqdm import tqdm
import random
import numpy as np
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data.make_dataset import load_cifar10, load_mnist
from src.models.model import get_model
from src.models.predict import predict_batch
from src.utils.metrics import (
    AverageMeter, calculate_metrics, plot_confusion_matrix,
    save_classification_report, plot_training_history
)


def set_seed(seed: int):
    """Set random seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_device(device_config: str) -> torch.device:
    """Get device based on configuration."""
    if device_config == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        return torch.device(device_config)


def train_epoch(model, train_loader, criterion, optimizer, device, clip_grad_norm=None):
    """Train for one epoch."""
    model.train()
    
    losses = AverageMeter()
    correct = 0
    total = 0
    
    pbar = tqdm(train_loader, desc="Training")
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping
        if clip_grad_norm is not None:
            torch.nn.utils.clip_grad_norm_(model.parameters(), clip_grad_norm)
        
        optimizer.step()
        
        # Update metrics
        losses.update(loss.item(), images.size(0))
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        # Update progress bar
        pbar.set_postfix({
            'loss': f'{losses.avg:.4f}',
            'acc': f'{100.*correct/total:.2f}%'
        })
    
    return losses.avg, 100. * correct / total


def validate(model, val_loader, criterion, device):
    """Validate the model."""
    model.eval()
    
    losses = AverageMeter()
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(val_loader, desc="Validation")
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            losses.update(loss.item(), images.size(0))
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({
                'loss': f'{losses.avg:.4f}',
                'acc': f'{100.*correct/total:.2f}%'
            })
    
    return losses.avg, 100. * correct / total


def get_optimizer(model, cfg):
    """Get optimizer based on configuration."""
    if cfg.hyperparameters.optimizer.lower() == "adam":
        return optim.Adam(
            model.parameters(),
            lr=cfg.hyperparameters.learning_rate,
            weight_decay=cfg.hyperparameters.weight_decay
        )
    elif cfg.hyperparameters.optimizer.lower() == "sgd":
        return optim.SGD(
            model.parameters(),
            lr=cfg.hyperparameters.learning_rate,
            momentum=cfg.hyperparameters.momentum,
            weight_decay=cfg.hyperparameters.weight_decay
        )
    else:
        raise ValueError(f"Unknown optimizer: {cfg.hyperparameters.optimizer}")


def get_scheduler(optimizer, cfg):
    """Get learning rate scheduler based on configuration."""
    if not cfg.hyperparameters.use_scheduler:
        return None
    
    scheduler_type = cfg.hyperparameters.scheduler_type.lower()
    
    if scheduler_type == "step":
        return StepLR(
            optimizer,
            step_size=cfg.hyperparameters.step_size,
            gamma=cfg.hyperparameters.gamma
        )
    elif scheduler_type == "cosine":
        return CosineAnnealingLR(
            optimizer,
            T_max=cfg.hyperparameters.num_epochs,
            eta_min=cfg.hyperparameters.min_lr
        )
    elif scheduler_type == "plateau":
        return ReduceLROnPlateau(
            optimizer,
            mode='min',
            factor=cfg.hyperparameters.gamma,
            patience=5,
            min_lr=cfg.hyperparameters.min_lr
        )
    else:
        raise ValueError(f"Unknown scheduler type: {scheduler_type}")


@hydra.main(version_base=None, config_path="../../configs", config_name="config")
def main(cfg: DictConfig):
    """Main training function."""
    
    # Print configuration
    print("=" * 80)
    print("Configuration:")
    print(OmegaConf.to_yaml(cfg))
    print("=" * 80)
    
    # Set seed
    set_seed(cfg.seed)
    
    # Get device
    device = get_device(cfg.device)
    print(f"\nUsing device: {device}")
    
    # Load data
    print(f"\nLoading {cfg.data.name} dataset...")
    if cfg.data.name == "cifar10":
        train_loader, val_loader, test_loader = load_cifar10(
            data_dir=cfg.data.data_dir,
            batch_size=cfg.hyperparameters.batch_size,
            val_split=cfg.data.val_split,
            num_workers=cfg.num_workers
        )
    elif cfg.data.name == "mnist":
        train_loader, val_loader, test_loader = load_mnist(
            data_dir=cfg.data.data_dir,
            batch_size=cfg.hyperparameters.batch_size,
            val_split=cfg.data.val_split,
            num_workers=cfg.num_workers
        )
    else:
        raise ValueError(f"Unknown dataset: {cfg.data.name}")
    
    print(f"Train batches: {len(train_loader)}")
    print(f"Val batches: {len(val_loader)}")
    print(f"Test batches: {len(test_loader)}")
    
    # Create model
    print(f"\nCreating {cfg.model.name} model...")
    model = get_model(
        model_name=cfg.model.name,
        num_classes=cfg.data.num_classes,
        input_channels=cfg.data.input_channels,
        image_size=cfg.data.image_size,
        dropout=cfg.hyperparameters.dropout
    )
    model = model.to(device)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss(label_smoothing=cfg.hyperparameters.label_smoothing)
    optimizer = get_optimizer(model, cfg)
    scheduler = get_scheduler(optimizer, cfg)
    
    # Training history
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    best_val_acc = 0.0
    patience_counter = 0
    
    # Training loop
    print(f"\nStarting training for {cfg.hyperparameters.num_epochs} epochs...")
    print("=" * 80)
    
    for epoch in range(cfg.hyperparameters.num_epochs):
        print(f"\nEpoch {epoch + 1}/{cfg.hyperparameters.num_epochs}")
        print("-" * 80)
        
        # Train
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device,
            clip_grad_norm=cfg.hyperparameters.clip_grad_norm
        )
        
        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        # Update learning rate
        if scheduler is not None:
            if isinstance(scheduler, ReduceLROnPlateau):
                scheduler.step(val_loss)
            else:
                scheduler.step()
        
        # Save history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        # Print epoch summary
        current_lr = optimizer.param_groups[0]['lr']
        print(f"\nEpoch Summary:")
        print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
        print(f"  Learning Rate: {current_lr:.6f}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            
            if cfg.save_best_only:
                model_save_path = Path(cfg.model_save_dir) / f"{cfg.model.name}_best.pth"
                model_save_path.parent.mkdir(parents=True, exist_ok=True)
                
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_acc': val_acc,
                    'config': OmegaConf.to_container(cfg)
                }, model_save_path)
                
                print(f"  ✓ Best model saved! (Val Acc: {val_acc:.2f}%)")
        else:
            patience_counter += 1
        
        # Early stopping
        if patience_counter >= cfg.early_stopping_patience:
            print(f"\nEarly stopping triggered after {epoch + 1} epochs")
            break
    
    print("\n" + "=" * 80)
    print("Training completed!")
    print(f"Best validation accuracy: {best_val_acc:.2f}%")
    
    # Load best model for evaluation
    best_model_path = Path(cfg.model_save_dir) / f"{cfg.model.name}_best.pth"
    if best_model_path.exists():
        checkpoint = torch.load(best_model_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        print(f"\nLoaded best model from epoch {checkpoint['epoch'] + 1}")
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    test_loss, test_acc = validate(model, test_loader, criterion, device)
    print(f"Test Loss: {test_loss:.4f}, Test Acc: {test_acc:.2f}%")
    
    # Generate predictions and metrics
    print("\nGenerating predictions and metrics...")
    predictions, true_labels = predict_batch(model, test_loader, device)
    
    # Calculate metrics
    metrics = calculate_metrics(predictions, true_labels)
    print("\nTest Metrics:")
    for metric_name, metric_value in metrics.items():
        print(f"  {metric_name}: {metric_value:.4f}")
    
    # Save reports
    report_dir = Path(cfg.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Confusion matrix
    plot_confusion_matrix(
        predictions, true_labels, cfg.data.classes,
        save_path=str(report_dir / "confusion_matrix.png")
    )
    
    # Classification report
    save_classification_report(
        predictions, true_labels, cfg.data.classes,
        save_path=str(report_dir / "classification_report.txt")
    )
    
    # Training history plot
    plot_training_history(
        history,
        save_path=str(report_dir / "training_history.png")
    )
    
    print(f"\nReports saved to {report_dir}")
    print("\n" + "=" * 80)
    print("All done! 🎉")


if __name__ == "__main__":
    main()
