# Diagnostic Taxonomy

## Contents

- Classification method
- Eight domains
- Health precedence
- Escalation

## Classification method

Classify by the failing stage and causal mechanism:

```text
discover → load → resolve resources → execute → use tools → manage state → verify → package
```

Collect symptom, expected behavior, first bad revision, affected hosts, reproducibility, error evidence, side effects, and recent changes.

## Eight domains

### Metadata and discovery

Use for invalid frontmatter, folder/name mismatch, missing or false triggers, UI metadata drift, and skill collisions.

### Context and resources

Use for broken links, missing references, wrong paths, deeply nested routing, stale or duplicated content, and resources loaded at the wrong time.

### Scripts and dependencies

Use for syntax errors, invalid inputs, wrong exit codes, hidden dependencies, destructive writes, nondeterministic helpers, and runtime incompatibility.

### Tools and environment

Use for missing capabilities, authentication, permissions, network, rate limits, tool schema drift, OS behavior, and unavailable services.

### Workflow, state, and recovery

Use for skipped stages, bad clarification, unbounded retries, lost checkpoints, partial success, false completion, and resume failures.

### Security and authority

Use for prompt injection, secret exposure, uncontrolled recipients, external or destructive actions, scope expansion, and missing technical enforcement.

### Evals and regressions

Use for missing reproduction, stale fixtures, false judges, answer leakage, untested failure paths, and inability to prove recovery.

### Packaging and portability

Use for installation layout, unsupported metadata, path conventions, accidental junk, host-specific assumptions, archive or distribution defects, and false compatibility claims.

## Health precedence

Use `UNSAFE` over `BROKEN`, `BROKEN` over `DEGRADED`, and `DEGRADED` over `HEALTHY`. A skill may be both functional and unsafe; health must reflect the unsafe state.

## Escalation

- Address `UNSAFE` containment before functionality.
- Restore broken core paths before optimization.
- Route healthy performance or quality work to an optimizer.
- Ask for authority before repair when edits or side effects were not authorized.

