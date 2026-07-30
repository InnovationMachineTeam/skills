# Snapshot and claims schema

## Snapshot root

```json
{
  "schema_version": 1,
  "snapshot_id": "stable-run-id",
  "created_at": "ISO-8601",
  "registry_hash": "sha256:...",
  "sources": []
}
```

Each source record contains:

- `source_id`;
- `status` — `available`, `unavailable`, `partial`, or `moved`;
- `checked_at`;
- `canonical_locator`;
- optional `resolved_locator`, `revision`, `etag`, `last_modified`, and `content_hash`;
- `semantic_fingerprint` derived from material headings and claims;
- comparison-only `semantic_status` — `changed`, `unchanged`, or `unknown`; keep this separate from retrieval `status`;
- `claims`;
- `errors` and `coverage_notes`.

## Claim record

```json
{
  "claim_id": "stable-topic-id",
  "statement": "Concise paraphrase",
  "scope": "portable|openai|anthropic|client|enterprise|exemplar",
  "locator": "heading, line, anchor, or repository path",
  "kind": "normative|recommendation|constraint|observation",
  "confidence": "high|medium|low"
}
```

Do not store long copyrighted passages. A semantic fingerprint should be deterministic from normalized claim IDs, statements, scopes, and locators. Hashes establish content identity, not correctness.

An unavailable or partial source has `semantic_status: unknown`, including when it was just added to the registry. Registry addition is tracked separately and never proves new guidance without retrieved claims.

Reject snapshots with an unknown retrieval status, missing root registry hash or timestamp, missing source locator/check time, missing claims/errors/coverage fields, or an available source without a valid semantic fingerprint. A reconciliation artifact binds both `snapshot_id` and the exact snapshot and registry hashes; its `unverified_sources` must match all unavailable or partial snapshot records.

## Reconciliation record

For every affected practice store practice ID, old statement, new statement, status, supporting and conflicting source IDs, applicability, rationale, action, validation effect, and reviewer/approval when required.
