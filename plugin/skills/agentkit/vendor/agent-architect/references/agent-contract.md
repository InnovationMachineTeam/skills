# Individual agent contract

## Required decisions

- stable identity, version, accountable owner and risk tier;
- observable mission and explicit non-goals;
- typed inputs, outputs and error/handoff envelopes;
- model requirements and fallback/escalation policy;
- allowlisted tools, permissions, data and network boundaries;
- immutable definition versus mutable runtime state;
- memory source, provenance, retention and deletion;
- runtime loop, budgets, stop, retry and recovery;
- human approval and unavailable-approver behavior;
- telemetry, evaluation, shadow/canary, rollback and retirement;
- documentation contract and public/private capability bindings.

Do not use a separate agent when a mode, workflow step, tool or deterministic
script has the same owner, context, permissions and completion criteria.

## Boundary handoffs

- multiple independently owned roles or workspaces → `agent-team-architect`;
- platform planes and reconciliation → `agent-os-architect`;
- frozen release evidence → `agent-evaluator`;
- registration, rollout or retirement → `agent-manager`.
