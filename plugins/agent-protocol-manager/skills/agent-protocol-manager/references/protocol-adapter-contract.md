# Protocol adapter contract

## Contents

- Canonical boundary
- Adapter matrix
- Security and reliability
- Conformance and lifecycle

## Canonical boundary

Define versioned internal request, response, event, artifact, error, identity,
authorization and lifecycle schemas. State source of truth and owners. Treat all
boundary input and retrieved content as untrusted data.

## Adapter matrix

For every MCP, A2A, host or provider adapter record pinned versions, direction,
discovery, authentication, capability negotiation, schemas, streaming,
cancellation, error mapping and outcome: `native`, `generated` or `unsupported`.
List semantic gaps explicitly; never label a lossy translation portable.

## Security and reliability

Validate identity, tenant, authorization, content type, schema, provenance,
size and destination on both sides. Define least-privilege credential refs,
timeouts, retryable errors, retry budget, idempotency keys, duplicate handling,
partial-stream semantics, cancellation, cleanup and audit. Store no credential
values in the bundle or evidence.

## Conformance and lifecycle

Freeze success, denial, malformed, unsupported, partial, disconnect, duplicate,
timeout, downgrade and recovery fixtures. Record compatibility ranges,
generated-artifact drift detection, upgrade order, rollback, deprecation,
retirement and target-host verification.
