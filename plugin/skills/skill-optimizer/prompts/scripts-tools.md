# Scripts and Tool Integration Optimization Prompt

Apply after [base.md](base.md). Improve deterministic helpers and external capability use.

## Diagnose

- Run every affected executable on success and failure cases.
- Verify tool availability, current contracts, dependencies, credentials, permissions, identifiers, and destinations.
- Inspect hidden network access, unstable parsing, ambiguous results, duplicate effects, and unsafe path handling.

## Optimize

- Keep judgment and consent in instructions; put exact repeated transformations in scripts.
- Parameterize paths and values, validate inputs, use stdout/stderr and nonzero exit codes, and add dry-run for consequential changes.
- Bound retries, protect non-idempotent actions, minimize access and data, and verify external state by read-back.
- Prefer official semantic tools over brittle UI or shell workarounds.

## Guardrails

Do not upgrade dependencies, change APIs, or add network access without a separate hypothesis and compatibility check. Never interpret capability as permission. Test missing dependency, authorization failure, rate limits, malformed data, partial success, and repeated invocation.

