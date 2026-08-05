---
name: agent-skill-mapper
description: Maps governed public and owner-private skills or commands to existing agents using mission fit, permissions, trust, context cost, evidence and capability budgets. Use when auditing agent capabilities, reconciling agent definitions with registries or skills-lock files, recommending versioned bindings, detecting gaps or excessive tool access, or preparing a controlled mapping update. Read only by default. Do not create agents or skills, promote private capabilities, silently edit agent definitions, or operate the team; route missing capability creation to the relevant architect and team design changes to agent-team-architect.
metadata:
  version: "1.0.3"
---

# Map Skills to Agents

Produce the smallest evidence-backed capability set for each registered agent.
Treat a skill binding as an authority and context decision, not keyword matching.

## Establish inventory and authority

Locate agent definitions, `docs/AGENT-ASSET-REGISTRY.json`,
`docs/AGENT-SKILLS-MAP.json`, public skill roots, agent-private capability roots
and optional `skills-lock.json` files. Record revisions and unresolved sources.
Do not infer write authority from a request to analyze or recommend.

Read [references/matching-contract.md](references/matching-contract.md) and
[references/registry-and-mutation.md](references/registry-and-mutation.md).

## Score candidates through hard gates

For every role-capability pair evaluate mission and trigger fit, expected task
frequency, input/output contract, host compatibility, provenance, lifecycle,
trust, tools, permissions, data classes, side effects, evidence and context cost.

Reject a candidate before scoring when it violates ownership, permissions,
trust, host or lifecycle constraints. A private skill or command may have exactly
one consumer: its owning agent. Never map it to another agent; recommend public
promotion through an explicit architecture workflow instead.

Compare against inline instructions, private commands, tools/scripts, existing
public skills and no binding. Prefer the least powerful adequate option. Enforce
each agent's capability budget and expose redundant, conflicting or unused
bindings.

## Decide and explain

Use `MATCH`, `CONDITIONAL`, `GAP`, `CONFLICT` or `REJECT`. Every recommendation
must cite evidence and exact versions, explain alternatives and risks, and state
whether an adapter, evaluation or approval is required. Ambiguous or missing
inventory yields `RESEARCH_REQUIRED`, not a guessed mapping.

Validate the machine-readable proposal before presenting it:

```bash
python3 scripts/validate_mapping.py mapping-proposal.json registry.json
```

## Apply only an authorized transaction

Analysis is read-only. If the user explicitly authorizes mutation, prepare one
transaction with expected registry/map revisions, an exact write-set, backups,
validation and rollback. Bump every changed agent's SemVer according to the
declared policy, update definitions and map together, preserve provenance and
generate host adapters rather than duplicating canonical policy.

Never activate a mapping, install dependencies, publish public assets or broaden
permissions unless those actions were explicitly authorized and independently
validated.

## Complete

Report inventory coverage, per-agent decisions, gaps/conflicts, rejected
candidates, capability budget, version changes, validation evidence, residual
risks and the next responsible workflow.
