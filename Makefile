.PHONY: help install test lint format clean train docker docs

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

test:  ## Run tests
	pytest tests/ -v -m "not slow"

test-all:  ## Run all tests including slow ones
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:  ## Run linters
	flake8 src tests
	black --check src tests
	isort --check-only src tests
	mypy src --ignore-missing-imports

format:  ## Format code
	black src tests
	isort src tests

clean:  ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/ .coverage htmlcov/
	rm -rf outputs/ multirun/

train:  ## Train model with default config
	python -m src.training.train

train-fast:  ## Quick training for testing
	python -m src.training.train hyperparameters=fast hyperparameters.num_epochs=2

train-resnet:  ## Train ResNet model
	python -m src.training.train model=resnet

train-mnist:  ## Train on MNIST dataset
	python -m src.training.train data=mnist

docker-build:  ## Build Docker image
	docker build -t image-classifier:latest .

docker-run:  ## Run Docker container
	docker run --rm \
		-v $$(pwd)/models:/app/models \
		-v $$(pwd)/reports:/app/reports \
		image-classifier:latest

docker-test:  ## Run tests in Docker
	docker run --rm image-classifier:latest pytest tests/ -m "not slow"

docker-shell:  ## Open shell in Docker container
	docker run --rm -it image-classifier:latest /bin/bash

docs-serve:  ## Serve documentation locally
	mkdocs serve

docs-build:  ## Build documentation
	mkdocs build

docs-deploy:  ## Deploy documentation to GitHub Pages
	mkdocs gh-deploy

dvc-init:  ## Initialize DVC
	dvc init
	git add .dvc .dvcignore
	git commit -m "Initialize DVC"

dvc-add-data:  ## Track data with DVC
	dvc add data/raw
	git add data/raw.dvc data/.gitignore
	git commit -m "Track data with DVC"

dvc-push:  ## Push data to DVC remote
	dvc push

dvc-pull:  ## Pull data from DVC remote
	dvc pull

setup-env:  ## Setup development environment
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  (Linux/Mac)"
	@echo "  venv\\Scripts\\activate     (Windows)"

check:  ## Run all checks (lint + test)
	@echo "Running linters..."
	@make lint
	@echo "\nRunning tests..."
	@make test
	@echo "\n✅ All checks passed!"

all: clean install lint test  ## Clean, install, lint, and test

ci:  ## Simulate CI pipeline
	@echo "=== Running CI Pipeline ==="
	@echo "\n1. Installing dependencies..."
	@make install
	@echo "\n2. Running linters..."
	@make lint
	@echo "\n3. Running tests..."
	@make test
	@echo "\n4. Quick training..."
	@make train-fast
	@echo "\n✅ CI Pipeline completed!"

# ============================================================================
# Quality & Security Automation
# ============================================================================

setup-precommit:  ## Install and setup pre-commit hooks
	pip install pre-commit
	pre-commit install
	@echo "✅ Pre-commit hooks installed!"

precommit-run:  ## Run pre-commit on all files
	pre-commit run --all-files

precommit-update:  ## Update pre-commit hooks
	pre-commit autoupdate

security-scan:  ## Run security scans (Bandit)
	./scripts/security_scan.sh

vulnerability-check:  ## Check dependency vulnerabilities
	./scripts/check_vulnerabilities.sh

security-all:  ## Run all security checks
	@echo "Running security scans..."
	@make security-scan
	@echo "\nChecking vulnerabilities..."
	@make vulnerability-check
	@echo "\n✅ Security checks complete!"

# ============================================================================
# W&B Integration
# ============================================================================

wandb-setup:  ## Setup Weights & Biases
	./scripts/setup_wandb.sh

wandb-login:  ## Login to W&B
	wandb login

train-wandb:  ## Train with W&B tracking
	python -m src.training.train tracking=wandb

train-wandb-offline:  ## Train with W&B offline mode
	WANDB_MODE=offline python -m src.training.train tracking=wandb

train-both:  ## Train with both MLflow and W&B
	python -m src.training.train tracking=wandb tracking.backend=both

# ============================================================================
# Docker Optimization
# ============================================================================

docker-build-optimized:  ## Build optimized Docker image
	docker build -f Dockerfile.optimized -t image-classifier:optimized .

docker-size-compare:  ## Compare Docker image sizes
	@echo "Building normal image..."
	@docker build -t image-classifier:normal -f Dockerfile . -q
	@echo "Building optimized image..."
	@docker build -t image-classifier:optimized -f Dockerfile.optimized . -q
	@echo "\nImage sizes:"
	@docker images | grep image-classifier

docker-compose-up:  ## Start all services with docker-compose
	docker-compose up -d

docker-compose-down:  ## Stop all services
	docker-compose down

docker-compose-logs:  ## View docker-compose logs
	docker-compose logs -f

docker-security-scan:  ## Scan Docker image with Trivy (if installed)
	@if command -v trivy >/dev/null 2>&1; then \
		trivy image image-classifier:optimized; \
	else \
		echo "Trivy not installed. Install from: https://github.com/aquasecurity/trivy"; \
	fi

# ============================================================================
# Complete Automation Workflow
# ============================================================================

setup-all:  ## Complete setup (pre-commit, W&B, dependencies)
	@echo "🚀 Setting up complete automation stack..."
	@echo "\n1. Installing dependencies..."
	@make install
	@echo "\n2. Setting up pre-commit hooks..."
	@make setup-precommit
	@echo "\n3. Setting up W&B..."
	@make wandb-setup
	@echo "\n✅ Setup complete!"

quality-check:  ## Run all quality checks
	@echo "🔍 Running quality checks..."
	@make lint
	@make test-cov
	@echo "\n✅ Quality checks complete!"

deploy-local:  ## Full local deployment with monitoring
	@echo "🐳 Deploying local stack..."
	@make docker-build-optimized
	@make docker-compose-up
	@echo "\n✅ Local stack deployed!"
	@echo "\nServices:"
	@echo "  - App: http://localhost:8000"
	@echo "  - MLflow: http://localhost:5000"
	@echo "  - Prometheus: http://localhost:9090"
	@echo "  - Grafana: http://localhost:3000"
