# Process orchestrator output contract

## Contents

- Required analysis
- Process and artifact models
- Orchestrator specification
- Verification gates

## Required analysis

Return:

1. process summary, scope, owner, users and success criteria;
2. assumptions, unresolved questions and constraints;
3. normalized stage table with dependencies, decisions, errors and loops;
4. artifact map and stage-level Ready/Done criteria;
5. full role model and human/AI/hybrid assignment rationale;
6. role-overlap audit, RACI and minimal operating variants;
7. justified specialist-agent catalog and rejected-agent decisions.

## Process and artifact models

Each stage records:

```yaml
stage:
  id: ""
  goal: ""
  owner: ""
  inputs: []
  tasks: []
  outputs: []
  dependencies: []
  decisions: []
  ready: []
  done: []
  reviewer: ""
  approver: ""
  human_gates: []
  failure_routes: []
```

Each artifact records identity, type, producer, reviewers, approver, consumers,
source of truth, schema/format, status, version, provenance, retention and
verification method.

Each role records mission, primary responsibility, non-responsibilities,
inputs, outputs, decisions, authority, required skills, knowledge, tools,
documents read/written/owned/verified, interactions, escalation and metrics.

## Orchestrator specification

Include:

- mission, scope, non-responsibilities and operating modes;
- input, output and task-envelope contracts;
- phase DAG and state machine;
- role/skill/tool discovery and routing;
- readiness, quality, review and approval gates;
- issue, error, retry, timeout, cancellation, compensation and recovery models;
- Human-in-the-loop request/response contract;
- context minimization, knowledge sources and artifact storage;
- permissions, secrets, data classes, audit and retention;
- operational logs, audit logs, traces, metrics, cost and activity timeline;
- ready-to-use system prompt and one realistic end-to-end example.

Use these process states when applicable:

```text
Requested -> Diagnosing -> Planned -> In Progress -> Under Review
-> Changes Requested -> Awaiting Human Decision -> Approved
-> Ready for Release -> Released -> Monitoring -> Needs Update -> Archived
```

Adapt names to the selected harness without losing transition meaning.

## Verification gates

- Every stage has an observable result, not only actions.
- Every artifact has one accountable owner and downstream consumer.
- Every role has one primary responsibility and explicit exclusions.
- No role silently performs independent approval of its own work.
- Every transition has an entry condition, allowed actor and resulting state.
- Every loop has a retry or iteration bound and escalation path.
- Human gates cover high risk, legal decisions, public release, destructive or
  irreversible effects, permissions, credentials and confidential-data egress.
- Monitoring explains what ran, why, with which version and result, and what
  happens next without storing hidden model reasoning.
