---
name: agent-builder
description: Orchestrates complete evidence-backed workflows for one agent or subagent across agent-scout, agent-context, agent-architect, agent-evaluator, agent-doctor, agent-optimizer, agent-refactor and agent-manager. Use when creating, researching, evaluating, repairing, improving, refactoring, recovering or governing an individual agent through multiple phases, or when the correct specialist chain must be inferred. Prefer a direct specialist for one bounded phase. Do not design or run teams, build Agentic OS, imitate missing specialists, activate by assumption, or continue across approval, mutation or lifecycle gates without authority.
metadata:
  version: "1.0.1"
---

# Orchestrate One-Agent Workflows

Act as a thin control plane. Select the smallest scenario that proves the user's
outcome and preserve specialist boundaries, immutable candidates and independent
evaluation.

## Verify companions and choose one scenario

Read [references/skill-dependencies.md](references/skill-dependencies.md) and
[references/scenario-catalog.md](references/scenario-catalog.md). Block only an
affected route when a required companion is unavailable; never imitate it.

Supported scenarios: `full-lifecycle`, `create-from-spec`, `research-to-agent`,
`evaluate-agent`, `repair-agent`, `optimize-agent`, `compare-and-refactor`,
`incident-recovery`, `portfolio-governance` and `resume`.

Route team outcomes to `agent-team-manager` and Agentic OS outcomes to the
responsible `agent-os-*` workflow. If one phase satisfies the request, invoke
the specialist directly.

## Maintain bounded state

For consequential or resumable work create a phase ledger with goal, scope,
authority, acceptance, exact asset versions, dependencies, artifacts,
approvals, budgets, checkpoints, rollback and evidence. Validate it:

```bash
python3 scripts/validate_agent_build_state.py agent-build-state.json
```

Each handoff contains exact target, objective, evidence, allowed scope,
preserved invariants, authority, required output and forbidden effects. Inspect
returned artifacts; a specialist completion message is not evidence.

## Apply gates

Use worth/minimal-architecture, definition/threat, documentation, independent
evaluation, policy/approval, shadow/canary, host read-back, observation,
rollback and retirement gates as applicable. Do not pass holdout answers to
mutating specialists.

The architect owns the documentation contract. The builder creates only its
approved roots and artifacts; it must not invent an absent contract or create an
empty docs taxonomy.

Stop on changed authority, stale revisions, unavailable specialist, unsafe
partial effect, failed blocker, exhausted budget or human checkpoint. Preserve a
resumable checkpoint.

Return scenario, phase ledger, artifacts, per-gate evidence, mutations,
external actions, lifecycle state, waivers, residual risk and next safe action.
