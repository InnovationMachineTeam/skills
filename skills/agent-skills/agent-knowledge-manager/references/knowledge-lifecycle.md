# Knowledge lifecycle

Pipeline:

`candidate -> sanitize -> verify -> classify -> approve -> publish -> retrieve -> revalidate -> supersede/archive`

Candidate discovery never grants trust. The curator verifies sources, scope,
sensitivity, freshness and contradictions. Approved knowledge can be published;
stale or revoked knowledge remains visible for history but is excluded from
automatic application.

Required metadata: stable `doc://` ID, type, status, accountable owner, SemVer,
updated/review dates, source refs, related refs, tags, sensitivity and agent
access. Facts and interpretations are separate. Decisions are append-mostly and
use `supersedes`; conflicts receive their own page.

Never store secrets, raw chain-of-thought, arbitrary tool dumps or volatile
runtime state. Session learnings become durable only after sanitization and
verification.
