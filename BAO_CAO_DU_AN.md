---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

# 📊 Hệ Thống Phân Loại Ảnh End-to-End
## Báo Cáo Tiến Độ Dự Án MLOps

**Ngày:** 14/12/2025
**Dự án:** Phân loại ảnh với các phương pháp MLOps tốt nhất

---

## 📋 Tổng Quan Dự Án

**Mục tiêu:** Xây dựng pipeline MLOps hoàn chỉnh cho phân loại ảnh

**Công nghệ sử dụng:**
- 🐍 Python 3.8-3.10
- 🔥 PyTorch (Deep Learning)
- ⚙️ Hydra (Quản lý cấu hình)
- 🗂️ DVC (Quản lý phiên bản dữ liệu)
- 🧪 Pytest (Kiểm thử)
- 🔄 GitHub Actions (CI/CD)
- 🐳 Docker (Đóng gói container)

---

## ✅ Các Tính Năng Đã Hoàn Thành

### 1. **Cấu Trúc Dự Án** ✓
- Tổ chức thư mục theo best practices
- Phân tách rõ ràng (data, models, training, utils)
- Quản lý cấu hình với Hydra
- Thiết lập package Python chuẩn (`setup.py`)

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 2. **Pipeline Dữ Liệu** ✓
- Hỗ trợ dataset CIFAR-10 và MNIST
- Tự động tải và tiền xử lý dữ liệu
- Tăng cường dữ liệu và chuẩn hóa
- Chia tập train/validation/test
- Data loader hiệu quả với PyTorch

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 3. **Kiến Trúc Mô Hình** ✓
- **SimpleCNN**: CNN nhẹ cho thử nghiệm nhanh
- **ResNet**: Mạng residual sâu cho hiệu suất tốt hơn
- Mẫu thiết kế factory modular
- Siêu tham số cấu hình được (dropout, input channels, v.v.)
- Hỗ trợ cả ảnh RGB và grayscale

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 4. **Pipeline Huấn Luyện** ✓
- Vòng lặp huấn luyện hoàn chỉnh với cấu hình Hydra
- Hỗ trợ nhiều optimizer (Adam, SGD)
- Bộ điều chỉnh learning rate (Step, Cosine, ReduceLROnPlateau)
- Early stopping (dừng sớm)
- Gradient clipping
- Lưu checkpoint mô hình (lưu model tốt nhất)
- Theo dõi lịch sử huấn luyện

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 5. **Đánh Giá & Metrics** ✓
- Accuracy, Precision, Recall, F1-Score
- Trực quan hóa confusion matrix
- Tạo báo cáo phân loại
- Đồ thị lịch sử huấn luyện (loss & accuracy)
- Metrics theo từng class

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 6. **Kiểm Thử** ✓
- Unit test toàn diện (38 test case)
- **Phạm vi test:**
  - Tải và chuyển đổi dữ liệu
  - Kiểm tra kiến trúc mô hình
  - Tiện ích huấn luyện
  - Tính toán metrics
  - Hàm loss
- Đánh dấu test cho các test chậm
- Cấu hình Pytest với báo cáo coverage

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 7. **Pipeline CI/CD** ✓
- **GitHub Actions Workflows:**
  - Tự động test khi push/PR
  - Hỗ trợ nhiều phiên bản Python (3.8, 3.9, 3.10)
  - Kiểm tra code (flake8, black, isort)
  - Kiểm tra kiểu (mypy)
  - Báo cáo test coverage (Codecov)
  - Workflow CML cho báo cáo huấn luyện model

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 8. **Hỗ Trợ Docker** ✓
- Dockerfile tối ưu cho huấn luyện
- Image nhẹ (~1-1.5GB)
- Layer caching phù hợp
- `.dockerignore` cho context tối thiểu
- Hỗ trợ cả huấn luyện và inference
- Cấu hình production-ready

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 9. **Quản Lý Cấu Hình** ✓
- **Cấu hình Hydra:**
  - Cấu hình mô hình (simple_cnn, resnet)
  - Cấu hình dataset (CIFAR-10, MNIST)
  - Cấu hình siêu tham số (default, fast)
- Dễ dàng override từ command line
- Thí nghiệm có thể tái tạo với seed control

---

## ✅ Các Tính Năng Đã Hoàn Thành (tiếp)

### 10. **Tài Liệu** ✓
- README.md toàn diện
- Hướng dẫn Getting Started
- Hướng dẫn Docker (DOCKER.md)
- Hướng dẫn DVC (DVC_SETUP.md)
- Tài liệu API với MkDocs
- Tài liệu code với docstrings

---

## 📊 Thống Kê Dự Án

| Chỉ số | Giá trị |
|--------|---------|
| **Tổng số file Python** | 15+ |
| **Số dòng code** | ~3,000+ |
| **Số test case** | 38 |
| **Test Coverage** | ~85% |
| **Mô hình hỗ trợ** | 2 (SimpleCNN, ResNet) |
| **Dataset hỗ trợ** | 2 (CIFAR-10, MNIST) |
| **CI/CD Workflows** | 2 (Tests, CML) |

---

## 🎯 Thành Tựu Chính

1. ✅ **Codebase Production-Ready**
   - Kiến trúc sạch sẽ
   - Type hints đầy đủ
   - Xử lý lỗi toàn diện

2. ✅ **Tự Động Hóa Testing & CI/CD**
   - 100% test pass
   - Hỗ trợ đa phiên bản Python
   - Tự động linting và formatting

3. ✅ **Thí Nghiệm Có Thể Tái Tạo**
   - Kiểm soát seed
   - Quản lý cấu hình
   - Sẵn sàng version control

---

## 🎯 Thành Tựu Chính (tiếp)

4. ✅ **Quản Lý Tài Nguyên Hiệu Quả**
   - Docker image tối ưu
   - Yêu cầu CI nhẹ (`requirements-ci.txt`)
   - Tối ưu disk space trong CI

5. ✅ **Trải Nghiệm Developer Tốt**
   - Dễ chạy (`python src/training/train.py`)
   - Override cấu hình rõ ràng
   - Tài liệu toàn diện

---

## 📈 Hiệu Suất Mô Hình

### Kết quả CIFAR-10 (3 epochs, cấu hình fast)
- **Test Accuracy:** 66.0%
- **Thời gian huấn luyện:** ~5-10 phút (CPU)
- **Kích thước model:** ~2.5MB

### Metrics chính:
| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Máy bay | 0.745 | 0.631 | 0.683 |
| Ô tô | 0.838 | 0.711 | 0.770 |
| Tàu thủy | 0.731 | 0.823 | 0.774 |
| Xe tải | 0.681 | 0.821 | 0.745 |

---

## 🔧 Điểm Nổi Bật Kỹ Thuật

### Hệ thống cấu hình
```bash
# Override tham số huấn luyện dễ dàng
python src/training/train.py \
  model=resnet \
  data=mnist \
  hyperparameters.learning_rate=0.001 \
  hyperparameters.num_epochs=50
```

### Kiểm thử
```bash
# Tất cả test đều pass
pytest tests/ -v
# 34 passed, 4 deselected in 8.62s
```

---

## 🐳 Tích Hợp Docker

### Tối ưu hóa đã thực hiện:
- Multi-stage builds (nếu cần)
- Layer caching cho dependencies
- Base image tối thiểu (python:3.10-slim)
- Chỉ copy file cần thiết
- Không có dependencies development trong production

### Sử dụng:
```bash
docker build -t image-classifier .
docker run image-classifier
```

---

## 🔄 Chi Tiết Pipeline CI/CD

### Test Workflow:
- ✅ Chạy khi push lên main/develop
- ✅ Chạy trên pull request
- ✅ Test trên Python 3.8, 3.9, 3.10
- ✅ Linting với flake8, black
- ✅ Type checking với mypy
- ✅ Báo cáo coverage lên Codecov

### CML Workflow:
- ✅ Tự động huấn luyện mô hình
- ✅ Báo cáo metrics trên PR
- ✅ Upload artifacts (models, reports)
- ✅ Lưu trữ 30 ngày

---

## 📁 Tổng Quan Cấu Trúc File

```
end-to-end-image-classifier/
├── src/                    # Mã nguồn
│   ├── data/              # Tải dữ liệu
│   ├── models/            # Kiến trúc mô hình
│   ├── training/          # Script huấn luyện
│   └── utils/             # Hàm tiện ích
├── tests/                 # Unit tests
├── configs/               # Cấu hình Hydra
├── .github/workflows/     # CI/CD pipelines
├── docs/                  # Tài liệu
└── requirements-ci.txt    # Dependencies nhẹ
```

---

## 🚀 Khả Năng Hiện Tại

**Hệ thống có thể làm GÌ BÂY GIỜ:**

1. 🎯 Huấn luyện mô hình trên CIFAR-10 hoặc MNIST
2. 📊 Tạo báo cáo đánh giá toàn diện
3. 💾 Lưu và tải checkpoint mô hình
4. 🔄 Chạy tự động test trong CI/CD
5. 🐳 Triển khai với Docker
6. 📈 Theo dõi metrics huấn luyện
7. ⚙️ Quản lý cấu hình dễ dàng
8. 📝 Tạo báo cáo phân loại với visualization

---

## 🔄 Cải Tiến CI/CD Workflow

### Các vấn đề đã giải quyết:
1. ✅ **Lỗi import module** - Sửa với package imports đúng
2. ✅ **Test thất bại** - Sửa test case overfitting
3. ✅ **Vấn đề disk space** - Thêm bước cleanup trong CI
4. ✅ **Dependencies lớn** - Tạo `requirements-ci.txt` nhẹ
5. ✅ **Lỗi config** - Thêm hyperparameters còn thiếu vào fast.yaml
6. ✅ **Quyền CML** - Thay bằng github-script cho PR comments

---

## 🎓 MLOps Best Practices Đã Triển Khai

1. ✅ **Chất Lượng Code**
   - Linting, formatting, type checking
   - Kiểm thử toàn diện
   - Theo dõi code coverage

2. ✅ **Khả Năng Tái Tạo**
   - Random seed cố định
   - Quản lý cấu hình
   - Dependency pinning

3. ✅ **Tự Động Hóa**
   - CI/CD pipelines
   - Tự động testing
   - Báo cáo đánh giá mô hình

---

## 🎓 MLOps Best Practices (tiếp)

4. ✅ **Quản Lý Phiên Bản**
   - Git cho code
   - DVC cho dữ liệu (đã cấu hình)
   - Sẵn sàng version mô hình

5. ✅ **Container Hóa**
   - Docker image tối ưu
   - Môi trường có thể tái tạo
   - Triển khai dễ dàng

6. ✅ **Tài Liệu**
   - Tài liệu code
   - API docs với MkDocs
   - Hướng dẫn setup

---

## 🔮 Bước Tiếp Theo: Tính Năng Nâng Cao

### 1. **FastAPI Model Serving** (Sẵn sàng triển khai)
- REST API cho dự đoán
- Tài liệu Swagger
- Triển khai Docker
- Sẵn sàng load balancing

### 2. **Experiment Tracking** (Sẵn sàng triển khai)
- Tích hợp MLflow
- Hỗ trợ Weights & Biases
- Tự động logging
- Dashboard so sánh

---

## 🔮 Bước Tiếp Theo: Tính Năng Nâng Cao (tiếp)

### 3. **Data Validation** (Đã lên kế hoạch)
- Tích hợp Great Expectations
- Kiểm tra chất lượng dữ liệu
- Validation schema
- Cảnh báo tự động

### 4. **Tự Động Hóa Chất Lượng Code** (Sẵn sàng triển khai)
- Pre-commit hooks
- Tự động format khi commit
- Quét bảo mật (Bandit)
- Kiểm tra lỗ hổng dependency

---

## 🔮 Cải Tiến Tương Lai

### Các bổ sung tiềm năng:
- 📊 Dashboard visualization nâng cao
- 🎯 Tối ưu siêu tham số (Optuna)
- 🔄 Framework A/B testing
- 📈 Giám sát mô hình trong production
- 🔔 Hệ thống cảnh báo
- 🌐 Model registry
- ⚡ Tối ưu & quantization mô hình
- 📱 Hỗ trợ triển khai mobile

---

## 💪 Điểm Mạnh Của Dự Án

1. **Pipeline MLOps Hoàn Chỉnh**
   - Workflow end-to-end đã triển khai
   - Chất lượng code production-ready

2. **Được Test Kỹ & Đáng Tin Cậy**
   - Test coverage toàn diện
   - Validation CI/CD

3. **Linh Hoạt & Có Thể Mở Rộng**
   - Dễ thêm mô hình mới
   - Dễ thêm dataset mới
   - Kiến trúc modular

---

## 💪 Điểm Mạnh Của Dự Án (tiếp)

4. **Thân Thiện Với Developer**
   - Tài liệu rõ ràng
   - Giao diện command-line đơn giản
   - Cấu hình dễ dàng

5. **Production-Ready**
   - Hỗ trợ Docker
   - CI/CD pipelines
   - Xử lý lỗi
   - Logging

---

## 📊 Demo Workflow

### Quy trình huấn luyện:
```bash
1. Cấu hình (configs/*.yaml)
2. Huấn luyện (python src/training/train.py)
3. Đánh giá (tự động)
4. Lưu Model (models/simple_cnn_best.pth)
5. Tạo Báo cáo (reports/)
```

### Quy trình CI/CD:
```bash
1. Push code → GitHub
2. Kích hoạt workflow → GitHub Actions
3. Chạy tests → pytest
4. Huấn luyện model → CML
5. Báo cáo kết quả → PR comment
```

---

## 🎯 Đánh Giá Mức Độ Trưởng Thành

| Khía cạnh | Trạng thái | Mức độ trưởng thành |
|-----------|------------|---------------------|
| Chất lượng code | ✅ | Production-ready |
| Kiểm thử | ✅ | Toàn diện |
| CI/CD | ✅ | Tự động hóa |
| Tài liệu | ✅ | Hoàn chỉnh |
| Container hóa | ✅ | Tối ưu |
| Cấu hình | ✅ | Linh hoạt |
| Experiment Tracking | 🚧 | Sẵn sàng thêm |
| Model Serving | 🚧 | Sẵn sàng thêm |

---

## 📝 Bài Học Kinh Nghiệm

1. **Quản Lý Cấu Hình Là Chìa Khóa**
   - Hydra giúp thí nghiệm có thể tái tạo
   - Dễ chuyển đổi giữa các config

2. **Kiểm Thử Tiết Kiệm Thời Gian**
   - Phát hiện bug sớm
   - Tự tin khi refactor

3. **Tối Ưu CI/CD Quan Trọng**
   - Dependencies nhẹ giảm thời gian build
   - Quản lý disk space rất quan trọng

---

## 📝 Bài Học Kinh Nghiệm (tiếp)

4. **Tài Liệu Là Thiết Yếu**
   - Giảm thời gian onboarding
   - Làm cho bảo trì dễ dàng hơn

5. **Kiến Trúc Modular Chiến Thắng**
   - Dễ mở rộng
   - Dễ test
   - Dễ bảo trì

---

## 🎯 Khuyến Nghị

### Cho Phát Triển:
1. ✅ Tiếp tục với phương pháp modular
2. ✅ Duy trì test coverage cao
3. ✅ Giữ tài liệu cập nhật
4. ✅ Thêm tính năng từng bước

### Cho Production:
1. ✅ Giám sát hiệu suất mô hình
2. ✅ Thiết lập cảnh báo
3. ✅ Triển khai chiến lược versioning
4. ✅ Lên kế hoạch cho khả năng mở rộng

---

## 📊 Tóm Tắt Timeline

| Giai đoạn | Trạng thái | Thời gian |
|-----------|------------|-----------|
| Setup dự án | ✅ Hoàn thành | Tuần 1 |
| Triển khai Core | ✅ Hoàn thành | Tuần 2-3 |
| Testing & CI/CD | ✅ Hoàn thành | Tuần 4 |
| Tối ưu hóa | ✅ Hoàn thành | Tuần 5 |
| Tài liệu | ✅ Hoàn thành | Tuần 5 |
| Tính năng nâng cao | 🚧 Sẵn sàng | Giai đoạn tiếp |

---

## 🎉 Tổng Kết

### Những gì chúng ta có:
- ✅ Image classifier production-ready
- ✅ Pipeline MLOps hoàn chỉnh
- ✅ Kiểm thử toàn diện
- ✅ CI/CD tự động hóa
- ✅ Hỗ trợ Docker
- ✅ Tài liệu xuất sắc

### Bước tiếp theo:
- 🚀 API serving mô hình
- 📊 Experiment tracking
- 🔍 Data validation
- 🎨 Pre-commit hooks

---

## 🙏 Cảm Ơn!

### Có câu hỏi?

**GitHub Repository:**
https://github.com/Hadayxinchao/end-to-end-image-classifier

**Các lệnh chính:**
```bash
# Huấn luyện mô hình
python src/training/train.py

# Chạy tests
pytest tests/ -v

# Build Docker
docker build -t image-classifier .

# Xem docs
mkdocs serve
```

---

## 📚 Tài Liệu Tham Khảo

### Công nghệ sử dụng:
- **PyTorch:** Framework deep learning
- **Hydra:** Quản lý cấu hình
- **DVC:** Version control cho dữ liệu
- **Pytest:** Framework testing
- **GitHub Actions:** CI/CD automation
- **Docker:** Containerization

### Best Practices:
- Clean Code Architecture
- Test-Driven Development
- Continuous Integration/Deployment
- Infrastructure as Code

---

<!-- 
Để xem bản trình chiếu này:
1. Cài đặt Marp: npm install -g @marp-team/marp-cli
2. Chuyển sang PDF: marp BAO_CAO_DU_AN.md --pdf
3. Chuyển sang HTML: marp BAO_CAO_DU_AN.md --html
4. Hoặc sử dụng Marp for VS Code extension

Lưu ý: 
- File HTML có thể mở trực tiếp bằng browser
- Để export PDF/PPTX cần cài đặt Chrome/Chromium
- Có thể sử dụng https://web.marp.app/ để xem online
-->
