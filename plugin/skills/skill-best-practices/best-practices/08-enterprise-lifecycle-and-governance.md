# Enterprise lifecycle and governance

Practice-ID: BP-GOV-001
Scope: enterprise
Status: current
Sources: SRC-ANT-002, SRC-ANT-003, SRC-OAI-002, SRC-EX-002
Last-rebuilt: 2026-07-30

## Registry and ownership

Track purpose, owner, reviewer, source, version, checksum, dependencies, compatibility, risk tier, security review, last evaluation, supported hosts/models, rollout, deprecation, and rollback. Store governance outside the portable runtime bundle when appropriate.

## Lifecycle

```text
plan → create → review → test → approve → deploy → monitor → iterate or deprecate
```

Separate author and reviewer for consequential skills. Require security, isolation, routing, behavior, and coexistence evidence before approval. Pin production versions, preserve last-known-good, verify checksums/provenance, stage rollout, and test rollback. Treat every material update as a reviewed release.

Platform distribution is not automatically cross-surface. Keep source-controlled canonical bundles and generate/deploy host adapters explicitly. Current API limits, retention, version formats, and deletion semantics are dynamic host facts.

## Portfolio scale

Start with narrow workflow skills, group by role, limit simultaneously active catalogs, measure recall as the portfolio grows, and consolidate only when evals prove equivalent behavior. Monitor activation, false activation, clarification, tool errors, validation failures, quality, tokens, latency, versions, feedback, and rollback without leaking sensitive data.
