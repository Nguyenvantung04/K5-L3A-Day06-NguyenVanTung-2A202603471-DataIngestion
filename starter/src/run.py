"""Full Data Ingestion and Benchmark Orchestration Pipeline."""
import json
import time
from pathlib import Path
from typing import Any

from .ingestion import load_pdf
from .chunking import fixed_size, by_paragraph
from .embeddings import MyEmbedder
from .store import ChromaVectorStore
from .evaluation import evaluate_query, summarize


def run_pipeline() -> dict[str, Any]:
    # Paths
    project_root = Path(__file__).resolve().parent.parent.parent
    pdf_path = project_root / "starter" / "data" / "corpus.pdf"
    benchmark_path = project_root / "benchmark" / "questions.json"
    results_dir = project_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("STEP 1: LOADING CORPUS AND VALIDATING CONTENT PAGES")
    print("=" * 60)
    pages = load_pdf(pdf_path, document_id="quy-che-dao-tao-tin-chi-2024", source="starter/data/corpus.pdf")
    print(f"Total extracted content pages: {len(pages)}")
    if len(pages) < 30:
        raise ValueError(f"Corpus requires at least 30 content pages; found {len(pages)}")

    total_chars = sum(len(p.text) for p in pages)
    print(f"Total normalized characters: {total_chars:,} chars (~{total_chars/36:.0f} chars/page)")

    print("\n" + "=" * 60)
    print("STEP 2: CHUNKING FOR STRATEGIES A, B, AND C")
    print("=" * 60)
    # Strategy A: Fixed-size (size 500, overlap 50)
    chunks_a = []
    for p in pages:
        chunks_a.extend(fixed_size(p, size=500, overlap=50))
    print(f"Strategy A (Fixed-size 500, overlap 50): {len(chunks_a)} chunks")

    # Strategy B & C: By-paragraph / heading (max_size 800)
    chunks_b = []
    for p in pages:
        chunks_b.extend(by_paragraph(p, max_size=800))
    print(f"Strategy B & C (Structure-aware, max 800): {len(chunks_b)} chunks")

    # Strategy C uses identical chunks to B for controlled comparison
    chunks_c = list(chunks_b)

    print("\n" + "=" * 60)
    print("STEP 3: EMBEDDING AND STORING IN VECTOR STORE")
    print("=" * 60)
    embedder = MyEmbedder(model_name="all-MiniLM-L6-v2")
    store = ChromaVectorStore(
        persist_directory=str(project_root / "starter" / "data" / "chroma_db"),
        dimensions=embedder.dimensions
    )
    store.create_schema()

    stats: dict[str, Any] = {}

    # Ingest Strategy A
    t0 = time.perf_counter()
    texts_a = [c.text for c in chunks_a]
    vectors_a = embedder.embed_documents(texts_a)
    store.upsert("a", chunks_a, vectors_a)
    time_a = round(time.perf_counter() - t0, 3)
    stats["A"] = {"chunk_count": len(chunks_a), "time_sec": time_a, "cost": "$0.00"}

    # Ingest Strategy B
    t0 = time.perf_counter()
    texts_b = [c.text for c in chunks_b]
    vectors_b = embedder.embed_documents(texts_b)
    store.upsert("b", chunks_b, vectors_b)
    time_b = round(time.perf_counter() - t0, 3)
    stats["B"] = {"chunk_count": len(chunks_b), "time_sec": time_b, "cost": "$0.00"}

    # Ingest Strategy C
    t0 = time.perf_counter()
    # Strategy C shares vectors with B to avoid redundant embedding
    store.upsert("c", chunks_c, vectors_b)
    time_c = round(time.perf_counter() - t0, 3)
    stats["C"] = {"chunk_count": len(chunks_c), "time_sec": time_c, "cost": "$0.00"}

    print("\n" + "=" * 60)
    print("STEP 4: RUNNING BENCHMARK RETRIEVAL ON DEV AND TEST SPLITS")
    print("=" * 60)
    with open(benchmark_path, "r", encoding="utf-8") as f:
        questions: list[dict[str, Any]] = json.load(f)
    print(f"Loaded {len(questions)} benchmark questions ({sum(1 for q in questions if q['split'] == 'dev')} dev, {sum(1 for q in questions if q['split'] == 'test')} test).")

    all_traces: dict[str, list[dict[str, Any]]] = {"A": [], "B": [], "C": []}

    for strat in ["A", "B", "C"]:
        print(f"\nEvaluating Strategy {strat}...")
        traces = []
        for q in questions:
            q_vec = embedder.embed_query(q["question"])
            # Apply metadata filter only in Strategy C when question specifies one
            q_filter = q.get("filter") if strat == "C" else None
            hits = store.search(strategy=strat.lower(), query_vector=q_vec, top_k=3, filters=q_filter)
            eval_res = evaluate_query(q, hits)
            traces.append(eval_res)

        all_traces[strat] = traces
        # Save traces to results/
        trace_file = results_dir / f"traces_strategy_{strat.lower()}.json"
        with open(trace_file, "w", encoding="utf-8") as f:
            json.dump(traces, f, ensure_ascii=False, indent=2)
        print(f"Saved traces to {trace_file}")

    print("\n" + "=" * 60)
    print("STEP 5: COMPILING FIVE-DIMENSION BENCHMARK REPORT")
    print("=" * 60)
    summary_report: dict[str, Any] = {}
    for strat in ["A", "B", "C"]:
        summ = summarize(all_traces[strat])
        summary_report[strat] = {
            "stats": stats[strat],
            "metrics": summ
        }

    summary_file = results_dir / "benchmark_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, ensure_ascii=False, indent=2)

    print("\nRETRIEVAL RESULTS SUMMARY:")
    print(f"{'Strat':<7} | {'Dev Hit@1':<15} | {'Dev Hit@3':<15} | {'Test Hit@1':<15} | {'Test Hit@3':<15} | {'Chunks':<8} | {'Time (s)'}")
    print("-" * 88)
    for strat in ["A", "B", "C"]:
        m = summary_report[strat]["metrics"]
        s = summary_report[strat]["stats"]
        print(f"{strat:<7} | {m['dev_hit1']:<15} | {m['dev_hit3']:<15} | {m['test_hit1']:<15} | {m['test_hit3']:<15} | {s['chunk_count']:<8} | {s['time_sec']}")

    return summary_report


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
