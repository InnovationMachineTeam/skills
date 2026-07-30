# Checklists

Practice-ID: BP-CHECK-001
Scope: mixed
Status: current
Sources: SRC-AS-001, SRC-AS-002, SRC-AS-003, SRC-AS-004, SRC-AS-005, SRC-ANT-002, SRC-OAI-001, SRC-LOCAL-001, SRC-DER-001
Last-rebuilt: 2026-07-30

## Author

- [ ] One recognizable user outcome and coherent trigger family.
- [ ] Valid name/directory identity and specific description with boundaries.
- [ ] Observable inputs, outputs, invariants, gates, recovery, and definition of done.
- [ ] Concise SKILL.md with conditional references and no duplicated knowledge.
- [ ] Scripts/assets/references exist only when reusable and necessary.
- [ ] Host assumptions, dependencies, permissions, and side effects are explicit.
- [ ] No unfinished placeholders or unsupported claims.

## Routing and behavior

- [ ] Direct, indirect, incomplete, negative, ambiguous, and neighboring cases.
- [ ] Routing and behavioral evals remain separate.
- [ ] Baseline, comparable environment, repeated stochastic runs, and untouched holdout.
- [ ] Assertions inspect observable artifacts and side effects.
- [ ] Fresh context without expected-answer leakage.
- [ ] Catalog coexistence and common compositions tested.

## Scripts and security

- [ ] Scripts were actually run on positive and failure cases.
- [ ] Inputs, sizes, paths, symlinks, dependencies, stdout/stderr, and exit codes are safe.
- [ ] No user-text shell interpolation or hidden dependency installation.
- [ ] Untrusted data cannot change policy, recipients, permissions, or destinations.
- [ ] Network, credentials, MCP, filesystem, external URLs, and exfiltration reviewed.
- [ ] Mutations have preview, exact scope, verification, rollback, and partial-success handling.

## Release and lifecycle

- [ ] Official validator and package checks pass.
- [ ] Owner, reviewer, source, version, checksum, risk, and evaluation status recorded.
- [ ] Isolation, coexistence, security, portability, consumer, and E2E gates pass.
- [ ] Target host verifies discovery and activation.
- [ ] Production version pinned; last-known-good and rollback tested.
- [ ] Monitoring and next evaluation trigger exist.

## Best-practices refresh

- [ ] All registered sources checked or explicitly unavailable.
- [ ] Snapshot comparison separates transport and semantic change.
- [ ] Claims classified and conflicts scoped.
- [ ] Corpus rebuilt in staging only when warranted.
- [ ] Every practice ID and source ID validates.
- [ ] Managed-skill master prompt generated from the resulting revision.
- [ ] No blanket target rewrites or active self-modification occurred.
