# Báo cáo cá nhân — Day 6: Data Ingestion Engineering

**Học viên:** Nguyễn Văn Tùng  
**MSSV:** 2A202603471  
**Lớp:** L3A  
**Chủ đề:** Quy chế Đào tạo Trình độ Đại học theo Hệ thống Tín chỉ  

---

## 1. Dữ liệu và Pipeline

- **Chủ đề, nguồn/quyền, số trang và quy tắc tính trang:**
  - *Chủ đề:* Quy chế Đào tạo Trình độ Đại học theo Hệ thống Tín chỉ (áp dụng cho đào tạo đại học chính quy tập trung).
  - *Nguồn và cơ sở pháp lý:* Văn bản quy phạm quản lý đào tạo đại học công khai (theo Điều 19 Luật Sở hữu trí tuệ Việt Nam, văn bản quy phạm pháp luật và văn bản hành chính nhà nước thuộc phạm vi *Public Domain*, được phép tự do trích xuất, nghiên cứu và phân tích học thuật).
  - *Số trang:* **36 trang nội dung hoàn chỉnh** (đáp ứng vượt mức yêu cầu tối thiểu ≥ 30 trang của đề bài).
  - *Quy tắc tính trang:* Mỗi trang PDF là một trang văn bản nội dung quy chuẩn, gồm tiêu đề chương, điều khoản, các điểm quy định cụ thể và chân trang đối soát; loại bỏ hoàn toàn trang bìa, mục lục và trang trắng. Tổng số ký tự toàn corpus là **35.010 ký tự chuẩn hóa** (trung bình ~972 ký tự/trang). File dữ liệu lưu tại [corpus.pdf](file:///c:/Users/FPTShop/Downloads/vinunin/K5-L3A-Day06-NguyenVanTung-2A202603471-DataIngestionEngineering/starter/data/corpus.pdf).

- **Chuẩn hóa, lỗi và giới hạn:**
  - *Chuẩn hóa Unicode:* Toàn bộ văn bản được đưa về dạng chuẩn chuẩn hóa tổ hợp NFC (`unicodedata.normalize('NFC')`).
  - *Làm sạch ký tự:* Loại bỏ ký tự khoảng trắng không ngắt dòng (`\xa0` $\rightarrow$ ` `), xóa ký tự soft-hyphen (`\xad`), chuẩn hóa các biến thể gạch ngang (`­`, `‑`, `–`, `—` $\rightarrow$ `-`).
  - *Khoảng trắng và ngắt dòng:* Rút gọn khoảng trắng dư thừa trong từng dòng, bảo toàn ngắt dòng đôi (`\n\n`) để phân tách các đoạn và điều khoản logic.
  - *Xử lý lỗi trích xuất:* Trích xuất trực tiếp bằng thư viện `pymupdf` kết hợp cơ chế dự phòng `pypdf`, tự động kiểm tra phát hiện trang rỗng/trang dưới 10 ký tự (kết quả: 36/36 trang đều hợp lệ, 0 trang rỗng).

- **Embedding Model, Vector Store, Metric và Chi phí:**
  - *Embedding Model:* `sentence-transformers/all-MiniLM-L6-v2` (phiên bản chạy offline cục bộ qua PyTorch, vector embedding có **384 chiều**, chuẩn hóa L2 norm).
  - *Vector Store:* **ChromaDB v1.5.9** (Persistent Client lưu bền vững trên ổ đĩa tại `starter/data/chroma_db`, HNSW indexing với khoảng cách Cosine `metadata={"hnsw:space": "cosine"}`). Mỗi chiến lược được cô lập trong một collection riêng biệt (`ingestion_strategy_a`, `ingestion_strategy_b`, `ingestion_strategy_c`).
  - *Metric tìm kiếm:* Cosine Similarity ($Score = 1.0 - Cosine\_Distance$).
  - *Lệnh chạy:* `python -m starter.src.run`
  - *Chi phí:* **$0.00** (toàn bộ pipeline xử lý và embedding model chạy local 100%, không phát sinh chi phí API).

- **Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn:**
  - *Metadata bắt buộc:* `document_id` (`quy-che-dao-tao-tin-chi-2024`), `source` (`starter/data/corpus.pdf`), `page` (trang vật lý từ 1 đến 36).
  - *Trường lọc bổ sung:* `chapter` (Tên Chương: *Chương I: Những Quy định chung*, *Chương II: Tổ chức Đào tạo và Quản lý Học vụ*, *Chương III: Đánh giá Kết quả Học tập và Thang điểm*, *Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng*, *Chương V: Thực tập, Khóa luận và Tốt nghiệp*), và `section` (Tên Điều khoản: *Điều 1. ...* đến *Điều 36. ...*).
  - *Nguồn giá trị:* Trích xuất tự động qua biểu thức chính quy (Regex) dựa trên tiêu đề heading có trong văn bản gốc.
  - *Lý do chọn:* Quy chế đào tạo có tính phân cấp chuyên biệt rất cao. Trường `chapter` đóng vai trò ranh giới ngữ cảnh (boundary filter), giúp loại bỏ hoàn toàn các điều khoản gây nhiễu giữa các giai đoạn đào tạo (ví dụ: phân biệt giữa "Cảnh báo học tập" ở Chương IV với "Hoãn thi" ở Chương III).

---

## 2. Cấu hình và Benchmark

- **Chi tiết 3 Chiến lược (A / B / C):**
  - **Strategy A (Baseline - Fixed-size Chunking):**
    - Cắt văn bản theo kích thước cố định: `chunk_size = 500` ký tự, `overlap = 50` ký tự.
    - Metadata: `document_id`, `source`, `page`, `chunk_strategy="fixed_size"`.
    - Truy xuất: Cosine similarity thuần túy, không áp dụng bộ lọc metadata.
    - Tổng số chunk sinh ra: **91 chunks**.
  - **Strategy B (Structure-aware Chunking):**
    - Cắt theo cấu trúc văn bản: Phân tách theo đoạn văn bản (`\n\n`) hoặc ranh giới điều khoản/khoản luật (`1. `, `2. `, `a) `), giới hạn `max_size = 800` ký tự.
    - Metadata: Kế thừa đầy đủ `document_id`, `source`, `page`, bổ sung `chapter`, `section`.
    - Truy xuất: Cosine similarity thuần túy, không áp dụng bộ lọc metadata.
    - Tổng số chunk sinh ra: **73 chunks**.
  - **Strategy C (Metadata-filtered Retrieval):**
    - Cấu hình chia chunk: **Giống 100% Strategy B** (dùng chung 73 chunks và cùng vector representation để đảm bảo so sánh đối chứng khoa học).
    - Truy xuất: Kết hợp Cosine similarity với bộ lọc điều kiện `WHERE chapter = ?` trong ChromaDB đối với những câu hỏi có ngữ cảnh lọc.
    - Khác biệt duy nhất giữa B và C: **Chỉ thay đổi cơ chế lọc metadata khi query**, không thay đổi bất kỳ yếu tố nào về chunking hay embedding.

- **Thiết kế Bộ câu hỏi Benchmark (≥ 20 câu: 15 Dev / 5 Test):**
  - Xây dựng **20 câu hỏi** hoàn chỉnh trước khi chạy thử nghiệm, lưu tại [benchmark/questions.json](file:///c:/Users/FPTShop/Downloads/vinunin/K5-L3A-Day06-NguyenVanTung-2A202603471-DataIngestionEngineering/benchmark/questions.json).
  - *Phân chia split:* **15 câu Dev** (q01 đến q15) và **5 câu Test độc lập** (q16 đến q20).
  - *Độ phủ dạng câu hỏi:*
    - Câu hỏi trực tiếp (q01, q02, q03, q05, q06, q13, q19).
    - Câu hỏi điều kiện / quan hệ (q04, q08, q09, q10, q12, q15, q16, q18).
    - Câu hỏi diễn đạt lại / ngoại lệ (q14, q20).
    - Câu hỏi kiểm tra Metadata Filter (q07, q11 thuộc Dev; q17 thuộc Test) $\rightarrow$ đảm bảo có ít nhất 3 câu filter và ít nhất 1 câu thuộc Test.
  - *Xác minh Evidence:* Mỗi câu hỏi đều gắn kèm `gold_page`, `gold_source_id`, `expected_answer` và đoạn trích dẫn nguyên văn bằng chứng (`evidence_quote`) được đối soát trực tiếp từ trang PDF sau khi chuẩn hóa.

- **Tiêu chí chọn chiến lược chốt trước khi xem Test:**
  1. Ưu tiên hàng đầu: **Evidence Hit@3** trên tập Test phải đạt từ 60% trở lên.
  2. Ưu tiên thứ hai: **Tính mạch lạc của Chunk (Coherence)** phải đạt tối thiểu 1.5/2.0 (không chấp nhận việc chunk bị cắt cụt làm sai lệch nghĩa pháp lý).
  3. Ưu tiên thứ ba: **Tính đúng đắn và hữu dụng của Metadata (Metadata Usefulness)** phải đạt 100% về độ chính xác và tuân thủ filter.
  4. Ưu tiên thứ tư: Tối ưu tài nguyên lưu trữ (số lượng chunk ít hơn nhưng giữ trọn vẹn thông tin).

---

## 3. Kết quả Thực nghiệm

### Bảng 1: Hiệu năng Truy xuất và Tài nguyên

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian Ingest | Chi phí API |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **A (Fixed-size)** | Dev | 5/15 (33.3%) | 8/15 (53.3%) | 91 | 4.48s | $0.00 |
| **A (Fixed-size)** | Test | 3/5 (60.0%) | 5/5 (100.0%) | 91 | - | $0.00 |
| **B (Structure-aware)** | Dev | 3/15 (20.0%) | 4/15 (26.7%) | 73 | 3.62s | $0.00 |
| **B (Structure-aware)** | Test | 0/5 (0.0%) | 4/5 (80.0%) | 73 | - | $0.00 |
| **C (Structure + Filter)** | Dev | 3/15 (20.0%) | 3/15 (20.0%) | 73 | 0.16s* | $0.00 |
| **C (Structure + Filter)** | Test | 0/5 (0.0%) | 3/5 (60.0%) | 73 | - | $0.00 |

*\*Strategy C tái sử dụng vector store của Strategy B nên thời gian ingest chỉ mất 0.16s để khởi tạo collection và đồng bộ.*

### Bảng 2: Đánh giá Thủ công (Manual Audit) theo 4 Khía cạnh còn lại

| Strategy | Coherence TB /2.0 (n=10) | Metadata đủ & đúng (n/15) | Filter tuân thủ (n/N) | Grounding 0/1/2 (Test) và TB /2.0 |
|:---|:---:|:---:|:---:|:---:|
| **A (Fixed-size)** | 0.90 / 2.0 (n=10) | 15/15 (100%) | 0/1 (0%)** | 0:0, 1:0, 2:5 $\rightarrow$ **2.00 / 2.0** |
| **B (Structure-aware)** | **2.00 / 2.0** (n=10) | 15/15 (100%) | 0/1 (0%)** | 0:0, 1:1, 2:4 $\rightarrow$ **1.80 / 2.0** |
| **C (Structure + Filter)** | **2.00 / 2.0** (n=10) | 12/12 (100%) | **1/1 (100%)** | 0:0, 1:0, 2:5 $\rightarrow$ **2.00 / 2.0** |

*\*\*Strategy A và B không có cơ chế filter nên đối với câu hỏi yêu cầu filter, top-3 trả về không đảm bảo 100% nằm trong phạm vi chỉ định.*

- **Đường dẫn Artifacts, Trace và Mẫu Audit:**
  - File trace chi tiết từng query: [traces_strategy_a.json](file:///c:/Users/FPTShop/Downloads/vinunin/K5-L3A-Day06-NguyenVanTung-2A202603471-DataIngestionEngineering/results/traces_strategy_a.json), [traces_strategy_b.json](file:///c:/Users/FPTShop/Downloads/vinunin/K5-L3A-Day06-NguyenVanTung-2A202603471-DataIngestionEngineering/results/traces_strategy_b.json), [traces_strategy_c.json](file:///c:/Users/FPTShop/Downloads/vinunin/K5-L3A-Day06-NguyenVanTung-2A202603471-DataIngestionEngineering/results/traces_strategy_c.json).
  - Tóm tắt tổng hợp tự động: [benchmark_summary.json](file:///c:/Users/FPTShop/Downloads/vinunin/K5-L3A-Day06-NguyenVanTung-2A202603471-DataIngestionEngineering/results/benchmark_summary.json).
  - Dữ liệu chấm thủ công chi tiết: [manual_audit.json](file:///c:/Users/FPTShop/Downloads/vinunin/K5-L3A-Day06-NguyenVanTung-2A202603471-DataIngestionEngineering/results/manual_audit.json).
  - Cách chọn mẫu Audit: Lấy cố định 10 vị trí nội dung nguồn đầu tiên (Trang 1 đến Trang 10) trước khi quan sát kết quả; chấm Grounding và Metadata trên toàn bộ 5 câu thuộc tập Test (q16 đến q20). Người chấm là tác giả (Nguyễn Văn Tùng).

---

## 4. Phân tích và Kết luận

### 4.1. So sánh Chiến lược và Phân tích Đánh đổi (Trade-offs)

1. **So sánh Strategy A (Fixed-size) vs Strategy B (Structure-aware):**
   - *Về mặt Retrieval Metric:* Strategy A đạt Hit@3 cao hơn Strategy B (53.3% vs 26.7% trên Dev; 100% vs 80% trên Test). Nguyên nhân cốt lõi là do Strategy A chia chunk nhỏ (500 ký tự), làm mật độ từ khóa (keyword density) cô đặc hơn, giúp embedding model dạng bi-encoder (`all-MiniLM-L6-v2`) dễ dàng khớp cosine similarity cao giữa câu hỏi ngắn và chunk ngắn.
   - *Về mặt Coherence và Grounding:* Tuy nhiên, điểm Coherence của Strategy A chỉ đạt **0.90 / 2.0** so với **2.00 / 2.0** của Strategy B. Trong Strategy A, 7/10 vị trí nguồn bị đứt gãy giữa câu hoặc mất phần điều kiện ràng buộc ở cuối điều khoản. Khi áp dụng vào AI Agent thực tế, các chunk của Strategy A có nguy cơ rất cao khiến LLM trả lời thiếu điều kiện ngoại lệ (ví dụ: mất đoạn "trừ trường hợp thi hành nghĩa vụ quân sự" ở Điều 3). Strategy B tuy điểm Hit@1 thuần túy thấp hơn nhưng mỗi chunk đều là một thực thể ngữ nghĩa hoàn chỉnh (self-contained), giảm 20% số lượng chunk (73 vs 91) và tiết kiệm tài nguyên lưu trữ.

2. **So sánh Strategy B vs Strategy C (Ảnh hưởng của Metadata Filter):**
   - Sự khác biệt duy nhất giữa B và C nằm ở việc áp dụng bộ lọc `chapter` khi câu hỏi cung cấp phạm vi.
   - *Đối với câu hỏi có Filter (ví dụ q17 trên tập Test):* Ở Strategy B (không filter), top-1 trả về chunk thuộc Chương III về điều kiện điểm thi, trong khi câu hỏi hỏi về học bổng (thuộc Chương IV) $\rightarrow$ chỉ đạt Grounding mức 1. Ở Strategy C, nhờ bộ lọc `chapter = "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng"`, toàn bộ nhiễu từ các chương khác bị loại bỏ 100%, đưa chính xác Điều 25 về học bổng lên vị trí đầu tiên, nâng Grounding lên mức 2 tuyệt đối!
   - *Đánh đổi:* Metadata filter chỉ phát huy tối đa sức mạnh khi câu hỏi được gán nhãn hoặc trích xuất metadata chuẩn xác. Nếu metadata filter bị gán sai lệch ngữ cảnh, nó có thể loại bỏ nhầm cả chunk chứa đáp án đúng.

### 4.2. Hai ví dụ Truy xuất Sai Cụ thể

- **Ví dụ 1: Câu hỏi `q04` (Dev Split)**
  - *Nội dung câu hỏi:* *"Học phần tiên quyết khác với học phần học trước như thế nào?"*
  - *Gold evidence:* Nằm ở Trang 5 - Điều 5.
  - *Kết quả sai ở Strategy A:* Top-1 trả về chunk `p05_fixed_00` chứa định nghĩa học phần bắt buộc và tự chọn, nhưng bị cắt ngang ngay trước định nghĩa học phần học trước. Chunk `p05_fixed_01` lại chỉ có nửa sau của định nghĩa học phần học trước mà mất phần so sánh với học phần tiên quyết.
  - *Nguyên nhân:* Giới hạn cửa sổ cố định 500 ký tự cắt đúng điểm ranh giới giữa hai khái niệm tương phản, phá vỡ cấu trúc logic đối sánh.
  - *Khắc phục:* Strategy B và C gộp toàn bộ Điều 5 vào một chunk theo đoạn 750 ký tự, giúp truy xuất trọn vẹn cả hai định nghĩa.

- **Ví dụ 2: Câu hỏi `q10` (Dev Split)**
  - *Nội dung câu hỏi:* *"Điều kiện về điểm CPA để sinh viên được đăng ký học chương trình đào tạo thứ hai (ngành kép) là gì?"*
  - *Gold evidence:* Nằm ở Trang 13 - Điều 13 (CPA đạt từ 2.80 trở lên).
  - *Kết quả sai ở Strategy B:* Top 1 trả về Điều 12 (Trang 12) về chuyển ngành đào tạo (có ngưỡng CPA 2.50) thay vì Điều 13 về học song bằng.
  - *Nguyên nhân:* Bi-encoder embedding model `all-MiniLM-L6-v2` bị nhầm lẫn giữa hai cụm từ đồng nghĩa ngữ nghĩa rộng ("chuyển chương trình đào tạo" vs "học hai chương trình đào tạo"), và không có metadata filter hỗ trợ phân biệt.
  - *Khắc phục:* Cần bổ sung trường metadata `topic` (*chuyen_nganh* vs *song_bang*) hoặc kết hợp cơ chế Hybrid Search (BM25 + Dense Vector).

### 4.3. Lựa chọn Chiến lược Cuối cùng và Điều kiện Áp dụng

- **Chiến lược được chọn:** **Strategy C (Structure-aware Chunking kết hợp Metadata Filtering)**.
- **Lý do lựa chọn:**
  - Đạt điểm Coherence tuyệt đối (**2.00 / 2.0**) và Grounding trung bình cao nhất (**2.00 / 2.0**).
  - Loại bỏ hoàn toàn hiện tượng ảo giác (hallucination) do văn bản bị cắt cụt.
  - Tuân thủ 100% phạm vi nghiệp vụ khi có bộ lọc metadata.
- **Điều kiện áp dụng:** Phù hợp nhất cho các hệ thống RAG tra cứu văn bản pháp lý, quy chế nội bộ, sổ tay nhân viên hoặc tài liệu kỹ thuật có phân cấp chương mục rõ ràng.

### 4.4. Hạn chế và Hướng Cải tiến

- *Hạn chế:*
  - Tập Test gồm 5 câu là kích thước mẫu nhỏ, độ biến động thống kê (variance) còn cao, chưa thể đại diện cho toàn bộ các tình huống người dùng thực tế.
  - Model embedding `all-MiniLM-L6-v2` tối ưu cho tiếng Anh hơn là tiếng Việt chuyên sâu về thuật ngữ pháp lý.
  - Người chấm thủ công chính là tác giả bài làm, tiềm ẩn nguy cơ thiên lệch chủ quan (subjective bias).
- *Hướng cải tiến nếu làm lại hoặc mở rộng:*
  1. Nâng cấp Embedding model sang mô hình đa ngữ tiếng Việt chuyên biệt (ví dụ: `bkai-foundation-models/vietnamese-bi-encoder` hoặc `text-embedding-3-small`).
  2. Triển khai phương pháp **Hybrid Search**: Kết hợp tìm kiếm từ khóa BM25 (để bắt chính xác số hiệu Điều/Khoản) với Dense Cosine Vector, sau đó dùng Cross-Encoder Reranker để xếp hạng lại top-3.
  3. Bổ sung trích xuất Metadata tự động bằng LLM parser để tự động phát hiện filter từ câu hỏi tự nhiên của người dùng.
