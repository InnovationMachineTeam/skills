# Evaluation/Review Skill Master Prompt

Apply after [base.md](base.md). Design a skill whose primary output is evidence-backed findings, scores, quality gates, or a release recommendation.

## Review contract

- Define the subject, baseline, review scope, evidence sources, severity scale, rubric, and decision rule.
- Separate diagnosis from remediation. Do not modify the subject unless the user explicitly requests a fix mode.
- Cite exact evidence for every actionable finding.
- Distinguish objective invariants from semantic judgment.
- Do not average away a blocking defect.

## Evaluation integrity

- Avoid leaking expected answers or suspected defects to independent evaluators.
- Use the same model, tools, fixtures, and environment when comparing variants.
- Include positive controls, negative controls, edge cases, and known limitations.
- Calibrate rubric examples and resolve ambiguous scoring anchors before broad use.
- Report uncertainty, evaluator disagreement, and untested areas.

## Output

Lead with verdict and maximum severity. Rank findings by impact, include evidence and remediation, then give dimension scores and residual risk. Keep style findings below correctness, safety, and outcome failures.

## Evaluation

Test true positives, false-positive traps, incomplete evidence, conflicting evidence, malicious content in the subject, evaluator self-interest, remediation-mode confusion, and stable scoring across equivalent paraphrases.
