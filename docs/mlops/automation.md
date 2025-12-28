# MLOps Automation Guide

This comprehensive guide covers all automation features implemented in the project.

## 📋 Overview

The project includes complete automation for:

1. ✅ **Pre-commit hooks** - Auto format and quality checks
2. 🔒 **Security scanning** - Bandit for vulnerability detection
3. 🛡️ **Dependency checking** - Safety and pip-audit
4. 🐳 **Docker optimization** - Multi-stage production builds
5. ☸️ **Kubernetes deployment** - Production-ready manifests
6. 📊 **W&B Tracking** - Weights, biases, and experiment tracking

## 🚀 Quick Start (3 Minutes)

### 1. Setup Environment (1 minute)
```bash
# Run automated setup script
./scripts/quickstart.sh
```

### 2. Install Pre-commit Hooks (30 seconds)
```bash
make setup-precommit
```

### 3. Setup W&B (1 minute)
```bash
make wandb-setup
# Enter API key from: https://wandb.ai/authorize
```

### 4. Start Training! (30 seconds to start)
```bash
# Train with W&B tracking
make train-wandb

# Or quick test training
make train-fast
```

## 💡 Common Commands

### Development
```bash
make format              # Format code
make lint                # Check linting
make test                # Run tests
make quality-check       # All quality checks
```

### Security
```bash
make security-scan       # Scan code
make vulnerability-check # Check dependencies
make security-all        # All security checks
```

### Training
```bash
make train-wandb         # Train with W&B
make train-wandb-offline # W&B offline mode
make train-both          # MLflow + W&B
```

### Docker
```bash
make docker-build-optimized  # Build optimized image
make docker-compose-up       # Start full stack
make docker-compose-down     # Stop stack
```

### Kubernetes
```bash
make k8s-deploy          # Deploy to K8s
make k8s-status          # Check status
make k8s-logs            # View logs
make k8s-port-forward    # Port forward to localhost
```

### View All Commands
```bash
make help                # List all available commands
```

## ✅ 1. Pre-commit Hooks & Auto-formatting

### Features
- 🎨 Auto-format code with Black
- 📦 Auto-sort imports with isort
- 🔍 Linting with flake8
- 🔒 Security scan with Bandit
- 📝 Type checking with mypy
- 🔐 Secret detection
- 🛡️ Dependency safety checks
- 🐳 Dockerfile linting with hadolint

### Installation
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### Files
- `.pre-commit-config.yaml` - Hook configuration
- `pyproject.toml` - Tool configurations
- `.secrets.baseline` - Baseline for secret detection

### Hooks Included
- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting with docstring checks
- **Bandit** - Security scanning
- **mypy** - Type checking
- **detect-secrets** - Secret detection
- **Safety** - Dependency security
- **hadolint** - Dockerfile linting
- **YAML formatter** - YAML file formatting

## 🔒 2. Security Scanning with Bandit

### Features
- Automatic code security vulnerability scanning
- JSON and text report generation
- Integrated into pre-commit hooks
- Integrated into CI/CD pipeline

### Usage
```bash
# Run security scan
make security-scan

# Or run script directly
./scripts/security_scan.sh
```

### Configuration
Security configuration is in `pyproject.toml`:

```toml
[tool.bandit]
exclude_dirs = ["tests", "venv", ".venv"]
tests = ["B201", "B301"]
skips = ["B101", "B601"]
```

### Reports
- `reports/bandit-report.json` - JSON format
- Console output with detailed findings

## 🛡️ 3. Dependency Vulnerability Checking

### Tools
- **Safety** - Check Python packages for known vulnerabilities
- **pip-audit** - Comprehensive dependency scanning
- **Trivy** - Docker image scanning (optional)

### Usage
```bash
# Check all vulnerabilities
make vulnerability-check

# Or run script directly
./scripts/check_vulnerabilities.sh
```

### Reports
- `reports/safety-report.json` - Safety scan results
- `reports/pip-audit-report.json` - pip-audit results

## 🐳 4. Docker Optimization

### Features
- Multi-stage build (reduced image size)
- Non-root user (enhanced security)
- Health checks
- Complete stack with monitoring

### Build Optimized Image
```bash
# Build optimized Docker image
make docker-build-optimized

# Compare with standard image
make docker-size-compare
```

### Docker Compose Stack
The `docker-compose.yml` includes:
- **App** - Main application (port 8000)
- **MLflow** - Experiment tracking (port 5000)
- **Prometheus** - Metrics collection (port 9090)
- **Grafana** - Monitoring dashboard (port 3000)

```bash
# Start full stack
make docker-compose-up

# Stop stack
make docker-compose-down
```

### Access Services
- App: http://localhost:8000
- MLflow: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## ☸️ 5. Kubernetes Deployment

### Production-Ready Manifests
- `k8s/namespace.yaml` - Isolated namespace
- `k8s/deployment.yaml` - Application deployment
- `k8s/service.yaml` - LoadBalancer service
- `k8s/hpa.yaml` - Horizontal auto-scaling (2-10 pods)
- `k8s/ingress.yaml` - HTTPS ingress
- `k8s/configmap.yaml` - Configuration
- `k8s/secrets.yaml` - Sensitive data
- `k8s/pvc.yaml` - Persistent storage
- `k8s/monitoring/prometheus.yml` - Monitoring config

### Deploy to Kubernetes
```bash
# Deploy all manifests
make k8s-deploy

# Or use script
./scripts/deploy_k8s.sh
```

### Manage Deployment
```bash
# Check status
make k8s-status

# View logs
make k8s-logs

# Port forward for local access
make k8s-port-forward

# Delete deployment
make k8s-delete
```

### Features
- **Auto-scaling**: 2-10 pods based on CPU/memory
- **Health checks**: Liveness and readiness probes
- **Resource limits**: CPU and memory constraints
- **Persistent storage**: 10Gi volume
- **HTTPS**: Ingress with TLS support
- **Monitoring**: Prometheus metrics

## 📊 6. Weights & Biases Tracking

### Features
- Experiment tracking
- Model versioning
- Weight and bias histogram logging
- Gradient tracking
- Model artifact storage
- Hyperparameter tuning with sweeps

### Setup
```bash
# Install W&B
pip install wandb

# Login
wandb login

# Or use setup script
./scripts/setup_wandb.sh
```

### Training with W&B
```bash
# Basic training
python src/training/train.py tracking=wandb

# With both MLflow and W&B
python src/training/train.py tracking=wandb tracking.backend=both

# Offline mode (no internet required)
WANDB_MODE=offline python src/training/train.py tracking=wandb
```

### Configuration
Edit `configs/tracking/wandb.yaml`:

```yaml
project: image-classifier
entity: your-username
log_model: true
log_code: true
log_weights_frequency: 10  # Log weights every 10 epochs
log_gradients: true
```

### Hyperparameter Sweeps
```bash
# Run hyperparameter sweep
python scripts/wandb_sweep.py

# Run multiple agents
wandb agent SWEEP_ID --count 5
```

### What Gets Logged
- Training/validation metrics
- Model architecture
- Hyperparameters
- Weight histograms (every 10 epochs)
- Bias histograms
- Gradient distributions
- Model checkpoints
- Code version
- System metrics

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
File: `.github/workflows/code-quality.yml`

### Jobs
1. **Code Quality** - Black, isort, flake8
2. **Security** - Bandit, Safety
3. **Type Checking** - mypy
4. **Testing** - pytest with coverage

### Triggers
- Push to main branch
- Pull requests
- Manual dispatch

### Configuration
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

## 📚 Additional Documentation

### Files Created
- `START_HERE.md` - Quick start guide
- `AUTOMATION_GUIDE.md` - Detailed automation guide
- `QUICK_REFERENCE.md` - Command reference
- `CHECKLIST.md` - Feature checklist
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `MLOPS_AUTOMATION_GUIDE.md` - Comprehensive merged guide

### Reference Order
1. **START_HERE.md** - Begin here for quick start
2. **QUICK_REFERENCE.md** - Commands and usage
3. **AUTOMATION_GUIDE.md** - Detailed instructions
4. **IMPLEMENTATION_SUMMARY.md** - What was implemented

## 🛠️ Troubleshooting

### Pre-commit Hooks Failing
```bash
# Update hooks
pre-commit autoupdate

# Clear cache
pre-commit clean

# Reinstall
pre-commit uninstall
pre-commit install
```

### W&B Login Issues
```bash
# Login with API key
wandb login YOUR_API_KEY

# Or set environment variable
export WANDB_API_KEY=YOUR_API_KEY
```

### Kubernetes Issues
```bash
# Check pods
kubectl get pods -n mlops-image-classifier

# Describe pod
kubectl describe pod POD_NAME -n mlops-image-classifier

# View logs
kubectl logs POD_NAME -n mlops-image-classifier
```

### Docker Build Issues
```bash
# Clear cache
docker builder prune

# Build without cache
docker build --no-cache -f Dockerfile.optimized -t image-classifier:latest .
```

## 📈 Best Practices

### Code Quality
- Run `make format` before committing
- Fix all linting errors shown by `make lint`
- Keep test coverage above 80%

### Security
- Run security scans regularly
- Update dependencies frequently
- Never commit secrets (use .env files)

### Training
- Always use experiment tracking
- Log hyperparameters and metrics
- Save model artifacts

### Deployment
- Test locally with Docker first
- Use environment-specific configs
- Monitor resource usage

## 🎯 Next Steps

After completing the quick start:

1. **Explore the codebase** - Understand project structure
2. **Run experiments** - Try different configurations
3. **Monitor metrics** - Use W&B and MLflow
4. **Deploy to production** - Use Kubernetes manifests
5. **Set up CI/CD** - Configure GitHub Actions
6. **Contribute** - Follow development guidelines

## 📞 Support

For issues and questions:
- Check documentation files
- Review error messages carefully
- Use `make help` for available commands
- Check logs in `reports/` directory

## 🔗 Useful Links

- [Weights & Biases Documentation](https://docs.wandb.ai/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Pre-commit Documentation](https://pre-commit.com/)
