# Context-engineering policy

Status: implemented candidate  
Owner: InnovationMachineTeam  
Reviewer: @stanislavus86  
Consumers: skill authors, metaskill maintainers, marketplace reviewers  
Last reviewed: 2026-08-03  
Review trigger: model-generation change, routing regression, or context-budget regression

## Decision

Canonical skills use progressive disclosure and capability-based execution
profiles. Model names and price tiers are not capability evidence.

- `standard` is available only after comparable evaluation demonstrates reliable
  planning, state tracking, tool recovery, instruction hierarchy and contract
  compliance.
- `constrained` is the default for unknown, mixed or simpler models. It uses
  one-phase-at-a-time execution, explicit schemas, checklists and assertions.
- A blocking miss in `standard` retries the current phase once with
  `constrained`; it does not weaken the gate or replay completed effects.

Both profiles preserve the same authority, safety, privacy, output, rollback
and Definition-of-Done contracts.

## Context placement

| Information | Location |
|---|---|
| trigger and differentiation | concise frontmatter description |
| route, invariants and completion | `SKILL.md` |
| conditional procedure | one-hop `prompts/` or `references/` resource |
| deterministic transformation | tested `scripts/` command |
| routing and behavior assertions | `evals/` |
| host-specific current facts | adapter, registry or current tool lookup |

Do not move text to a resource unless the runtime can avoid loading it for
unrelated routes.

## Hard-rule classification

Every `must`, `never`, `always`, `do not`, `require`, `reject`, `stop` or
equivalent rule should have one owner and one of these reasons:

1. `authority_safety` — permissions, secrets, external effects, publication,
   production, destructive operations, data boundaries or human approval;
2. `verification_recovery` — truthful completion, frozen evaluation, retries,
   rollback, partial failure or evidence preservation;
3. `deterministic_interface` — schema, state machine, hash, exit code or exact
   mechanical contract;
4. `judgment_candidate` — style or process preference without an evidenced
   high-cost failure.

The first three classes may remain strict. Rewrite a `judgment_candidate` as a
contextual default, bounded preference or evaluated decision table unless a
regression case justifies the absolute wording.

Run the portfolio audit with:

```bash
python3 scripts/audit_skill_context.py skills --format json
```

The audit is a review queue, not proof that any rule is safe to remove.

## Current implementation

Capability profiles and fallback eval cases are implemented in:

- `skills/agent-master/agent-master`;
- `skills/prompt-skills/prompt-master`;
- `skills/metaskills/skill-builder`.

The official Anthropic Claude 5 context-engineering article is registered as
`SRC-ANT-005` with `anthropic-claude-5` scope. It is not promoted to a portable
standard.
