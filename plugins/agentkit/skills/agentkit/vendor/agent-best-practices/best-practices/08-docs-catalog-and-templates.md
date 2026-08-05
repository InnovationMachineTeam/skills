# Document Catalog and Minimal Templates

## Document selection by risk size

| Artifact | Lite | Standard | High assurance |
|---|---:|---:|---:|
| Intent / change brief | MUST | MUST | MUST |
| Behavioral spec | as needed | MUST | MUST |
| Functional requirements | inline | MUST | MUST |
| Quality requirements | key only | MUST | MUST + traceability |
| Architecture overview | reference | MUST | MUST |
| ADR | significant choice | MUST for significant decisions | MUST |
| Threat model | risk-dependent | risk-dependent | MUST |
| Test/eval plan | smoke | MUST | MUST + independent review |
| Runbook/rollback | for ops changes | MUST for service | MUST |
| Release evidence | brief | MUST | MUST + approvals |

## Product and Discovery

### `docs/product/vision.md`

- problem and target users;
- desired outcomes and business metrics;
- principles and non-goals;
- strategic constraints;
- owner and decision horizon.

### `docs/product/bets.md`

```markdown
## BET-012 — Shorter checkout

- Hypothesis:
- Unknown to resolve:
- Target generation:
- Resolution signal:
- Decision deadline:
- Risk envelope:
- Owner:
- Status:
```

This operationalizes ADLC Intent: planning formulates a testable hypothesis
rather than pretending the outcome is already known
([ADLC](https://www.adlc.io/)).

### `docs/discovery/research-*.md`

- research question;
- method and sample;
- sources with dates;
- findings vs. interpretations;
- contradictions;
- limitations;
- implications and follow-up experiments.

## Requirements and specifications

### `docs/requirements/<capability>.md`

```markdown
# Capability

## Intent and scope
## Stakeholders
## Functional requirements
### FR-001 — Observable behavior
- Rationale:
- Acceptance scenarios:
- Verification:
- Priority:

## Quality requirements
### QR-001 — Latency
- Scenario:
- Measure:
- Target:
- Operating conditions:
- Verification:

## Constraints
## Assumptions
## Out of scope
## Traceability
```

### Change package

```text
docs/delivery/changes/<change-id>/
├── proposal.md       # why, intent, scope
├── spec.md           # observable what
├── design.md         # how and trade-offs
├── tasks.md          # dependency-ordered work
├── verification.md   # evidence against spec
└── archive.md        # shipped outcome and links
```

This package combines the strengths of Agent OS `specs/`, Spec Kit, and
OpenSpec: intent → behavior → design → tasks → evidence. For brownfield work,
delta sections ADDED/MODIFIED/REMOVED are useful
([OpenSpec](https://github.com/Fission-AI/OpenSpec)).

## Architecture

### `docs/architecture/README.md`

- system context;
- container map;
- boundaries and owners;
- critical flows;
- data classification;
- external dependencies;
- quality attribute scenarios;
- risks and active ADRs;
- links to code maps and runbooks.

For large systems, arc42 can be adapted, but only the meaningful sections should
be filled in ([arc42](https://arc42.org/)).

### ADR

```markdown
---
id: ADR-0042
status: proposed
date: 2026-07-30
decision_owners: [platform]
consulted: [security, checkout]
---

# Use an outbox for payment events

## Context and problem
## Decision drivers
## Considered options
## Decision
## Consequences
## Risks and mitigations
## Confirmation
## Links
```

## Delivery

### Plan

```markdown
# Plan

## Goal and non-goals
## Source artifacts
## Assumptions and preconditions
## Deliverables
## Task DAG
| ID | Outcome | Depends on | Owner | Write-set | Verification |
## Waves
## Risks and checkpoints
## Rollback
## Done when
```

The plan MUST include exact paths, dependencies, and observable verification.
GSD adds wave, depends_on, files_modified, and goal-backward must-haves; Spec
Kit groups tasks by independently testable user stories.

### Release record

- shipped scope and non-shipped scope;
- commits/PR/artifacts;
- schema/data migrations;
- tests/evals and approvals;
- feature flags/canary;
- rollback;
- monitoring window;
- docs updated;
- known issues.

## Operations

### Runbook

```markdown
# Service runbook

## Purpose and owner
## Preconditions and access
## Health indicators and SLOs
## Dashboards and alerts
## Diagnosis decision tree
## Safe actions
## Dangerous actions requiring approval
## Rollback / recovery
## Escalation contacts or roles
## Verification after action
## Last exercised
```

### Incident record

- impact and timeline;
- detection;
- contributing factors;
- response actions;
- evidence;
- root cause vs. trigger;
- corrective actions with owners;
- new tests/alerts/runbook changes;
- agent behavior and tool traces, if agents were involved.

## Agent system docs

```text
docs/agents/
├── README.md              # topology and how to operate
├── catalog.md             # agent capability registry projection
├── contracts/             # input/output/task contracts
├── workflows/             # diagrams and state machines
├── policies/              # permissions, approvals, budgets
├── evals/                 # datasets, rubrics, scorecards
├── operations/            # pause, resume, cancel, incident runbooks
└── changes/               # versioned changes to agent behavior
```

### Agent card

```markdown
# requirements-analyst

- Purpose:
- Owner:
- Version:
- Inputs / outputs:
- Tools and permissions:
- Data classifications:
- Delegation rules:
- Stop/escalation rules:
- Known failure modes:
- Evals and thresholds:
- Runbook:
```

## Indexes

`docs/README.md` is navigation, not duplicated content. For each section it
shows:

- canonical documents;
- owner;
- audience;
- status/freshness;
- when to read it;
- generated vs. hand-authored;
- archive location.

The index MAY be generated from metadata, but manual summaries SHOULD remain
short and verifiable.
