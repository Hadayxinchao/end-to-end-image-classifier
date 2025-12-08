"""Prediction and inference utilities."""

import torch
import torch.nn as nn
from pathlib import Path
from PIL import Image
from torchvision import transforms
from typing import Tuple, List
import numpy as np


CIFAR10_CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                   'dog', 'frog', 'horse', 'ship', 'truck']

MNIST_CLASSES = [str(i) for i in range(10)]


def load_model(model_path: str, model: nn.Module, device: str = 'cpu') -> nn.Module:
    """
    Load trained model from checkpoint.
    
    Args:
        model_path: Path to model checkpoint
        model: Model architecture
        device: Device to load model on
        
    Returns:
        Loaded model
    """
    checkpoint = torch.load(model_path, map_location=device)
    
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    
    model.to(device)
    model.eval()
    
    return model


def preprocess_image(image_path: str, image_size: int = 32, 
                     dataset: str = 'cifar10') -> torch.Tensor:
    """
    Preprocess a single image for inference.
    
    Args:
        image_path: Path to image file
        image_size: Size to resize image to
        dataset: Dataset type ('cifar10' or 'mnist')
        
    Returns:
        Preprocessed image tensor
    """
    image = Image.open(image_path)
    
    if dataset == 'mnist':
        image = image.convert('L')  # Convert to grayscale
        transform = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
    else:
        image = image.convert('RGB')
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
    
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    
    return image_tensor


def predict(model: nn.Module, image_tensor: torch.Tensor, 
            device: str = 'cpu', classes: List[str] = CIFAR10_CLASSES) -> Tuple[str, float, np.ndarray]:
    """
    Make prediction on a single image.
    
    Args:
        model: Trained model
        image_tensor: Preprocessed image tensor
        device: Device to run inference on
        classes: List of class names
        
    Returns:
        Tuple of (predicted_class, confidence, all_probabilities)
    """
    model.eval()
    image_tensor = image_tensor.to(device)
    
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    predicted_class = classes[predicted.item()]
    confidence_score = confidence.item()
    all_probs = probabilities.cpu().numpy()[0]
    
    return predicted_class, confidence_score, all_probs


def predict_batch(model: nn.Module, dataloader, device: str = 'cpu') -> Tuple[np.ndarray, np.ndarray]:
    """
    Make predictions on a batch of images.
    
    Args:
        model: Trained model
        dataloader: DataLoader containing images
        device: Device to run inference on
        
    Returns:
        Tuple of (predictions, true_labels)
    """
    model.eval()
    all_predictions = []
    all_labels = []
    
    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            
            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    return np.array(all_predictions), np.array(all_labels)


if __name__ == "__main__":
    import argparse
    import sys
    from pathlib import Path
    
    # Add project root to path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    from src.models.model import get_model
    
    parser = argparse.ArgumentParser(description='Make predictions on images')
    parser.add_argument('--model_path', type=str, required=True, help='Path to trained model')
    parser.add_argument('--image_path', type=str, required=True, help='Path to image')
    parser.add_argument('--dataset', type=str, default='cifar10', choices=['cifar10', 'mnist'])
    parser.add_argument('--model_name', type=str, default='simple_cnn')
    
    args = parser.parse_args()
    
    # Setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Determine model parameters based on dataset
    if args.dataset == 'mnist':
        num_classes = 10
        input_channels = 1
        classes = MNIST_CLASSES
    else:
        num_classes = 10
        input_channels = 3
        classes = CIFAR10_CLASSES
    
    # Load model
    model = get_model(args.model_name, num_classes=num_classes, input_channels=input_channels)
    model = load_model(args.model_path, model, device)
    
    # Preprocess image
    image_tensor = preprocess_image(args.image_path, dataset=args.dataset)
    
    # Make prediction
    pred_class, confidence, probs = predict(model, image_tensor, device, classes)
    
    print(f"\nPrediction: {pred_class}")
    print(f"Confidence: {confidence:.4f}")
    print("\nAll class probabilities:")
    for cls, prob in zip(classes, probs):
        print(f"  {cls}: {prob:.4f}")
