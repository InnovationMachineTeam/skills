# Behavioral evaluation and graders

## Observable assertions

Prefer assertions on files, schemas, fields, citations, commands, tool calls, recipients, paths, side effects, refusal boundaries, recovery state, and completion conditions. Avoid exact full-text equality unless text identity is the requirement.

Use metamorphic tests when outputs should remain invariant under harmless transformations, property tests for broad input spaces, fuzzing for parser and boundary resilience, and mutation tests to verify that the suite detects meaningful defects.

## Rubrics

Define dimensions, anchored levels, blocking failures, evidence requirements, and aggregation rules before grading. Do not allow high style scores to offset data loss, unsafe action, fabricated evidence, or missed mandatory output.

## Model judges

Use model graders for scalable judgment only after checking prompt clarity, position/order bias, verbosity bias, self-preference, reference leakage, and sensitivity to irrelevant formatting. Prefer blinded pairwise comparisons for close candidates. Calibrate against deterministic labels or human adjudication and preserve judge identity and raw rationale.

## Human review

Use domain experts for subjective, consequential, or ambiguous outcomes. Record reviewer criteria and disagreement without exposing unnecessary private data. Sample across success and failure cases; do not review only cherry-picked outputs.
