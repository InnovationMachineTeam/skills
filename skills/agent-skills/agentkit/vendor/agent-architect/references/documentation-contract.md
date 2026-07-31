# Documentation contract

Discover the existing project convention first. Preserve it unless an explicit
migration updates all consumers. For a new project, use:

- `docs/agents/specs/` for agent definitions;
- `docs/agents/contexts/` for design context;
- `docs/agents/evals/` for evaluation artifacts;
- `docs/agents/operations/` for runbooks;
- `docs/agents/changes/` for version changes;
- `docs/decisions/architecture/` for ADRs.

Declare read/write roots, artifact path pattern, owner, reviewers, consumers,
source-of-truth status, decision authority, freshness, supersession, indexes and
validation. Create only directories needed by approved artifacts. Agents may
propose consequential decisions; accountable humans or policy owners accept
them. Never edit generated projections directly.

Reject absolute paths, empty segments, `.`/`..`, traversal and normalized paths
outside `docs/`. Every artifact declares owner, reviewers, at least one
consumer, source-of-truth status, nullable decision authority, freshness and
nullable supersession.

For a software architect, prefer an owner-private ADR capability if it has one
consumer. Assess public promotion only after independent reuse exists.
