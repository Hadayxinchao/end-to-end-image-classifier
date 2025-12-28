# Hướng Dẫn Tự Động Hóa Chất Lượng Code và Deployment

## 📋 Tổng Quan

Dự án này đã được trang bị đầy đủ các công cụ tự động hóa chất lượng code và deployment:

1. ✅ **Pre-commit hooks** - Tự động format và kiểm tra code
2. 🔒 **Security scanning** - Quét lỗ hổng bảo mật với Bandit
3. 🛡️ **Dependency checking** - Kiểm tra lỗ hổng trong dependencies
4. 🐳 **Docker optimization** - Container tối ưu hóa cho production
5. ☸️ **Kubernetes deployment** - Triển khai lên K8s cluster
6. 📊 **W&B Tracking** - Theo dõi weights, biases và experiments

## 🚀 Cài Đặt Nhanh

### 1. Cài Đặt Pre-commit Hooks

```bash
# Cài đặt pre-commit
pip install pre-commit

# Cài đặt hooks
pre-commit install

# Chạy thử trên tất cả files
pre-commit run --all-files
```

Từ giờ, mỗi khi bạn commit code, các hooks sẽ tự động:
- Format code với Black
- Sắp xếp imports với isort
- Kiểm tra lỗi với flake8
- Quét bảo mật với Bandit
- Kiểm tra type với mypy
- Detect secrets và lỗ hổng bảo mật

### 2. Quét Bảo Mật

```bash
# Quét code với Bandit
./scripts/security_scan.sh

# Kiểm tra lỗ hổng dependencies
./scripts/check_vulnerabilities.sh
```

### 3. Setup Weights & Biases

```bash
# Setup W&B
./scripts/setup_wandb.sh

# Hoặc login thủ công
wandb login

# Đặt API key (option)
export WANDB_API_KEY=your-api-key
```

### 4. Docker Build & Run

```bash
# Build Docker image (optimized)
docker build -f Dockerfile.optimized -t image-classifier:latest .

# Run container
docker run -p 8000:8000 image-classifier:latest

# Hoặc dùng docker-compose (với MLflow, Prometheus, Grafana)
docker-compose up -d
```

### 5. Deploy lên Kubernetes

```bash
# Cập nhật image registry trong k8s/deployment.yaml
# Sau đó deploy
./scripts/deploy_k8s.sh

# Xem status
kubectl get all -n mlops-image-classifier

# Port-forward để test
kubectl port-forward service/image-classifier-service 8000:80 -n mlops-image-classifier
```

## 📊 W&B Tracking - Theo Dõi Weights & Biases

### Training với W&B

```bash
# Train với W&B tracking (default)
python src/training/train.py tracking=wandb

# Train với cả MLflow và W&B
python src/training/train.py tracking=wandb tracking.backend=both

# Offline mode (không cần internet)
WANDB_MODE=offline python src/training/train.py tracking=wandb
```

### Các Tính Năng W&B

✅ **Tự động log:**
- Model architecture
- Hyperparameters
- Training/validation metrics
- Learning rate schedule
- **Weight và bias histograms** (mỗi 10 epochs)
- **Gradient histograms**
- Model checkpoints với metadata
- Confusion matrix và reports

✅ **Model versioning:**
- Best model tự động được log với tag "best"
- Checkpoints có metadata đầy đủ
- Download models từ W&B artifacts

### Xem Kết Quả

```bash
# Mở W&B dashboard
wandb board

# Hoặc truy cập: https://wandb.ai/<your-username>/image-classifier
```

## 🔄 CI/CD Pipeline

GitHub Actions workflow tự động chạy khi push code:

### Code Quality Checks
- ✅ Format checking (Black, isort)
- ✅ Linting (flake8)
- ✅ Type checking (mypy)
- ✅ Pre-commit hooks validation

### Security Scans
- 🔒 Bandit code security scan
- 🛡️ Safety dependency vulnerability check
- 🔍 pip-audit
- 📋 CodeQL analysis
- 🐳 Trivy Docker image scanning

### Testing
- 🧪 Unit tests với pytest
- 📊 Coverage reports (upload to Codecov)
- 📈 Test results artifacts

## 🐳 Docker Optimization

### Multi-stage Build

File `Dockerfile.optimized` sử dụng multi-stage build để:
- Giảm image size
- Tách build dependencies khỏi runtime
- Chạy với non-root user (security)
- Health checks tự động

### Size Comparison

```bash
# Build thông thường
docker build -t image-classifier:normal -f Dockerfile .

# Build optimized
docker build -t image-classifier:optimized -f Dockerfile.optimized .

# So sánh size
docker images | grep image-classifier
```

## ☸️ Kubernetes Deployment

### Components

- **Deployment**: 3 replicas với rolling updates
- **Service**: LoadBalancer với session affinity
- **HPA**: Auto-scaling từ 2-10 pods
- **ConfigMap**: Configuration management
- **Secrets**: API keys và credentials
- **PVC**: Persistent storage cho models
- **Ingress**: HTTPS với Let's Encrypt

### Monitoring

Stack bao gồm:
- Prometheus (metrics collection)
- Grafana (visualization)
- Custom metrics từ application

### Commands

```bash
# Apply all manifests
kubectl apply -f k8s/

# Scale deployment
kubectl scale deployment image-classifier --replicas=5 -n mlops-image-classifier

# Check HPA
kubectl get hpa -n mlops-image-classifier

# View logs
kubectl logs -f deployment/image-classifier -n mlops-image-classifier

# Delete deployment
kubectl delete -f k8s/
```

## 📝 Configuration Files

### Pre-commit Configuration
- `.pre-commit-config.yaml` - Pre-commit hooks config

### Security Configuration
- `pyproject.toml` - Bandit, isort, coverage config
- `.secrets.baseline` - Detect-secrets baseline

### Tracking Configuration
- `configs/tracking/wandb.yaml` - W&B settings
- `configs/tracking/mlflow.yaml` - MLflow settings

### Docker/K8s Configuration
- `Dockerfile.optimized` - Optimized production Dockerfile
- `docker-compose.yml` - Local development stack
- `k8s/*.yaml` - Kubernetes manifests

## 🛠️ Development Workflow

### 1. Trước khi Commit

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/

# Security scan
bandit -r src/
```

Pre-commit hooks sẽ tự động chạy các bước này!

### 2. Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Security checks
./scripts/security_scan.sh
./scripts/check_vulnerabilities.sh
```

### 3. Training

```bash
# Local training với W&B
python src/training/train.py tracking=wandb

# Hyperparameter sweep với W&B
wandb sweep configs/sweep.yaml
wandb agent <sweep-id>
```

### 4. Build & Deploy

```bash
# Build Docker
docker build -f Dockerfile.optimized -t your-registry/image-classifier:v1.0 .

# Push to registry
docker push your-registry/image-classifier:v1.0

# Deploy to K8s
./scripts/deploy_k8s.sh v1.0
```

## 📊 Monitoring & Observability

### Application Metrics

```python
# Metrics được tự động log vào W&B:
- Training loss & accuracy
- Validation loss & accuracy
- Learning rate schedule
- Weight histograms (every 10 epochs)
- Gradient statistics
- Model parameters count
```

### Infrastructure Metrics

- Prometheus scrapes metrics từ pods
- Grafana dashboards cho visualization
- HPA metrics cho auto-scaling

## 🔐 Security Best Practices

✅ **Đã implement:**
- Non-root user trong Docker
- Multi-stage builds
- Secrets management với K8s secrets
- Security scanning trong CI/CD
- Dependency vulnerability checks
- Code security với Bandit
- No hardcoded secrets (detect-secrets)

## 📚 Tài Liệu Bổ Sung

- [Pre-commit hooks documentation](https://pre-commit.com/)
- [Bandit documentation](https://bandit.readthedocs.io/)
- [W&B documentation](https://docs.wandb.ai/)
- [Kubernetes documentation](https://kubernetes.io/docs/)

## 🆘 Troubleshooting

### Pre-commit Issues

```bash
# Clear pre-commit cache
pre-commit clean

# Reinstall hooks
pre-commit uninstall
pre-commit install

# Skip hooks (not recommended)
git commit --no-verify
```

### W&B Issues

```bash
# Check W&B status
wandb status

# Offline mode
export WANDB_MODE=offline

# Disable W&B
python src/training/train.py tracking.enabled=false
```

### Docker Issues

```bash
# Clean build cache
docker builder prune -af

# Remove unused images
docker image prune -a

# Check logs
docker logs <container-id>
```

### K8s Issues

```bash
# Check pod status
kubectl describe pod <pod-name> -n mlops-image-classifier

# View events
kubectl get events -n mlops-image-classifier --sort-by='.lastTimestamp'

# Debug pod
kubectl exec -it <pod-name> -n mlops-image-classifier -- /bin/bash
```

## 🎉 Kết Luận

Dự án của bạn giờ đã có:
- ✅ Tự động format code và quality checks
- ✅ Security scanning tự động
- ✅ Dependency vulnerability monitoring
- ✅ Docker images tối ưu
- ✅ K8s deployment với auto-scaling
- ✅ Complete W&B tracking cho weights/biases
- ✅ CI/CD pipeline đầy đủ

Happy coding! 🚀
