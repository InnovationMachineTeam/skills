# Каталог типовых агентов

Этот файл перечисляет прикладные специализации. Ролевые архетипы, lifecycle
accountability, human oversight и separation of duties описаны в
[21-role-patterns-and-separation-of-duties.md](21-role-patterns-and-separation-of-duties.md).

## Как пользоваться каталогом

Роль — не обязательный отдельный агент. Сначала определите capability и
security boundary. Объединяйте роли, если у них общие tools, context и критерии;
разделяйте, если нужны независимость, специализация, разные права или
параллелизм.

Каждой роли задайте owner, входы, выходы, write-set, tools, permissions, evals и
escalation rules.

## PDLC и Discovery

| Агент | Ответственность | Основные выходы |
|---|---|---|
| Opportunity scout | Собирает сигналы, проблемы и возможности | opportunity backlog |
| Research planner | Формулирует вопросы, метод и критерии доказательства | research plan |
| Market researcher | Рынок, конкуренты, alternatives | cited market report |
| Domain researcher | Доменные правила, failure modes, regulation | domain context |
| User researcher | Интервью/наблюдения, не подменяя человека | evidence synthesis |
| JTBD analyst | Jobs, pains, gains, alternatives | jobs map |
| Hypothesis/bet steward | Ведёт bet register и resolution signals | governed bets |
| Product strategist | Outcomes, positioning, non-goals | vision/strategy |
| Product manager | Scope, priorities, PRD/spec lifecycle | product requirements |
| UX researcher | Research questions, usability evidence | UX findings |
| UX/service designer | Journeys, states, service blueprint | experience design |
| Experiment designer | Протокол эксперимента и decision thresholds | experiment plan |

## Requirements engineering

| Агент | Ответственность | Независимый gate |
|---|---|---|
| Requirements elicitor | Находит stakeholders, needs, constraints | coverage review |
| Requirements analyst | Делает требования атомарными и тестируемыми | ambiguity lint |
| Functional analyst | Observable capabilities, rules, scenarios | acceptance review |
| Quality-attribute analyst | Performance, reliability, security и др. | measurable NFR gate |
| Constraint/compliance analyst | Legal, organizational, technical constraints | compliance owner |
| Traceability manager | Связи intent→requirement→design→test→release | orphan detection |
| Requirements verifier | Проверяет completeness, consistency, feasibility | read-only verdict |

## SDLC / Architecture

| Агент | Ответственность | Выходы |
|---|---|---|
| Solution architect | Boundaries, integrations, trade-offs | architecture overview |
| Enterprise architect | Portfolio/platform alignment | capability map |
| Data architect | Data model, lineage, retention | data architecture |
| API/contract architect | Interfaces, versioning, compatibility | API contracts |
| Security architect | Threat model и control design | threats/controls |
| Reliability architect | SLO, failure domains, recovery | reliability plan |
| Privacy engineer | Data minimization, purpose, consent | privacy controls |
| Cost/FinOps analyst | Cost model и budgets | cost envelope |
| ADR steward | Decision quality и lifecycle | decision log |

## Implementation

| Агент | Ответственность | Ограничение |
|---|---|---|
| Planner | DAG, slices, write-sets, verification | не реализует |
| Codebase mapper | Структура, patterns, dependencies | read-only |
| Implementer | Один bounded deliverable | exclusive write-set |
| Refactoring agent | Поведение-сохраняющие изменения | characterization tests |
| Migration agent | Schema/data/code migration | rollback + dry-run |
| Integration agent | Соединяет independently built slices | merge owner |
| Test engineer | Автоматические tests по risk model | не подтверждает собственный код |
| Documentation agent | Обновляет документы по shipped behavior | fact verification |

## Quality и assurance

| Агент | Фокус |
|---|---|
| Plan reviewer | Достижимость goal и coverage |
| Code reviewer | Correctness, maintainability, defects |
| Goal verifier | Outcome против spec, не tasks |
| Security reviewer | Threat mitigations и misuse cases |
| Performance reviewer | Budgets, bottlenecks, regressions |
| Accessibility reviewer | WCAG/user flows/assistive behavior |
| Test architect | Risk-based strategy и traceability |
| Eval designer | Dataset, rubrics, graders, thresholds |
| Adversarial tester | Prompt injection, tool misuse, edge cases |
| Compliance assessor | Evidence против control requirements |
| Release gatekeeper | Сводит evidence и policy в go/no-go |

## Delivery и Operations

| Агент | Ответственность |
|---|---|
| Release orchestrator | Версии, changelog, checks, approvals |
| Deployment agent | Promotion/canary в утверждённом envelope |
| Canary observer | Production signals и rollback trigger |
| SRE/reliability agent | SLO, alerts, capacity, runbooks |
| Incident triage agent | Классификация, evidence, safe routing |
| Incident commander assistant | Timeline и coordination; человек accountable |
| Root-cause investigator | Гипотезы и доказательства до fix |
| Rollback/recovery agent | Проверенная обратимая процедура |
| Cost monitor | Spend anomalies и budget enforcement |
| Documentation drift detector | Несоответствие docs/code/runtime |

## Agent OS и governance

| Агент | Ответственность |
|---|---|
| Intent router | Выбор workflow/capability с confidence |
| Orchestrator | DAG, dispatch, integration, verification |
| Scheduler | Dependencies, leases, retries, backpressure |
| Policy agent/service | Объясняет policy; enforcement остаётся детерминированным |
| Approval broker | Собирает evidence для accountable approver |
| Context builder | Формирует минимальный grounded context pack |
| Memory curator | Проверяет, классифицирует и устаревает memory |
| Knowledge indexer | Индексы и provenance |
| Agent registry steward | Версии, compatibility, lifecycle |
| Agent evaluator | Offline/online evals и regression gates |
| Trace analyst | Находит loops, routing и tool failures |
| Agent security monitor | Поведение, privilege и injection signals |
| Workflow doctor | Диагностика stuck/orphan/inconsistent runs |

## Командные композиции

### Discovery pod

Research planner + market/domain/user researchers + product strategist +
skeptical evaluator. Product owner принимает bet.

### Feature delivery pod

Requirements analyst + architect + planner + scoped implementers + test engineer
+ verifier + documentation agent. Оркестратор не пишет те же файлы.

### High-risk change pod

Feature pod + security/privacy/reliability/migration specialists + independent
release gatekeeper + accountable human.

### Incident pod

Triage + competing-hypothesis investigators + SRE + recovery agent + timeline
scribe. Incident commander остаётся человеком для high-impact решений.

### Agent improvement pod

Trace analyst + eval designer + prompt/tool engineer + security reviewer +
canary owner. Изменение не проходит production gate без regression evidence.

## Роли, которые нельзя бездумно объединять

- implementer и единственный verifier;
- policy author и единственный policy approver;
- deployment agent и безусловный release approver;
- memory writer и единственный fact verifier;
- incident fixer и единственный root-cause investigator;
- requirements author и единственный stakeholder proxy.

Separation of duties особенно важен для денег, персональных данных, security,
production и compliance.
