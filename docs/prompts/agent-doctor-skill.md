# Master Prompt For The `agent-doctor` Skill

Apply [agent-documentation-contract.md](agent-documentation-contract.md)
when the symptom is tied to stale context, incorrect ownership, broken links,
code/docs drift, or an incorrect decision path. Repair only the proven cause and
do not rewrite the documentation architecture under the guise of repair.

Apply after [agent-skill-base.md](agent-skill-base.md). Create a diagnostic
skill that reproduces agent failure, localizes the root cause, proposes a
minimal repair, and proves recovery. It does not optimize a healthy agent and
does not change production without authorization.

## Modes

- `check` — health inventory without mutation;
- `diagnose` — reproduction and root-cause analysis;
- `repair` — minimal staged candidate after permission;
- `verify-recovery` — rerun original case + regressions;
- `compare-health` — baseline/candidate diagnostic comparison.

Default mode is read-only `diagnose`. A request like "why did it break?" is not
permission to fix it.

## Evidence preservation

Before making changes, preserve:

- symptom and expected/observed behavior;
- exact agent/model/tool/policy/memory versions;
- sanitized inputs, outputs, events, and trace IDs;
- environment, permissions, budgets, and timing;
- last-known-good and change history;
- reproduction steps and occurrence rate;
- affected users/assets and severity.

Do not diagnose from the agent's summary alone. Redact sensitive traces while
preserving diagnostic signals.

## Diagnostic taxonomy

Classify the primary failure domain:

- definition/instruction conflict;
- routing/intent/scope;
- context/retrieval/grounding;
- planning/loop/stop condition;
- tool schema/integration/permission;
- delegation/handoff/team coordination;
- state/memory/provenance/drift;
- model/runtime/version incompatibility;
- budget/latency/capacity;
- security/prompt injection/data handling;
- approval/policy/governance;
- observability/evidence gap;
- deployment/rollout/recovery.

Separate the trigger, contributing factor, and root cause. Do not accept a
correlation with the most recent change as causation without falsification.

## Scientific diagnosis

1. Record the minimal reproduction.
2. Form competing hypotheses.
3. Define a distinguishing prediction for each one.
4. Execute read-only/dry-run observations.
5. Falsify alternatives.
6. State confidence and missing evidence.
7. Propose a repair only after the root-cause gate.

If reproduction is impossible, return `INCONCLUSIVE` and an instrumentation plan,
not an invented cause.

## Repair safety

- Create a new immutable candidate revision.
- Change the minimum number of causally related components.
- Do not update prompt, model, tools, and memory simultaneously unless necessary.
- Preserve last-known-good and rollback.
- Policy, permissions, and risk tier are not weakened as a "fix."
- Production repair follows the normal manager/approval path.

## Recovery verification

Always run the original failure, neighboring cases, frozen regressions,
an adversarial case, and rollback. Verify that the symptom disappeared because
of the repair, not because of a changed environment or a hidden retry.

## Output

Return the health state, severity, reproduction, hypothesis ledger, root cause,
candidate diff, recovery evidence, regressions, residual risk, and handoff.
An unconfirmed hypothesis is not labeled as a fixed defect.
