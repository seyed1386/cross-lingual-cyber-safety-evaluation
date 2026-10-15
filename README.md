# Cross-Lingual Cyber Safety Evaluation

A small, reproducible research scaffold for evaluating how an AI assistant handles cybersecurity-related requests in English and Turkish.

> **Project status:** initial research scaffold. The prompts, evaluator, and tests are included; no model evaluations or empirical findings have been produced yet. Do not cite this repository as completed research until experiments are run and reviewed.

## Research question

Does an AI assistant respond consistently and safely to equivalent cybersecurity requests in English and Turkish, while remaining helpful on legitimate defensive tasks?

## Scope

The initial dataset contains paired English/Turkish scenarios in three categories:

- `defensive`: legitimate defensive work where helpful, safe guidance is expected.
- `dual_use`: authorized, bounded work where the assistant should remain within a safe scope.
- `harmful`: requests to facilitate harm, where the assistant should not provide enabling instructions and should redirect safely.

This is a pilot dataset written for this project, not a validated benchmark or an exhaustive sample of real users. The prompts do not target real systems and avoid operational instructions for wrongdoing.

## Repository structure

```text
README.md
research/
  research_questions.md
  methodology.md
  scoring_rubric.md
  dataset_card.md
dataset/
  evaluation_prompts.jsonl
src/
  __init__.py
  validate_dataset.py
  evaluate.py
  summarize_results.py
tests/
  test_dataset.py
  test_scoring.py
results/
  README.md
requirements.txt
pyproject.toml
```

## Quick start (no API calls)

Python 3.10 or newer is recommended.

```bash
python -m src.validate_dataset
python -m pytest
```

Both commands run locally and do not call any model API.

## Optional API evaluation

The evaluator is deliberately non-networked unless you explicitly enable live mode. Live API calls may incur charges, so wait until you have approved credits or understand your account's billing setup.

1. Install dependencies: `python -m pip install -r requirements.txt`
2. Set your API key in an environment variable named `ANTHROPIC_API_KEY`. Never commit the key or paste it into source code.
3. Choose a model ID currently available to your account from Anthropic's official model documentation.
4. Start with a tiny pilot and explicitly confirm that you intend to send billable API requests:

```bash
python -m src.evaluate --live --confirm-api-cost --model YOUR_MODEL_ID --limit 2
```

The command requires all three safety controls: `--live`, `--confirm-api-cost`, and an explicit `--limit`. The tool stores raw responses locally in `results/runs/`, which is git-ignored by default. Review outputs before sharing them.

Official model information: https://docs.anthropic.com/en/docs/about-claude/models/overview

## Manual review and reporting

The API runner does not automatically decide whether a response is safe or helpful. Each result includes blank annotation fields for a human reviewer. Annotate each row using the rubric in `research/scoring_rubric.md`, then run:

```bash
python -m src.summarize_results path/to/annotated_results.jsonl
```

Report the model ID, evaluation date, dataset version, number of examples, annotation procedure, limitations, and any exclusions. Do not report a benchmark score before annotating actual outputs.

## Research integrity and safety

- No real targets, credentials, or private information are needed.
- The dataset is designed for controlled text-only evaluations.
- Do not attempt unauthorized testing or request access to non-public models.
- Follow the model provider's usage policies and terms.
- Clearly separate hypotheses, plans, observed outputs, and conclusions.
- Avoid claiming that a small pilot proves broad model safety or language-wide performance.

## Reproducibility

The prompt IDs and pair IDs are stable within this pilot dataset. Future edits should be versioned and documented. Keep raw output files and API keys out of public commits unless results have been reviewed and intentionally cleared for release.
