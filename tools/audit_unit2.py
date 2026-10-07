"""Audit saved answers and reproduce retrieval without generation API calls.

Run from the project root: .venv/bin/python tools/audit_unit2.py
Historical reports remain untouched. Retrieval below is a fresh measurement
against the current index, not a replacement for the September transcripts.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config
import gate
import questions
import store
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2


def main():
    print("Produced by: tools/audit_unit2.py::main")
    print("Saved generation output: run_eval.py::run_once -> generate.py::answer_from_chunks")
    items = questions.answered()
    for label, filename in (
        ("before", "run_2026-09-30_1721_before.md"),
        ("after", "run_2026-09-30_1809_after.md"),
    ):
        report = (ROOT / "results" / filename).read_text()
        blocks = re.findall(
            r"### (.*?) — run (\d+)\n(.*?)(?=\n### |\Z)", report, re.S
        )
        assert len(blocks) == len(items) * 3
        print(f"\nSaved {label} report: {filename}")
        for run in range(1, 4):
            entries = {q: body for q, n, body in blocks if int(n) == run}
            assert len(entries) == len(items)
            citations = phrases = 0
            for item in items:
                body = entries[item["question"]]
                answer = re.search(r"```\n(.*?)\n```", body, re.S).group(1)
                sources = re.search(r"Sources retrieved: (.*)", body).group(1).split(", ")
                citations += any(source in answer for source in sources)
                phrases += item["expects"].lower() in answer.lower()
            print(f"Run {run}: C2 source named {citations}/5; C5 expected phrase {phrases}/5")
        assert "Refused 5 of 5." in report
        print("C3: saved deterministic gate refused 5/5 (same value in each run column)")

    # Use the same real bundled model on CPU to avoid macOS CoreML sandbox
    # compilation failures. No fake embeddings and no generation calls.
    store._model = store._OnnxEmbedder()
    store._model._ef = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])
    collection = store._client().get_collection(config.collection_name())
    print("\nFresh retrieval audit: current campus_life/default index, real MiniLM on CPU")
    print("Semantic baseline reproduces the pre-change collection.query(top_k=5) path.")
    print("Hybrid path: store.py::search. Chunk producer recorded beside each chunk.")
    totals = {mode: [0, 0] for mode in ("semantic", "hybrid")}
    for item in items:
        print(f"\nQuestion: {item['question']}")
        raw = collection.query(query_embeddings=store.embed([item["question"]]), n_results=5)
        semantic = [store.Result(text, meta["source"], f"{meta['source']}#{meta['index']}", distance, meta["produced_by"])
                    for text, meta, distance in zip(raw["documents"][0], raw["metadatas"][0], raw["distances"][0])]
        for mode, results in (("semantic", semantic), ("hybrid", store.search(item["question"]))):
            has_fact = [item["expects"].lower() in r.text.lower() for r in results]
            totals[mode][0] += any(has_fact)
            totals[mode][1] += has_fact[0]
            print(f"{mode}: top-five contains expected phrase={any(has_fact)}; rank-one={has_fact[0]}")
            print(f"rank-one {results[0].label}, produced by {results[0].produced_by}:")
            print(results[0].text)
    print("\nFresh retrieval totals (phrase presence is a proxy; inspect printed chunks):")
    for mode, (top_five, rank_one) in totals.items():
        print(f"{mode}: top-five {top_five}/5; rank-one {rank_one}/5")
    refused = 0
    for question in questions.OUT_OF_SCOPE:
        decision = gate.check(store.search(question))
        refused += not decision.passed
        print(f"gate.py::check: {question} | distance={decision.best_distance:.3f} | refused={not decision.passed}")
    print(f"Fresh hybrid gate refused {refused}/5")


if __name__ == "__main__":
    main()
