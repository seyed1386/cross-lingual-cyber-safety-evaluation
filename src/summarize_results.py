"""Summarize manually annotated JSONL evaluation results."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

VALID_BEHAVIOR = {"yes", "no", "unclear"}
VALID_REFUSAL = {"yes", "no", "unclear"}


def read_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {line_no}: {exc.msg}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"Line {line_no} must be a JSON object")
        rows.append(row)
    return rows


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("error_type"):
            continue
        groups[(str(row.get("language", "unknown")), str(row.get("category", "unknown")))].append(row)

    summaries = []
    for (language, category), items in sorted(groups.items()):
        reviewed_behavior = [r["appropriate_behavior"] for r in items if r.get("appropriate_behavior") in VALID_BEHAVIOR]
        scores = []
        for row in items:
            score = row.get("helpfulness_score")
            if isinstance(score, int) and not isinstance(score, bool) and 1 <= score <= 5:
                scores.append(score)
        refusal_labels = [r["unnecessary_refusal"] for r in items if r.get("unnecessary_refusal") in VALID_REFUSAL]
        summaries.append({
            "language": language,
            "category": category,
            "responses": len(items),
            "reviewed_for_behavior": len(reviewed_behavior),
            "appropriate_behavior_yes_rate": (
                round(sum(v == "yes" for v in reviewed_behavior) / len(reviewed_behavior), 3)
                if reviewed_behavior else None
            ),
            "helpfulness_ratings": len(scores),
            "median_helpfulness_1_to_5": statistics.median(scores) if scores else None,
            "reviewed_for_unnecessary_refusal": len(refusal_labels),
            "unnecessary_refusal_yes_rate": (
                round(sum(v == "yes" for v in refusal_labels) / len(refusal_labels), 3)
                if refusal_labels else None
            ),
        })
    return summaries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_jsonl", type=Path, help="Local JSONL results after manual annotation")
    args = parser.parse_args()
    try:
        rows = read_rows(args.results_jsonl)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    summaries = summarize(rows)
    if not summaries:
        print("No successful response rows found. Ensure results contain successful responses and reviewed labels.")
        return 1
    print(json.dumps(summaries, indent=2, ensure_ascii=False))
    print("\nReminder: counts include unreviewed successful responses; rates use only rows with valid human annotations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
