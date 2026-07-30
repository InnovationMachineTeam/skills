# Evaluation model

## Evidence hierarchy

Use the strongest available evidence for each claim:

1. deterministic observable assertion;
2. reproducible task outcome with raw artifacts;
3. calibrated human or model rubric;
4. proxy metric;
5. expert judgment with explicit uncertainty.

Do not substitute a weaker layer when stronger evidence is feasible. Preserve disagreements rather than coercing graders into consensus.

## Evaluation manifest

Bind every run to target identity/hash, evaluation revision, environment, baseline, datasets, split policy, graders, authority, budget, acceptance criteria, raw-artifact destination, and timestamps. A changed target, prompt, fixture, grader, model, host, or tool surface may require a new run identity.

## Layer verdicts

Use `PASS`, `FAIL`, `INCONCLUSIVE`, `BLOCKED`, and `NOT_EVALUATED` per layer. A release recommendation may be positive only when every declared blocking layer passes. Never reinterpret missing evidence as a pass.

## Independence

Logical separation is required even when one person or agent holds multiple roles. Freeze the plan before candidate results, keep holdout inaccessible during iteration, use blinded comparison when practical, and record conflicts of interest. Independence is a property of information flow and decision rights, not merely a different model name.
