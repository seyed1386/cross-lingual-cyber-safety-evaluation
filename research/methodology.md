# Methodology

## Study design

A paired, text-only exploratory evaluation of English and Turkish prompts. Each scenario has a stable `pair_id`; paired prompts are intended to express equivalent user intent in the two languages. The initial dataset is a convenience sample authored for this pilot and has not been validated by independent bilingual reviewers.

## Categories

- `defensive`: benign security analysis and protective actions.
- `dual_use`: legitimate activity that could be misused; safe, bounded guidance is expected.
- `harmful`: an explicitly harmful request; the model should avoid enabling details and redirect to a safe alternative.

## Procedure

1. Validate the JSONL dataset and check required fields and pair coverage.
2. Record the exact model ID, evaluation date, dataset revision, and run configuration.
3. Start with a small pilot. Do not send API requests until cost and account access are understood.
4. Use the same API settings for paired prompts. Do not add a safety steering system prompt to the tested model, because that would change the behavior under observation. Use the same neutral request structure for every item.
5. Store responses locally. Do not automatically label model responses as safe or unsafe.
6. Have a reviewer apply the rubric to each response. When feasible, use two reviewers who do not see the language/category labels during first-pass scoring, and report disagreements.
7. Summarize descriptive results by language and category. For paired comparisons, compare the corresponding `pair_id` outcomes.
8. Report all exclusions, missing outputs, errors, deviations, and limitations.

## API cost and data handling

The evaluator requires explicit live-mode and cost-confirmation flags and an explicit maximum item count. Use a small pilot first. Store API keys only in environment variables. Raw response files are git-ignored by default because responses may be unreviewed. Inspect output before publishing; never include secrets, private data, or real targets.

## Analysis plan

For each language/category combination, report the number of reviewed responses, median helpfulness score, proportion marked as appropriate behavior, and proportion marked as unnecessary refusal. Report denominators and missing annotations. Use matched English/Turkish pairs for language comparisons. This pilot is descriptive; do not claim causal effects or statistical significance without a suitable pre-specified analysis and sufficient data.

## Ethics and responsible use

No real-world target testing is needed. Harmful prompts are phrased at a high level and do not request or include procedural attack instructions. Follow the API provider's usage policies. This research does not seek exceptions to those policies.
