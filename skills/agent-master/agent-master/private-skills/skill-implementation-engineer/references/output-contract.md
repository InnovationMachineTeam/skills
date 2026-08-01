# Skill implementation output contract

## Contents

- Component audit
- Engineering contracts
- Security and observability
- Verification and integration

## Component audit

For every proposed component return its source type, normalized type, decision,
reason, owner and lifecycle. Explicitly list created, reused, adapted, merged,
split, excluded and deferred components.

Build only when specific business logic, data control or stable small
integration justifies ownership. Reuse when the task is standard and a current,
licensed, maintained solution has an acceptable contract. Add an adapter when
an external solution fits but must be isolated, permission-limited or replaceable.

Keep expert judgment outside deterministic automation. Split components with
unrelated responsibilities, different permissions, risks, runtimes, review
independence or release cadence.

## Engineering contracts

Every component records:

```yaml
component:
  id: ""
  kind: "script|tool|adapter|automation|hook"
  version: "1.0.0"
  responsibility: ""
  non_responsibilities: []
  entrypoints: []
  inputs: []
  outputs: []
  errors: []
  side_effects: []
  idempotent: true
  dry_run: true
  timeout: ""
  retry_policy: ""
  permissions: []
  secrets: []
  human_gates: []
  observability: []
  tests: []
  owner: ""
```

CLI components provide `--help`, `--version`, predictable nonzero failures,
stderr diagnostics and machine-readable output where useful. Mutating commands
provide `--dry-run` when technically possible. Automations define trigger,
preconditions, persisted state, idempotency key, retry, resume, stop,
notification, dead-letter/escalation and rollback/compensation behavior.

Use one error model with category, severity, user-safe message, diagnostic
details, retryability, suggested action, Human-decision flag and correlation ID.

## Security and observability

Threat-model prompt injection, command injection, path traversal, unsafe
deserialization, SSRF, secret leakage, excessive permissions, unsafe temporary
files, race conditions, dependency/supply-chain attacks, webhook spoofing,
duplicate delivery, uncontrolled code execution and confidential-data egress.

Require input/output validation, path allowlists where possible, structured
process invocation, sandboxing for untrusted code, external secret storage,
redacted logs, auditable mutations and Human approval for high-risk effects.

Record operational logs, audit logs, metrics and traces with component/version,
task/process/correlation/trace IDs, event, status, duration and safe metadata.
Never log secrets, personal data or hidden model reasoning.

## Verification and integration

Run applicable formatting, lint, type, schema, unit, contract, integration,
security, failure, end-to-end, coverage and dependency/license checks. Block a
release candidate on broken build, incompatible unversioned contract, critical
vulnerability, required-test/eval failure, policy violation or missing required
documentation.

Show the exact skill step that calls each component and the agent binding with
allowed operations, permissions, contracts, failure and approval policies.
Return actual commands run and results. If a check was not run, mark it
`NOT_EVALUATED`; never infer a pass from file creation.
