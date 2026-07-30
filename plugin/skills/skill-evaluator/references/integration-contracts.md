# Integration contracts

## Ownership boundaries

| Specialist | Owns | Receives from evaluator |
|---|---|---|
| `skill-architect` | new skill architecture and creation | plan gaps, required eval assets, creation verdict |
| `skill-doctor` | defect diagnosis and verified repair | failing cases, raw reproduction, affected layer |
| `skill-optimizer` | measured healthy improvement | baseline, metrics, protected regressions, acceptance rule |
| `skill-refactor` | capability topology and migration | collision/composition evidence, consumer regressions |
| `skill-manager` | versions, activation, rollout, rollback, retirement | release gate, target hash, skipped layers, rollback evidence |
| `skill-builder` | phase orchestration and resumable state | evaluation manifest, verdicts, artifacts, next valid handoff |

## Input handoff

Require exact target, objective, claims, baseline, environment, authority, preserved invariants, required layers, budget, confidential data policy, acceptance gates, and forbidden side effects.

## Output handoff

Return evaluation/run IDs, target hash, environment, datasets, fixtures, raw artifacts, metrics, per-layer verdicts, failures, uncertainty, skipped gates, blocking regressions, and next evaluation trigger. A recommendation is not mutation or activation authority.

## Builder gates

- Creation: `skill-architect` → `skill-evaluator`; failed cases may route to `skill-doctor`, then back to evaluator.
- Optimization: evaluator baseline → `skill-optimizer` → evaluator comparison and holdout.
- Repair: `skill-doctor` reproduction/fix → evaluator regression and affected-layer verification.
- Refactor: `skill-refactor` staged topology → evaluator routing/coexistence/consumer E2E.
- Release: evaluator blocking layers pass → `skill-manager` verifies lifecycle state and rollback.

Never let the same mutable run state silently serve as baseline and candidate. Never advance because a specialist says its own work passed without independent evidence proportional to risk.
