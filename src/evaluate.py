"""Run a small, explicitly confirmed Claude API evaluation pilot."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.validate_dataset import DEFAULT_DATASET, load_jsonl, validate_records

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "results" / "runs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the dataset by default. Live API calls require --live, "
            "--confirm-api-cost, an explicit --limit, and --model."
        )
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--live", action="store_true", help="Actually send API requests")
    parser.add_argument(
        "--confirm-api-cost", action="store_true",
        help="Explicitly acknowledge that live requests may incur charges"
    )
    parser.add_argument("--model", help="Model ID available to your Anthropic API account")
    parser.add_argument("--limit", type=int, help="Maximum number of prompts to send; required for live mode")
    parser.add_argument("--max-tokens", type=int, default=500)
    return parser.parse_args()


def response_text(message: Any) -> str:
    parts = []
    for block in message.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "\n".join(parts).strip()


def main() -> int:
    args = parse_args()
    try:
        records = load_jsonl(args.dataset)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate_records(records)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if not args.live:
        print("Dry run only: no API requests were sent.")
        print(f"Would evaluate {len(records)} prompts from {args.dataset}.")
        print("To run a paid pilot, explicitly set --live --confirm-api-cost --model MODEL_ID --limit N.")
        return 0

    if not args.confirm_api_cost:
        print("Refusing live mode without --confirm-api-cost.", file=sys.stderr)
        return 2
    if not args.model:
        print("Live mode requires --model with a current model ID available to your account.", file=sys.stderr)
        return 2
    if args.limit is None or args.limit < 1:
        print("Live mode requires an explicit positive --limit.", file=sys.stderr)
        return 2
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Set ANTHROPIC_API_KEY in your environment; never place it in source code.", file=sys.stderr)
        return 2
    if args.max_tokens < 1:
        print("--max-tokens must be positive.", file=sys.stderr)
        return 2

    try:
        from anthropic import Anthropic
    except ImportError:
        print("Missing dependency. Install requirements.txt first.", file=sys.stderr)
        return 2

    selected = records[: min(args.limit, len(records))]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = args.output_dir / f"run_{stamp}.jsonl"
    client = Anthropic(api_key=api_key)

    with output_path.open("w", encoding="utf-8") as stream:
        for index, record in enumerate(selected, start=1):
            print(f"[{index}/{len(selected)}] Evaluating {record['id']} ({record['language']})...")
            try:
                message = client.messages.create(
                    model=args.model,
                    max_tokens=args.max_tokens,
                    messages=[{"role": "user", "content": record["prompt"]}],
                )
                row = {
                    "record_id": record["id"],
                    "pair_id": record["pair_id"],
                    "language": record["language"],
                    "category": record["category"],
                    "model": args.model,
                    "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "response": response_text(message),
                    "input_tokens": getattr(message.usage, "input_tokens", None),
                    "output_tokens": getattr(message.usage, "output_tokens", None),
                    "stop_reason": getattr(message, "stop_reason", None),
                    # Human annotations remain blank until reviewed using research/scoring_rubric.md.
                    "appropriate_behavior": None,
                    "helpfulness_score": None,
                    "unnecessary_refusal": None,
                    "reviewer_notes": None,
                }
            except Exception as exc:  # Keep the pilot moving, but record the failure.
                row = {
                    "record_id": record["id"],
                    "pair_id": record["pair_id"],
                    "language": record["language"],
                    "category": record["category"],
                    "model": args.model,
                    "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "appropriate_behavior": None,
                    "helpfulness_score": None,
                    "unnecessary_refusal": None,
                    "reviewer_notes": None,
                }
                print(f"Request failed for {record['id']}: {type(exc).__name__}: {exc}", file=sys.stderr)
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()

    print(f"Saved local results to: {output_path}")
    print("Review responses manually before reporting findings or publishing results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
