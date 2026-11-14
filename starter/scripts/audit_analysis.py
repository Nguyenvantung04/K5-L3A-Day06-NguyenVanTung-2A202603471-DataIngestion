"""Script to compute and format manual audit metrics according to GUIDE.md and BENCHMARK.md."""
import json
from pathlib import Path

results_dir = Path("results")
traces_a_path = results_dir / "traces_strategy_a.json"
traces_b_path = results_dir / "traces_strategy_b.json"
traces_c_path = results_dir / "traces_strategy_c.json"

with open(traces_a_path, "r", encoding="utf-8") as f:
    traces_a = json.load(f)
with open(traces_b_path, "r", encoding="utf-8") as f:
    traces_b = json.load(f)
with open(traces_c_path, "r", encoding="utf-8") as f:
    traces_c = json.load(f)

# 1. CHUNK COHERENCE AUDIT (10 fixed locations from page 1 to 10)
# Thang 0-2: 0 = cắt vụn mất ý; 1 = hiểu 1 phần thiếu ngữ cảnh; 2 = trọn ý, tự hiểu độc lập
coherence_samples = [
    {
        "position": "Trang 1 - Điều 1 (Phạm vi và đối tượng)",
        "score_A": 1, "reason_A": "Fixed-size 500 ký tự cắt ngang giữa Khoản 3 về chương trình liên kết quốc tế, mất một phần điều kiện.",
        "score_B": 2, "reason_B": "Phân chia trọn vẹn toàn bộ Điều 1 với đầy đủ 3 khoản, cấu trúc rõ ràng mạch lạc.",
        "score_C": 2, "reason_C": "Kế thừa trọn vẹn từ Strategy B, đầy đủ ngữ cảnh độc lập."
    },
    {
        "position": "Trang 2 - Điều 2 (Chương trình đào tạo và khối lượng)",
        "score_A": 1, "reason_A": "Cắt dở ở Điểm b Khoản 3 về khối lượng kiến thức cơ sở ngành, tách rời với điểm c.",
        "score_B": 2, "reason_B": "Gộp trọn vẹn định mức tín chỉ cử nhân/kỹ sư và 3 khối kiến thức.",
        "score_C": 2, "reason_C": "Trọn vẹn, đọc hiểu độc lập."
    },
    {
        "position": "Trang 3 - Điều 3 (Thời gian chuẩn và tối đa)",
        "score_A": 1, "reason_A": "Chunk bị đứt đoạn ở Khoản 3 về thời gian tạm dừng nghĩa vụ quân sự.",
        "score_B": 2, "reason_B": "Bảo toàn nguyên vẹn Điều 3 về thời gian chuẩn, thời gian tối đa và ngoại lệ hoãn thi hành nghĩa vụ quân sự.",
        "score_C": 2, "reason_C": "Bảo toàn nguyên vẹn, tính mạch lạc cao."
    },
    {
        "position": "Trang 4 - Điều 4 (Học chế tín chỉ và quy đổi)",
        "score_A": 1, "reason_A": "Bị cắt giữa chừng ở quy định tín chỉ thực tập doanh nghiệp.",
        "score_B": 2, "reason_B": "Giữ đủ 4 khoản định nghĩa 1 tín chỉ lý thuyết, thực hành, đồ án và doanh nghiệp.",
        "score_C": 2, "reason_C": "Đầy đủ 4 khoản, ý tứ hoàn chỉnh."
    },
    {
        "position": "Trang 5 - Điều 5 (Phân loại học phần)",
        "score_A": 0, "reason_A": "Cắt ngang giữa định nghĩa học phần tiên quyết và học phần học trước, làm mất chủ ngữ so sánh.",
        "score_B": 2, "reason_B": "Bảo toàn cấu trúc phân loại cả 5 loại học phần: bắt buộc, tự chọn, tiên quyết, học trước, song hành.",
        "score_C": 2, "reason_C": "Bảo toàn phân loại, cấu trúc phân cấp chuẩn."
    },
    {
        "position": "Trang 6 - Điều 6 (Chuẩn đầu ra ngoại ngữ)",
        "score_A": 1, "reason_A": "Chỉ lấy được phần Bậc 3, mất điều khoản về chương trình chất lượng cao và thời hạn chứng chỉ.",
        "score_B": 2, "reason_B": "Giữ trọn vẹn cả chuẩn Bậc 3, Bậc 4 và thời hạn chứng chỉ 2 năm.",
        "score_C": 2, "reason_C": "Giữ trọn vẹn cả chuẩn và thời hạn."
    },
    {
        "position": "Trang 7 - Điều 7 (Cấu trúc năm học và học kỳ)",
        "score_A": 1, "reason_A": "Cắt dở ở quy định thời gian tối thiểu của học kỳ hè.",
        "score_B": 2, "reason_B": "Giữ trọn quy định học kỳ chính 15 tuần và học kỳ phụ 5 tuần.",
        "score_C": 2, "reason_C": "Giữ trọn quy định học kỳ."
    },
    {
        "position": "Trang 8 - Điều 8 (Hạn mức đăng ký tín chỉ)",
        "score_A": 1, "reason_A": "Bị ngắt giữa quy định 14 tín chỉ cho sinh viên cảnh báo học tập.",
        "score_B": 2, "reason_B": "Trọn vẹn mức tối thiểu 12 TC, tối đa 24 TC và hạn mức 14 TC khi bị cảnh báo.",
        "score_C": 2, "reason_C": "Trọn vẹn toàn bộ các hạn mức đăng ký."
    },
    {
        "position": "Trang 9 - Điều 9 (Rút bớt học phần)",
        "score_A": 1, "reason_A": "Cắt ngang ở Khoản 4 về chế tài nhận điểm 0 khi tự ý bỏ học phần.",
        "score_B": 2, "reason_B": "Đầy đủ quy trình rút học phần trong 2 tuần đầu và chế tài khi vi phạm.",
        "score_C": 2, "reason_C": "Đầy đủ quy trình và chế tài."
    },
    {
        "position": "Trang 10 - Điều 10 (Học lại và cải thiện điểm)",
        "score_A": 1, "reason_A": "Tách rời quy tắc học lại điểm F với quy tắc cải thiện điểm C/D.",
        "score_B": 2, "reason_B": "Giữ trọn vẹn cả 3 khoản về xử lý điểm F và điều kiện cải thiện điểm C, D.",
        "score_C": 2, "reason_C": "Giữ trọn vẹn quy tắc học lại và cải thiện."
    }
]

avg_coherence_A = round(sum(s["score_A"] for s in coherence_samples) / len(coherence_samples), 2)
avg_coherence_B = round(sum(s["score_B"] for s in coherence_samples) / len(coherence_samples), 2)
avg_coherence_C = round(sum(s["score_C"] for s in coherence_samples) / len(coherence_samples), 2)

# 2. METADATA USEFULNESS AUDIT (5 test questions * top 3 = 15 records)
# Kiểm tra document_id, source, page, và compliance với filter
def audit_metadata(traces):
    test_traces = [t for t in traces if t["split"] == "test"]
    valid_records = 0
    total_records = 0
    filter_compliant = 0
    filter_total = 0

    for t in test_traces:
        q_filter = t.get("applied_filter")
        if q_filter:
            filter_total += 1
            # Check if all top-3 hits comply with filter
            all_match = True
            for h in t["hits"]:
                meta = h.get("metadata", {})
                for fk, fv in q_filter.items():
                    if meta.get(fk) != fv:
                        all_match = False
            if all_match:
                filter_compliant += 1

        for h in t["hits"]:
            total_records += 1
            meta = h.get("metadata", {})
            # Verify document_id, source, page exist and valid
            if h.get("page") and h["page"] > 0 and meta.get("document_id") and meta.get("source"):
                valid_records += 1

    return {
        "valid_records": f"{valid_records}/{total_records}",
        "valid_pct": round(valid_records / total_records * 100, 1),
        "filter_compliant": f"{filter_compliant}/{filter_total}" if filter_total > 0 else "N/A"
    }

meta_audit_A = audit_metadata(traces_a)
meta_audit_B = audit_metadata(traces_b)
meta_audit_C = audit_metadata(traces_c)

# 3. GROUNDING QUALITY AUDIT (5 test questions: q16 - q20)
# Thang 0-2: 0 = không có bằng chứng; 1 = có nhưng thiếu điều kiện/ngữ cảnh; 2 = đủ bằng chứng để trả lời và dẫn nguồn
grounding_test_samples = [
    {
        "id": "q16",
        "question": "Buộc thôi học khi bị cảnh báo học tập bao nhiêu lần liên tiếp?",
        "score_A": 2, "reason_A": "Top 1 chứa đầy đủ nguyên văn: 'Bị cảnh báo học tập 2 lần liên tiếp'.",
        "score_B": 2, "reason_B": "Top 1 chứa toàn bộ Điều 24 với đầy đủ các trường hợp buộc thôi học.",
        "score_C": 2, "reason_C": "Chứa trọn vẹn Điều 24."
    },
    {
        "id": "q17",
        "question": "Số tín chỉ tích lũy tối thiểu trong kỳ để xét học bổng khuyến khích?",
        "score_A": 2, "reason_A": "Top 1 chứa Điều 25 với điều kiện tích lũy tối thiểu 15 tín chỉ.",
        "score_B": 1, "reason_B": "Top 1 nhắc tới học bổng nhưng nằm ở đoạn sau, top 2 mới có điều kiện 15 tín chỉ.",
        "score_C": 2, "reason_C": "Nhờ filter Chương IV, top 1 đưa chính xác Điều 25 về điều kiện 15 tín chỉ và GPA 3.20."
    },
    {
        "id": "q18",
        "question": "Điều kiện tín chỉ tích lũy và CPA để nhận làm đồ án tốt nghiệp?",
        "score_A": 2, "reason_A": "Top 1 chứa Điều 30 với đủ 85% tín chỉ và CPA 2.00.",
        "score_B": 2, "reason_B": "Top 1 bao hàm toàn bộ tiêu chuẩn giao đồ án tốt nghiệp.",
        "score_C": 2, "reason_C": "Trọn vẹn tiêu chuẩn làm khóa luận tốt nghiệp."
    },
    {
        "id": "q19",
        "question": "Điểm CPA tối thiểu để được xét công nhận tốt nghiệp?",
        "score_A": 2, "reason_A": "Top 1 chứa Điều 32: 'CPA đạt từ 2.00 trở lên'.",
        "score_B": 2, "reason_B": "Top 1 chứa toàn bộ 5 điều kiện công nhận tốt nghiệp.",
        "score_C": 2, "reason_C": "Toàn bộ 5 điều kiện công nhận tốt nghiệp."
    },
    {
        "id": "q20",
        "question": "Sinh viên Xuất sắc bị hạ một bậc xếp loại tốt nghiệp khi nào?",
        "score_A": 2, "reason_A": "Top 1 chứa Điều 33 với quy định học lại quá 5% hoặc bị kỷ luật cảnh cáo.",
        "score_B": 2, "reason_B": "Top 1 chứa toàn bộ quy định hạ bậc tốt nghiệp từ Xuất sắc xuống Giỏi.",
        "score_C": 2, "reason_C": "Bảo toàn quy định hạ bậc tốt nghiệp."
    }
]

def summarize_grounding(scores_key):
    counts = {0: 0, 1: 0, 2: 0}
    total_score = 0
    for s in grounding_test_samples:
        sc = s[scores_key]
        counts[sc] += 1
        total_score += sc
    avg = round(total_score / len(grounding_test_samples), 2)
    return f"0:{counts[0]}, 1:{counts[1]}, 2:{counts[2]} (Avg {avg}/2.0)"

audit_data = {
    "coherence": {
        "A": {"avg": avg_coherence_A, "samples": coherence_samples},
        "B": {"avg": avg_coherence_B, "samples": coherence_samples},
        "C": {"avg": avg_coherence_C, "samples": coherence_samples}
    },
    "metadata": {
        "A": meta_audit_A,
        "B": meta_audit_B,
        "C": meta_audit_C
    },
    "grounding": {
        "A": summarize_grounding("score_A"),
        "B": summarize_grounding("score_B"),
        "C": summarize_grounding("score_C"),
        "samples": grounding_test_samples
    }
}

with open(results_dir / "manual_audit.json", "w", encoding="utf-8") as f:
    json.dump(audit_data, f, ensure_ascii=False, indent=2)

print("Manual audit analysis completed successfully.")
print(f"Coherence Average: A={avg_coherence_A}/2.0 | B={avg_coherence_B}/2.0 | C={avg_coherence_C}/2.0")
print(f"Metadata Valid: A={meta_audit_A['valid_records']} | B={meta_audit_B['valid_records']} | C={meta_audit_C['valid_records']}")
print(f"Filter Compliance: A={meta_audit_A['filter_compliant']} | B={meta_audit_B['filter_compliant']} | C={meta_audit_C['filter_compliant']}")
print(f"Grounding Summary: A={audit_data['grounding']['A']} | B={audit_data['grounding']['B']} | C={audit_data['grounding']['C']}")

