"""Test script for FastAPI serving endpoint."""

import io
import sys
from pathlib import Path

import requests
from PIL import Image

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

API_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200


def test_predict(image_path: str):
    """Test predict endpoint."""
    print(f"Testing /predict endpoint with {image_path}...")

    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        return False

    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_URL}/predict", files=files)

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Predicted: {data['predicted_class']}")
        print(f"   Confidence: {data['confidence']:.4f}")
        print(f"   Top 3 classes:")
        sorted_probs = sorted(
            data["all_probabilities"].items(), key=lambda x: x[1], reverse=True
        )
        for cls, prob in sorted_probs[:3]:
            print(f"     - {cls}: {prob:.4f}")
    else:
        print(f"❌ Error: {response.text}")

    print()
    return response.status_code == 200


def test_classes():
    """Test classes endpoint."""
    print("Testing /classes endpoint...")
    response = requests.get(f"{API_URL}/classes")
    print(f"Status: {response.status_code}")
    print(f"Classes: {response.json()}\n")
    return response.status_code == 200


def test_model_info():
    """Test model-info endpoint."""
    print("Testing /model-info endpoint...")
    response = requests.get(f"{API_URL}/model-info")
    print(f"Status: {response.status_code}")
    print(f"Model info: {response.json()}\n")
    return response.status_code == 200


def create_dummy_image():
    """Create a dummy image for testing."""
    import numpy as np

    # Create random RGB image
    img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
    img = Image.fromarray(img_array, "RGB")

    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes


def test_predict_dummy():
    """Test predict with dummy image."""
    print("Testing /predict with dummy image...")

    img_bytes = create_dummy_image()
    files = {"file": ("test.png", img_bytes, "image/png")}
    response = requests.post(f"{API_URL}/predict", files=files)

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Predicted: {data['predicted_class']}")
        print(f"   Confidence: {data['confidence']:.4f}")
    else:
        print(f"❌ Error: {response.text}")

    print()
    return response.status_code == 200


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test FastAPI serving endpoint")
    parser.add_argument("--url", type=str, default=API_URL, help="API URL")
    parser.add_argument("--image", type=str, help="Path to test image")

    args = parser.parse_args()
    API_URL = args.url

    print("=" * 80)
    print("Testing Image Classifier API")
    print("=" * 80 + "\n")

    # Run tests
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Get Classes", test_classes()))
    results.append(("Model Info", test_model_info()))
    results.append(("Predict (dummy)", test_predict_dummy()))

    if args.image:
        results.append(("Predict (real)", test_predict(args.image)))

    # Summary
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\n{passed}/{total} tests passed")
