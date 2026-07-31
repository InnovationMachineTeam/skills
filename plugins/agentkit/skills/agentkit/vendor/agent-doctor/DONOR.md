---
name: agent-doctor
description: Diagnoses unhealthy or broken behavior in one agent or subagent, reproduces symptoms from definitions and traces, identifies a root cause, applies an explicitly authorized minimal repair to a new candidate revision, and verifies recovery. Use for routing failures, tool misuse, permission denials, loops, stale context, memory poisoning, document drift, runtime errors or regressions in an individual agent. Do not optimize a healthy agent, redesign teams or Agentic OS, change mission or authority under a repair label, edit production state without approval, or declare release readiness.
metadata:
  version: "1.0.0"
---

# Diagnose One Agent

Preserve the failing definition, trace, environment and evidence before any
change. A symptom is not a root cause; a plausible patch is not recovery proof.

Read [references/skill-dependencies.md](references/skill-dependencies.md) and
make missing independent evaluation support visible without fabricating it.

## Gate the case

Resolve exact agent/version/hash, observed versus expected behavior, first known
bad version, environment, tools, permissions, state, documents, reproduction,
impact and mutation authority. Return `INSUFFICIENT_EVIDENCE` when the symptom
cannot be reproduced or isolated.

Read [references/diagnosis-contract.md](references/diagnosis-contract.md).
Classify the leading fault surface: routing/mission, prompt/context, tool/schema,
permission/policy, model compatibility, loop/budget, state/memory,
documentation, dependency, runtime or environment.

## Diagnose scientifically

1. Freeze the reproduction and baseline.
2. Build competing hypotheses with discriminating observations.
3. Run the cheapest safe tests first.
4. Identify the smallest causal boundary supported by evidence.
5. Propose the minimal repair, affected invariants and rollback.
6. Obtain exact write/runtime authority before mutation.
7. Create a new candidate revision; never overwrite the baseline.
8. Rerun the original failure, neighboring regressions and recovery case.

For document failures, verify canonical path, owner, freshness, provenance,
links, decision authority and code/docs parity. Do not reorganize the docs tree
under a repair label; route a boundary migration to `agent-refactor`.

## Complete

Return `REPRODUCED`, `REPAIRED`, `NOT_REPRODUCED`, `INCONCLUSIVE`, `BLOCKED` or
`ROLLED_BACK` with evidence, root cause, changed files/state, new version,
recovery proof and residual risk. Hand the immutable repaired candidate to
`agent-evaluator`; do not activate it.
