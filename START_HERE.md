# 🚀 BẮT ĐẦU TẠI ĐÂY!

## Chào mừng bạn đến với dự án MLOps Image Classifier với Automation đầy đủ!

### 📋 Đã triển khai:
✅ Pre-commit hooks (tự động format code)
✅ Security scanning (Bandit)
✅ Vulnerability checking (Safety, pip-audit)
✅ Docker optimization (multi-stage)
✅ Kubernetes deployment (production-ready)
✅ W&B tracking (weights, biases, gradients)
✅ CI/CD pipeline (GitHub Actions)

---

## 🎯 Bắt Đầu Nhanh (3 Phút)

### 1. Setup môi trường (1 phút)
```bash
# Chạy script tự động setup
./scripts/quickstart.sh
```

### 2. Cài đặt pre-commit hooks (30 giây)
```bash
make setup-precommit
```

### 3. Setup W&B (1 phút)
```bash
make wandb-setup
# Nhập API key từ: https://wandb.ai/authorize
```

### 4. Train ngay! (30 giây để start)
```bash
# Train với W&B tracking
make train-wandb

# Hoặc train nhanh để test
make train-fast
```

---

## 📚 Tài Liệu

### Đọc theo thứ tự:
1. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Tổng quan những gì đã triển khai
2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Commands và cách sử dụng nhanh
3. **[AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)** - Hướng dẫn chi tiết đầy đủ

### Tham khảo thêm:
- **[CHECKLIST.md](CHECKLIST.md)** - Checklist đầy đủ các tính năng

---

## 💡 Commands Hay Dùng

### Development:
```bash
make format              # Format code
make lint                # Check linting
make test                # Run tests
make quality-check       # All quality checks
```

### Security:
```bash
make security-scan       # Quét bảo mật
make vulnerability-check # Check dependencies
make security-all        # Tất cả security checks
```

### Training:
```bash
make train-wandb         # Train với W&B
make train-wandb-offline # W&B offline mode
make train-both          # MLflow + W&B
```

### Docker:
```bash
make docker-build-optimized  # Build optimized image
make docker-compose-up       # Start full stack
make docker-compose-down     # Stop stack
```

### Kubernetes:
```bash
make k8s-deploy          # Deploy to K8s
make k8s-status          # Check status
make k8s-logs            # View logs
make k8s-port-forward    # Port forward to localhost
```

### Xem tất cả:
```bash
make help                # List all commands
```

---

## 🔥 Demo Nhanh

### 1. Test Pre-commit Hooks:
```bash
make precommit-run
# Sẽ tự động format, lint, check security
```

### 2. Security Scan:
```bash
make security-all
# Reports trong folder reports/
```

### 3. Train với W&B:
```bash
make train-wandb
# Xem kết quả tại https://wandb.ai
```

### 4. Deploy Local Stack:
```bash
make deploy-local
# Truy cập:
# - App: http://localhost:8000
# - MLflow: http://localhost:5000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
```

---

## 🎓 Workflow Khuyến Nghị

### Hàng ngày:
1. Code như bình thường
2. Commit - pre-commit hooks tự động chạy
3. Push - CI/CD tự động test và scan

### Hàng tuần:
1. `make security-all` - Check security
2. `make vulnerability-check` - Check dependencies

### Khi train model:
1. `make train-wandb` - Track everything
2. Xem results trên W&B dashboard
3. Download best model từ W&B artifacts

### Khi deploy:
1. Local: `make deploy-local`
2. K8s: Build image → Push → `make k8s-deploy`

---

## 🆘 Gặp Vấn Đề?

### Pre-commit không chạy:
```bash
pre-commit clean
pre-commit install
```

### W&B login issues:
```bash
export WANDB_MODE=offline  # Offline mode
wandb login                 # Login lại
```

### Docker build chậm:
```bash
docker builder prune -af   # Clean cache
```

### Xem help:
```bash
make help                  # All commands
```

---

## 📖 Đọc Thêm

- [Pre-commit hooks](https://pre-commit.com/)
- [Bandit security](https://bandit.readthedocs.io/)
- [W&B documentation](https://docs.wandb.ai/)
- [Kubernetes docs](https://kubernetes.io/docs/)

---

## 🎉 Let's Go!

```bash
# Setup everything in one go
make setup-all

# Or start step by step
./scripts/quickstart.sh
```

**Happy coding! 🚀**
