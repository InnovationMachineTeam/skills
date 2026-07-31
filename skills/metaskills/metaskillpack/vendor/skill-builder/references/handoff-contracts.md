# Specialist handoff contracts

Every handoff must be bounded and evidence-bearing.

## Common input envelope

```json
{
  "target": "exact path, source, or identity",
  "objective": "observable phase outcome",
  "evidence": ["artifact or locator"],
  "scope": ["allowed source or file"],
  "preserve": ["behavior, consumers, permissions"],
  "authority": {"read": true, "write": false, "external": false},
  "required_output": ["artifact and decision"],
  "forbidden": ["side effect or inference"]
}
```

## Specialist outputs

| Specialist | Required decision or artifact | Builder must verify |
|---|---|---|
| `skill-scout` | opportunity manifest and one build/no-build decision per candidate | coverage, evidence, uncertainty, no mutation |
| `skill-harvester` | inventory, candidates or `SKILL_CONTEXT.md` with provenance | locators, rights, duplicates, contradictions, no source mutation |
| `skill-architect` | skill bundle, classification, tests, validation evidence | exact files, official validation, functional and forward evidence |
| `skill-evaluator` | versioned plan/suite/run manifest, raw evidence, layered verdict and release recommendation | target hash, split integrity, environment, baselines, blocking layers, comparability, no candidate mutation |
| `skill-doctor` | health state, root cause, reproduction and recovery result | original case rerun, residual risk, repair authority |
| `skill-optimizer` | baseline, hypothesis, before/after and acceptance decision | comparable metric, preserved invariants, neighbor regressions |
| `skill-refactor` | boundary decision, topology plan and migration evidence | approvals, trigger/resource ownership, consumers, rollback |
| `skill-manager` | inventory or lifecycle manifest and verified host state | provenance, versions, discovery, conflicts, rollback |
| `optimize-prompts` | prompt or audit, resolved conflicts and evals | authority preservation, adversarial cases, no unauthorized deployment |

## Rejection and inconclusive results

A specialist may return `reject`, `keep separate`, `keep ad hoc`, `unverified`, or `inconclusive`. Preserve the decision. Do not reinterpret it as permission to advance. A later phase may proceed only if it has an independent valid entry condition and does not rely on the failed gate.

## No hidden answer leakage

For forward tests or independent review, pass the artifact and realistic task. Do not pass the suspected defect, intended patch, ideal route, expected answer, or previous score unless the evaluation explicitly measures response to that information.

## Evaluation handoffs

- Architect, doctor, optimizer, and refactor hand a new immutable candidate revision to evaluator; they do not mark their own work release-ready.
- Evaluator sends reproducible failures to doctor, improvement opportunities to optimizer, boundary collisions to refactor, and a layered release gate to manager.
- Manager owns activation and rollback state. An evaluator `PASS` is evidence for a release decision, not deployment authority.
- After any repair or optimization, rerun the affected cases plus frozen regression and holdout gates. Never overwrite the baseline or reveal holdout expected answers to the mutating specialist.
