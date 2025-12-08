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
	python src/training/train.py

train-fast:  ## Quick training for testing
	python src/training/train.py hyperparameters=fast hyperparameters.num_epochs=2

train-resnet:  ## Train ResNet model
	python src/training/train.py model=resnet

train-mnist:  ## Train on MNIST dataset
	python src/training/train.py data=mnist

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
