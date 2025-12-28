#!/bin/bash
# Quick start script for automation features

set -e

echo "🚀 MLOps Image Classifier - Automation Quick Start"
echo "=================================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python --version

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Setup pre-commit
echo ""
echo "🔧 Setting up pre-commit hooks..."
pip install pre-commit
pre-commit install

# Generate secrets baseline
echo ""
echo "🔐 Generating secrets baseline..."
detect-secrets scan > .secrets.baseline

# Run initial checks
echo ""
echo "🔍 Running initial code quality checks..."
black --check src/ tests/ || true
isort --check src/ tests/ || true
flake8 src/ tests/ || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo ""
echo "1. Pre-commit hooks:"
echo "   - Hooks are installed and will run on every commit"
echo "   - Test manually: make precommit-run"
echo ""
echo "2. Security scanning:"
echo "   - Run: make security-scan"
echo "   - Check vulnerabilities: make vulnerability-check"
echo ""
echo "3. W&B Setup:"
echo "   - Run: make wandb-setup"
echo "   - Train: make train-wandb"
echo ""
echo "4. Docker:"
echo "   - Build optimized: make docker-build-optimized"
echo "   - Run stack: make docker-compose-up"
echo ""
echo "5. Kubernetes:"
echo "   - Deploy: make k8s-deploy"
echo "   - Status: make k8s-status"
echo ""
echo "📖 Full documentation: AUTOMATION_GUIDE.md"
echo "💡 Available commands: make help"
