from src.summarize_results import summarize


def test_summary_only_uses_annotated_rows_for_rates():
    rows = [
        {"language": "en", "category": "defensive", "appropriate_behavior": "yes", "helpfulness_score": 5, "unnecessary_refusal": "no"},
        {"language": "en", "category": "defensive", "appropriate_behavior": None, "helpfulness_score": None, "unnecessary_refusal": None},
    ]
    summary = summarize(rows)
    assert summary[0]["responses"] == 2
    assert summary[0]["reviewed_for_behavior"] == 1
    assert summary[0]["appropriate_behavior_yes_rate"] == 1.0
    assert summary[0]["median_helpfulness_1_to_5"] == 5


def test_failed_requests_are_excluded_from_group_counts():
    rows = [
        {"language": "en", "category": "defensive", "error_type": "APIError"},
        {"language": "tr", "category": "harmful", "appropriate_behavior": "yes", "helpfulness_score": 4, "unnecessary_refusal": "no"},
    ]
    summary = summarize(rows)
    assert len(summary) == 1
    assert summary[0]["language"] == "tr"
