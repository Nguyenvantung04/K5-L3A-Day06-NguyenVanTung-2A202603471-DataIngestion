"""Evaluate retrieved evidence and preserve per-query traces."""
import re
from typing import Any


def _normalize_match_text(text: str) -> str:
    """Normalize text for evidence comparison."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Check source/page and gold evidence; keep hit@1 and hit@3 trace."""
    gold_page = int(question.get("gold_page", -1))
    gold_source = question.get("gold_source_id", "")
    evidence_quote = question.get("evidence_quote", "")
    norm_evidence = _normalize_match_text(evidence_quote)

    evaluated_hits: list[dict[str, Any]] = []
    for hit in hits:
        hit_page = int(hit.get("page", -2))
        hit_text = hit.get("text", "")
        norm_hit_text = _normalize_match_text(hit_text)

        # A hit requires matching gold page and containing the gold evidence
        page_match = (hit_page == gold_page)
        
        # Check substring or key tokens of evidence
        evidence_match = False
        if norm_evidence and norm_evidence in norm_hit_text:
            evidence_match = True
        else:
            # Check overlap if punctuation / line breaks differed
            words = [w for w in norm_evidence.split() if len(w) > 3]
            if words and sum(1 for w in words if w in norm_hit_text) / len(words) >= 0.8:
                evidence_match = True

        is_hit = page_match and evidence_match

        evaluated_hits.append({
            "chunk_id": hit.get("chunk_id"),
            "page": hit_page,
            "score": hit.get("score"),
            "text": hit_text,
            "metadata": hit.get("metadata", {}),
            "page_match": page_match,
            "evidence_match": evidence_match,
            "is_hit": is_hit
        })

    hit_1 = bool(evaluated_hits and evaluated_hits[0]["is_hit"])
    hit_3 = any(h["is_hit"] for h in evaluated_hits[:3])

    return {
        "question_id": question.get("id"),
        "split": question.get("split"),
        "question": question.get("question"),
        "expected_answer": question.get("expected_answer"),
        "gold_page": gold_page,
        "evidence_quote": evidence_quote,
        "applied_filter": question.get("filter"),
        "hit_at_1": hit_1,
        "hit_at_3": hit_3,
        "hits": evaluated_hits
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by dev/test split."""
    splits = {"dev": [], "test": []}
    for t in traces:
        s = t.get("split", "dev")
        if s in splits:
            splits[s].append(t)

    summary: dict[str, Any] = {}
    for s_name, s_traces in splits.items():
        total = len(s_traces)
        if total == 0:
            summary[f"{s_name}_hit1"] = "0/0 (0.0%)"
            summary[f"{s_name}_hit3"] = "0/0 (0.0%)"
            summary[f"{s_name}_hit1_count"] = 0
            summary[f"{s_name}_hit3_count"] = 0
            summary[f"{s_name}_total"] = 0
            continue

        h1 = sum(1 for t in s_traces if t.get("hit_at_1"))
        h3 = sum(1 for t in s_traces if t.get("hit_at_3"))

        summary[f"{s_name}_hit1"] = f"{h1}/{total} ({round(h1/total*100, 1)}%)"
        summary[f"{s_name}_hit3"] = f"{h3}/{total} ({round(h3/total*100, 1)}%)"
        summary[f"{s_name}_hit1_count"] = h1
        summary[f"{s_name}_hit3_count"] = h3
        summary[f"{s_name}_total"] = total

    return summary
