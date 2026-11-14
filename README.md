# Day 06 · Data Ingestion Engineering

**Học viên:** Nguyễn Văn Tùng  
**MSSV:** 2A202603471  
**Lớp:** L3A  
**Chủ đề:** Quy chế Đào tạo Trình độ Đại học theo Hệ thống Tín chỉ  

---

## 🚀 Tái lập Nhanh (Quick Start)

Dự án đã được tích hợp trọn vẹn và cấu hình sẵn sàng chạy offline 100% không phụ thuộc API key trả phí hay Docker:

```bash
# 1. Chạy toàn bộ pipeline (đọc PDF, chia 3 chiến lược, embed, lưu vector và benchmark)
python -m starter.src.run

# 2. Chạy kiểm tra và phân tích thủ công (Coherence, Metadata, Grounding)
python starter/scripts/audit_analysis.py
```

---

## 📁 Cấu trúc Thư mục Bài nộp

```text
├── STUDENT.md                              # Thông tin học viên và commit chốt
├── README.md                               # Hướng dẫn tái lập và tổng quan kết quả
├── data/
│   └── manifest.json                       # Manifest chi tiết 36 trang nội dung, bản quyền
├── benchmark/
│   └── questions.json                      # 20 câu hỏi (15 Dev / 5 Test) kèm gold evidence
├── artifacts/
│   └── experiment_log.csv                  # Bảng log cấu hình và số liệu 3 chiến lược A, B, C
├── results/
│   ├── traces_strategy_a.json              # Trace top-3 chi tiết Strategy A (Fixed-size)
│   ├── traces_strategy_b.json              # Trace top-3 chi tiết Strategy B (Structure-aware)
│   ├── traces_strategy_c.json              # Trace top-3 chi tiết Strategy C (Metadata filter)
│   ├── benchmark_summary.json              # Tổng hợp chỉ số Hit@1, Hit@3 tự động
│   └── manual_audit.json                   # Bảng chấm thủ công Coherence, Metadata, Grounding
├── report/
│   └── individual/
│       ├── 2A202603471_NguyenVanTung.md    # Báo cáo cá nhân chi tiết theo mẫu
│       └── MSSV_HoTen.md                   # Bản sao báo cáo cá nhân
└── starter/
    ├── data/
    │   ├── corpus.pdf                      # Tệp PDF 36 trang nội dung chuẩn hóa
    │   └── chroma_db/                      # Persistent Vector Store (ChromaDB)
    └── src/
        ├── models.py                       # Dataclass DocumentPage, Chunk
        ├── ingestion.py                    # Trích xuất PDF và chuẩn hóa Unicode
        ├── chunking.py                     # Fixed-size (A) và Structure-aware (B & C)
        ├── embeddings.py                   # Embedder model all-MiniLM-L6-v2 (offline)
        ├── store.py                        # Persistent ChromaDB Store (Cosine distance, filter)
        ├── evaluation.py                   # Đánh giá Hit@1, Evidence Hit@3 theo split
        └── run.py                          # Pipeline điều phối thực nghiệm tự động
```

---

## 📊 Tóm tắt Kết quả Thực nghiệm

| Chiến lược | Kỹ thuật Chunking | Số chunk | Dev Hit@1 | Dev Hit@3 | Test Hit@1 | Test Hit@3 | Coherence (TB /2.0) | Grounding (TB /2.0) | Filter Tuân thủ |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Strategy A** | Cố định (500 chars, overlap 50) | 91 | 5/15 (33.3%) | 8/15 (53.3%) | 3/5 (60.0%) | 5/5 (100.0%) | 0.90 / 2.0 | 2.00 / 2.0 | 0/1 (0%) |
| **Strategy B** | Cấu trúc Điều/Khoản (max 800) | 73 | 3/15 (20.0%) | 4/15 (26.7%) | 0/5 (0.0%) | 4/5 (80.0%) | **2.00 / 2.0** | 1.80 / 2.0 | 0/1 (0%) |
| **Strategy C** | Cấu trúc Điều/Khoản + Filter | 73 | 3/15 (20.0%) | 3/15 (20.0%) | 0/5 (0.0%) | 3/5 (60.0%) | **2.00 / 2.0** | **2.00 / 2.0** | **1/1 (100%)** |

> Xem chi tiết phân tích lỗi, đánh đổi và kiến giải khoa học trong [Báo cáo cá nhân](report/individual/2A202603471_NguyenVanTung.md).
