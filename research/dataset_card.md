# Dataset card

## Summary

`dataset/evaluation_prompts.jsonl` is an initial, manually authored pilot set for exploring safe helpfulness in English (`en`) and Turkish (`tr`) cybersecurity prompts.

## Contents

- 24 prompt records.
- 12 paired scenarios, each with one English and one Turkish prompt.
- Three categories: `defensive`, `dual_use`, and `harmful`.
- Stable record IDs and scenario pair IDs.

## Intended use

- Small-scale, exploratory evaluation of model behavior on these constructed prompts.
- Testing the project's dataset validation, collection, and manual annotation workflow.
- Demonstrating a reproducible research procedure before a larger, reviewed study.

## Out-of-scope uses

- Claiming the prompts represent all cybersecurity users or all English/Turkish language use.
- Using the dataset as a complete safety certification or model ranking benchmark.
- Generalizing to models, languages, settings, or tasks that were not tested.

## Creation and review

The prompts were authored specifically for this repository and paired by intended scenario. They have not been independently validated by bilingual subject-matter experts. Translation equivalence, difficulty balance, and cultural/linguistic naturalness may vary. Before drawing strong conclusions, seek bilingual review and revise the dataset with documented versioning.

## Safety considerations

Harmful prompts describe unsafe goals at a high level without including operational instructions for carrying them out. The dataset uses no real targets, credentials, personal information, or live infrastructure.

## Known limitations

- Small sample size and convenience sampling.
- Single authored translation per language, without independent translation adjudication.
- Model outputs can vary over time and across API settings.
- Human scoring is subjective and requires a clear rubric; inter-rater agreement should be measured where possible.
- The initial dataset does not by itself establish statistical power or representativeness.

## Update policy

When prompts change, retain stable IDs where the underlying scenario remains the same, record the change in version history, and describe material changes in evaluation reports. Avoid comparing scores across materially different dataset versions without qualification.
