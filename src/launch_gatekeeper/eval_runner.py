
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .pipeline import review_launch
from .utils import load_jsonl

def main() -> None:
    parser = argparse.ArgumentParser(description="Run eval over seeded launch cases.")
    parser.add_argument("gold_path")
    args = parser.parse_args()

    golds = load_jsonl(Path(args.gold_path))
    total = len(golds)
    risk_score = 0
    abstain_ok = 0
    rows = []

    for g in golds:
        pred = review_launch(g["launch"])
        expected = set(g["expected_risks"])
        predicted = set(pred["risks"])
        risk_score += len(expected & predicted) / max(len(expected), 1)
        ok = (pred["status"] == "abstained") == g["should_abstain"]
        abstain_ok += int(ok)
        rows.append({
            "case_id": g["case_id"],
            "predicted_risks": sorted(predicted),
            "expected_risks": sorted(expected),
            "status": pred["status"],
            "abstain_ok": ok
        })

    summary = {
        "total_cases": total,
        "risk_match_score": round(risk_score / total, 3) if total else 0.0,
        "abstention_accuracy": round(abstain_ok / total, 3) if total else 0.0,
        "rows": rows
    }
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
