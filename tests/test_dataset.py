import json
from pathlib import Path

from src.validate_dataset import DEFAULT_DATASET, load_jsonl, validate_records


def test_project_dataset_validates():
    records = load_jsonl(DEFAULT_DATASET)
    assert validate_records(records) == []


def test_dataset_has_english_and_turkish_pairs():
    records = load_jsonl(DEFAULT_DATASET)
    groups = {}
    for record in records:
        groups.setdefault(record["pair_id"], set()).add(record["language"])
    assert groups
    assert all(languages == {"en", "tr"} for languages in groups.values())


def test_duplicate_ids_are_detected():
    records = load_jsonl(DEFAULT_DATASET)[:2]
    records[1] = dict(records[1], id=records[0]["id"])
    assert any("Duplicate id" in error for error in validate_records(records))


def test_malformed_jsonl_is_reported(tmp_path: Path):
    path = tmp_path / "bad.jsonl"
    path.write_text('{not json}\n', encoding="utf-8")
    try:
        load_jsonl(path)
    except ValueError as exc:
        assert "line 1" in str(exc).lower()
    else:
        raise AssertionError("Malformed JSONL should fail")
