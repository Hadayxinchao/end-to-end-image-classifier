# 🚀 Automation Features - Quick Reference

## Tính năng đã triển khai

### ✅ 1. Pre-commit Hooks & Auto-formatting
**Files:**
- `.pre-commit-config.yaml` - Cấu hình hooks
- `pyproject.toml` - Config cho Black, isort, Bandit, coverage

**Sử dụng:**
```bash
make setup-precommit    # Install hooks
make precommit-run      # Run on all files
git commit -m "..."     # Auto-run on commit
```

**Hooks bao gồm:**
- ✅ Black (code formatting)
- ✅ isort (import sorting)
- ✅ flake8 (linting)
- ✅ Bandit (security)
- ✅ mypy (type checking)
- ✅ detect-secrets (secret detection)
- ✅ Safety (dependency security)

---

### 🔒 2. Security Scanning với Bandit
**Files:**
- `scripts/security_scan.sh` - Script quét bảo mật
- `pyproject.toml` - Bandit config

**Sử dụng:**
```bash
make security-scan              # Quét code
./scripts/security_scan.sh      # Trực tiếp
```

**Reports:** `reports/bandit-report.json`

---

### 🛡️ 3. Dependency Vulnerability Checking
**Files:**
- `scripts/check_vulnerabilities.sh` - Script kiểm tra

**Sử dụng:**
```bash
make vulnerability-check              # Kiểm tra lỗ hổng
./scripts/check_vulnerabilities.sh    # Trực tiếp
```

**Tools sử dụng:**
- Safety (Python packages)
- pip-audit (alternative scanner)
- Trivy (Docker images - optional)

**Reports:** `reports/safety-report.json`, `reports/pip-audit-report.json`

---

### 🐳 4. Docker Optimization
**Files:**
- `Dockerfile.optimized` - Multi-stage optimized
- `docker-compose.yml` - Local stack với monitoring

**Sử dụng:**
```bash
# Build
make docker-build-optimized

# Compare sizes
make docker-size-compare

# Run full stack
make docker-compose-up
```

**Tính năng:**
- Multi-stage build (giảm size)
- Non-root user (security)
- Health checks
- Với MLflow, Prometheus, Grafana

**Services:**
- App: http://localhost:8000
- MLflow: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

---

### ☸️ 5. Kubernetes Deployment
**Files:**
- `k8s/namespace.yaml` - Namespace
- `k8s/deployment.yaml` - Deployment config
- `k8s/service.yaml` - Service
- `k8s/hpa.yaml` - Auto-scaling
- `k8s/ingress.yaml` - HTTPS ingress
- `k8s/configmap.yaml` - Configuration
- `k8s/secrets.yaml` - Secrets
- `scripts/deploy_k8s.sh` - Deploy script

**Sử dụng:**
```bash
# Deploy
make k8s-deploy

# Status
make k8s-status
make k8s-hpa-status

# Logs
make k8s-logs

# Port forward
make k8s-port-forward

# Scale
make k8s-scale REPLICAS=5

# Delete
make k8s-delete
```

**Features:**
- 3 replicas với rolling updates
- Auto-scaling (2-10 pods)
- Load balancer
- Persistent storage
- Health checks
- Prometheus metrics

---

### 📊 6. W&B Tracking (Weights & Biases)
**Files:**
- `src/utils/wandb_tracker.py` - W&B tracker class
- `configs/tracking/wandb.yaml` - W&B config
- `scripts/setup_wandb.sh` - Setup script

**Sử dụng:**
```bash
# Setup
make wandb-setup
make wandb-login

# Train
make train-wandb                # Online
make train-wandb-offline        # Offline
make train-both                 # MLflow + W&B
```

**Tự động log:**
- ✅ Model architecture
- ✅ Hyperparameters
- ✅ Training/validation metrics
- ✅ **Weight histograms** (every 10 epochs)
- ✅ **Bias histograms**
- ✅ **Gradient statistics**
- ✅ Learning rate schedule
- ✅ Model checkpoints với metadata
- ✅ Confusion matrix
- ✅ Training history plots

**View results:** https://wandb.ai

---

### 🔄 7. CI/CD Pipeline
**Files:**
- `.github/workflows/code-quality.yml` - GitHub Actions

**Tự động chạy khi:**
- Push to main/develop
- Pull request
- Weekly (security scans)

**Jobs:**
1. **code-quality** - Lint, format, type check
2. **security-scan** - Bandit, Safety, CodeQL
3. **test** - Unit tests với coverage
4. **docker-security** - Trivy scanning

---

## Quick Commands

### Setup
```bash
./scripts/quickstart.sh    # One-time setup
make setup-all             # Complete setup
```

### Development
```bash
make format                # Format code
make lint                  # Lint check
make test                  # Run tests
make quality-check         # All checks
```

### Security
```bash
make security-all          # All security checks
```

### Training
```bash
make train-wandb           # Train với W&B
```

### Deployment
```bash
make deploy-local          # Docker stack
make deploy-k8s            # Kubernetes
```

### All Commands
```bash
make help                  # List all commands
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `pyproject.toml` | Tool configs (Black, isort, Bandit, etc) |
| `Dockerfile.optimized` | Production Docker image |
| `docker-compose.yml` | Local development stack |
| `k8s/*.yaml` | Kubernetes manifests |
| `configs/tracking/wandb.yaml` | W&B settings |
| `.github/workflows/code-quality.yml` | CI/CD pipeline |

---

## Troubleshooting

### Pre-commit fails
```bash
pre-commit clean
pre-commit install
```

### W&B offline
```bash
export WANDB_MODE=offline
```

### Docker build slow
```bash
docker builder prune -af
```

### K8s pod not starting
```bash
kubectl describe pod <pod-name> -n mlops-image-classifier
kubectl logs <pod-name> -n mlops-image-classifier
```

---

## Documentation

📖 **Chi tiết:** [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)
