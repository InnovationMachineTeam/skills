# Agent opportunity decision: agentkit release steward

Decision: `AGENT_JUSTIFIED` as an evaluation-only candidate.

The repository currently coordinates donor locks, maturity evidence, generated
marketplaces, registry hashes, rollback and release reports across multiple
validators. A deterministic release script remains responsible for generation
and validation, while one bounded agent may interpret conflicting evidence,
stop on failed gates and prepare a reviewable release decision.

Non-goals: publishing, installing, activating, changing donors, bypassing
review, choosing product scope, or replacing deterministic validators.

Coverage check: `agent-builder` coordinates agent lifecycle work but does not
own marketplace release judgment; `skill-marketplace-manager` governs
marketplaces but not the agentkit donor maturity ledger. The candidate is kept
outside the registry until evaluation and explicit lifecycle approval.
