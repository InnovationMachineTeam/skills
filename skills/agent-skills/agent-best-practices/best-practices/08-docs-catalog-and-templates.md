# Каталог документов и минимальные шаблоны

## Выбор документов по размеру риска

| Артефакт | Lite | Standard | High assurance |
|---|---:|---:|---:|
| Intent / change brief | MUST | MUST | MUST |
| Behavioral spec | по необходимости | MUST | MUST |
| Functional requirements | inline | MUST | MUST |
| Quality requirements | ключевые | MUST | MUST + traceability |
| Architecture overview | ссылка | MUST | MUST |
| ADR | значимый выбор | MUST для значимых решений | MUST |
| Threat model | риск-зависимо | риск-зависимо | MUST |
| Test/eval plan | smoke | MUST | MUST + independent review |
| Runbook/rollback | при ops change | MUST для service | MUST |
| Release evidence | кратко | MUST | MUST + approvals |

## Product и Discovery

### `docs/product/vision.md`

- проблема и целевые пользователи;
- desired outcomes и business metrics;
- принципы и non-goals;
- стратегические ограничения;
- owner и горизонт решения.

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

Это операционализирует ADLC Intent: планирование формулирует проверяемую
гипотезу, а не притворяется, что outcome уже известен
([ADLC](https://www.adlc.io/)).

### `docs/discovery/research-*.md`

- research question;
- method и выборка;
- источники с датами;
- findings vs interpretations;
- contradictions;
- limitations;
- implications и follow-up experiments.

## Требования и спецификации

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

Этот пакет объединяет сильные стороны Agent OS `specs/`, Spec Kit и OpenSpec:
intent → behavior → design → tasks → evidence. Для brownfield полезны delta
sections ADDED/MODIFIED/REMOVED
([OpenSpec](https://github.com/Fission-AI/OpenSpec)).

## Архитектура

### `docs/architecture/README.md`

- system context;
- container map;
- boundaries и owners;
- critical flows;
- data classification;
- external dependencies;
- quality attribute scenarios;
- risks и active ADRs;
- links на code maps и runbooks.

Для больших систем можно адаптировать arc42, но заполнять только значимые
разделы ([arc42](https://arc42.org/)).

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

### План

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

План должен включать exact paths, зависимости и observable verification. GSD
добавляет wave, depends_on, files_modified и goal-backward must-haves; Spec Kit
группирует задачи по independently testable user stories.

### Release record

- shipped scope и non-shipped scope;
- commits/PR/artifacts;
- schema/data migrations;
- tests/evals и approvals;
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
- root cause vs trigger;
- corrective actions with owners;
- new tests/alerts/runbook changes;
- agent behavior and tool traces, если участвовали агенты.

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

## Индексы

`docs/README.md` — навигация, а не повтор содержания. Для каждого раздела он
показывает:

- canonical documents;
- owner;
- audience;
- status/freshness;
- когда читать;
- generated vs hand-authored;
- archive location.

Индекс MAY генерироваться из metadata, но ручные summaries должны оставаться
короткими и проверяемыми.
