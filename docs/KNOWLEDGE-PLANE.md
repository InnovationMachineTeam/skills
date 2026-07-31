# Project knowledge plane

`docs/` is curated project knowledge, not live runtime state. Canonical code,
specifications, decisions, runbooks and evidence keep their own authority; no
single document is the source of truth for every knowledge class.

## Lifecycle

New material enters `docs/knowledge/inbox/` as a candidate. A curator sanitizes,
verifies provenance, classifies sensitivity and freshness, resolves or records
contradictions, then publishes it to an atomic page or rejects it. Published
decisions are superseded rather than overwritten. Stale/revoked pages are
excluded from automatic agent use.

## Required frontmatter

```yaml
---
id: doc://knowledge/example
type: fact
status: candidate
owner: team-or-person
version: "1.0.0"
updated_at: 2026-07-31
review_at: 2026-10-31
sources: [source://example]
related: []
tags: [example]
sensitivity: internal
agent_access: read
---
```

Standard Markdown links are canonical. Optional Obsidian links are views only.
Never store secrets, raw chain-of-thought, arbitrary tool output, active leases
or heartbeats here.

## Generated projections

`docs/generated/knowledge-graph.json` is generated from `docs/knowledge/` and
must not be edited manually. It carries locators and hashes so drift and deletion
are detectable. Vector or external graph infrastructure requires a separate
measured architecture decision.
