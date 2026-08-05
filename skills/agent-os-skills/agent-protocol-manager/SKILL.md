---
name: agent-protocol-manager
description: Designs, audits and stages explicit ports-and-adapters contracts for MCP, A2A, agent hosts and model/tool providers, including pinned versions, discovery, authentication, capability negotiation, schemas, streaming, cancellation, errors, retries, provenance, conformance and rollback. Use when an agent system needs a governed interoperability boundary or compatibility matrix. Do not use for ordinary API implementation, silently hiding semantic differences, issuing credentials, enabling unsupported features, or deploying adapters without conformance and lifecycle authority.
metadata:
  version: "1.0.3"
---

# Govern Agent Protocol Boundaries

Define a canonical internal contract and make every transport or host difference
explicit. An adapter may be `native`, `generated` or `unsupported`; it must not
claim portability by erasing semantics.

## Establish the boundary

Resolve the two systems, protocol/host/provider, pinned versions, discovery,
identity, authentication, data classes, operations, schemas, streaming,
cancellation, error model, timeout, retry, idempotency and lifecycle owner.
Require current authoritative specifications before asserting exact behavior.
Default to a read-only compatibility and conformance plan.

Do not build a platform adapter when an existing native boundary is sufficient
or when the requested feature cannot preserve policy, provenance, cancellation
or failure semantics.

Read [references/skill-dependencies.md](references/skill-dependencies.md) when
the route needs a recommended companion. Missing companions limit only their
named evidence layer; never imitate them.

## Design the contract

Read [references/protocol-adapter-contract.md](references/protocol-adapter-contract.md).

1. Define the canonical internal request, event, artifact, error and lifecycle
   schemas before mapping transports.
2. Pin every protocol and host version. Record capability negotiation and the
   exact unsupported set.
3. Validate identity, authorization, content type, schema, provenance, size,
   timeout, idempotency and tenant boundary at ingress and egress.
4. Map streaming, cancellation, retries, duplicate delivery, partial results
   and disconnects without converting ambiguous outcomes into success.
5. Keep credentials least-privilege, short-lived and outside the bundle.
6. Define generated-artifact ownership and drift detection. Generated adapters
   never become a second source of truth.
7. Define compatibility, upgrade, downgrade, deprecation and rollback.

Validate the candidate:

```bash
python3 scripts/validate_protocol_contract.py protocol-contract.json
```

## Prove conformance

Freeze fixtures for success, authorization denial, malformed data, unsupported
feature, partial stream, cancellation, disconnect, duplicate message, timeout,
oversize payload, stale version and downgrade. Verify output schemas, audit and
provenance, bounded retries, cleanup, idempotency and no credential leakage.

Use `agent-policy-manager` for cross-boundary authorization and
`agent-evaluator` for independent conformance evidence. Implementation,
credential provisioning, publication and deployment remain separate authorized
transitions.

## Complete

Return contract identity/version/status, compatibility matrix, native/generated/
unsupported outcomes, conformance evidence, security and data boundary, drift,
upgrade/rollback plan, residual risks and deployment status.
