# Evaluation Methods

## Contents

- Evaluation layers
- Metrics
- Judges and assertions
- Forward-testing

## Evaluation layers

1. Structural validity and links.
2. Routing precision, recall, ambiguity, and collisions.
3. Functional outcome and artifact correctness.
4. Script and tool failure behavior.
5. Security and authority adversarial cases.
6. Portability across declared hosts.
7. Regression against last-known-good.

## Metrics

Select only metrics tied to the hypothesis:

- task success and critical failure rate;
- routing precision, recall, and weighted error cost;
- validation failures and script exit behavior;
- false completion and partial-success accuracy;
- unsafe action or data-exposure rate;
- tokens, loaded lines, latency, tool calls, retries, and cost;
- cross-host pass rate.

## Judges and assertions

Use deterministic assertions for files, schemas, exit codes, links, required sections, prohibited actions, and exact invariants. Use rubrics or independent judges for semantic quality. Calibrate with examples and allow multiple valid formulations.

Do not let the same author context serve as the only independent judge. Blind evaluators to the intended fix when possible. Report disagreement and untested surfaces.

## Forward-testing

Pass the candidate skill and a realistic task to fresh context. Do not include the expected answer, suspected bug, or change rationale. Use separate fixtures and destinations to avoid contamination. Inspect raw artifacts and traces before accepting the evaluator's summary.

