"""Validate the project's JSONL evaluation dataset using only the standard library."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

DEFAULT_DATASET = Path(__file__).resolve().parents[1] / "dataset" / "evaluation_prompts.jsonl"
REQUIRED_FIELDS = {
    "id", "pair_id", "language", "category", "prompt", "expected_behavior"
}
VALID_LANGUAGES = {"en", "tr"}
VALID_CATEGORIES = {"defensive", "dual_use", "harmful"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read JSONL with useful line-numbered parse errors."""
    records: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"Cannot read dataset {path}: {exc}") from exc

    for line_number, line in enumerate(lines, start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at line {line_number}: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"Line {line_number} must contain a JSON object")
        records.append(value)
    return records


def validate_records(records: list[dict[str, Any]]) -> list[str]:
    """Return validation errors; an empty list means the dataset passed checks."""
    errors: list[str] = []
    if not records:
        return ["Dataset has no records"]

    seen_ids: set[str] = set()
    pairs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    categories = Counter()
    languages = Counter()

    for index, record in enumerate(records, start=1):
        missing = REQUIRED_FIELDS - record.keys()
        if missing:
            errors.append(f"Record {index} is missing fields: {', '.join(sorted(missing))}")
            continue

        record_id = record["id"]
        if not isinstance(record_id, str) or not record_id.strip():
            errors.append(f"Record {index} has an empty/non-string id")
        elif record_id in seen_ids:
            errors.append(f"Duplicate id: {record_id}")
        else:
            seen_ids.add(record_id)

        if record["language"] not in VALID_LANGUAGES:
            errors.append(f"{record_id}: invalid language {record['language']!r}")
        if record["category"] not in VALID_CATEGORIES:
            errors.append(f"{record_id}: invalid category {record['category']!r}")
        if not isinstance(record["prompt"], str) or not record["prompt"].strip():
            errors.append(f"{record_id}: prompt must be a non-empty string")
        if not isinstance(record["expected_behavior"], str) or not record["expected_behavior"].strip():
            errors.append(f"{record_id}: expected_behavior must be a non-empty string")

        categories[record["category"]] += 1
        languages[record["language"]] += 1
        pairs[str(record["pair_id"])].append(record)

    for pair_id, pair_records in sorted(pairs.items()):
        pair_languages = [r.get("language") for r in pair_records]
        if len(pair_records) != 2 or set(pair_languages) != VALID_LANGUAGES:
            errors.append(
                f"Pair {pair_id!r} must contain exactly one English and one Turkish record; "
                f"found {pair_languages}"
            )
        if len({r.get("category") for r in pair_records}) > 1:
            errors.append(f"Pair {pair_id!r} has inconsistent categories")

    if not errors:
        print(f"Dataset valid: {len(records)} records, {len(pairs)} paired scenarios")
        print("Languages: " + ", ".join(f"{key}={languages[key]}" for key in sorted(languages)))
        print("Categories: " + ", ".join(f"{key}={categories[key]}" for key in sorted(categories)))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args()
    try:
        records = load_jsonl(args.dataset)
    except ValueError as exc:
        parser.error(str(exc))
    errors = validate_records(records)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
