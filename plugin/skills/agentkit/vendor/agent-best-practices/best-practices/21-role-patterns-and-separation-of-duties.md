# Ролевые паттерны и разделение обязанностей

## Роль не равна агенту

Роль — набор ответственности, полномочий, входов и проверяемых результатов.
Один человек или агент может выполнять несколько ролей в low-risk процессе;
одна роль может быть реализована несколькими agents. Отдельный agent оправдан,
если требуется независимый контекст, capability, security boundary,
параллелизм или иной lifecycle owner.

Для каждой роли фиксируйте:

```yaml
role: independent-verifier
accountable_human: quality-owner
mission: подтвердить outcome по исходному intent
inputs: [intent_ref, artifact_ref, eval_plan_ref]
outputs: [typed_verdict, evidence_refs, gaps]
permissions: [read_artifacts, run_approved_evals]
forbidden: [edit_candidate, approve_exception]
escalates_when: [uncertain_high_impact, conflicting_evidence]
sla: 30m
```

NIST AI RMF требует документировать роли, линии коммуникации и human-AI
oversight на протяжении lifecycle; executive leadership сохраняет
ответственность за AI risk decisions
([AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)).

## Базовые ролевые архетипы

### Sponsor / accountable owner

Определяет ценность, risk appetite и окончательную ответственность. Может
делегировать работу, но не accountability. Принимает high-impact trade-offs,
исключения и retirement решения.

### Intent owner

Формулирует outcome, stakeholders, non-goals, constraints и success measures.
Защищает процесс от локальной оптимизации не той задачи. В продуктовой работе
обычно product owner; в incident — incident commander.

### Architect

Выбирает boundaries, contracts, patterns и quality trade-offs. Не диктует каждый
шаг исполнения; фиксирует architecturally significant decisions и последствия.
Специализации: agent architect, workflow/orchestration architect, skill
architect, platform/Agent OS architect, security и data architect.

### Builder / executor

Создаёт bounded deliverable в выданном scope. Возвращает artifact, change log,
tests и evidence; не объявляет собственную работу окончательно принятой.

### Orchestrator / coordinator

Владеет task graph, dispatch, state, budgets, checkpoints и synthesis. Он
ответственен за завершение процесса, но не должен подменять независимые domain,
security и approval роли.

### Verifier / evaluator

Проверяет outcome, assumptions и regressions по заранее заданным критериям.
Verifier отвечает «доказано ли?», evaluator — «насколько хорошо и устойчиво?». Для
high risk они read-only относительно candidate и имеют независимые datasets или
tools.

### Governor / approver

Применяет policy и принимает residual risk. Approval broker может собрать
evidence, но право решения остаётся у назначенного approver. У approval есть
scope, expiry и revocation.

### Curator / steward

Поддерживает качество долгоживущего актива: registry, memory, knowledge,
documentation, dataset, prompt/skill portfolio. Stewardship включает freshness,
provenance, duplication, compatibility, deprecation и retirement.

### Operator / SRE

Владеет SLO, capacity, telemetry, runbooks, recovery и operational readiness.
Не обязан быть автором agent; production reality имеет приоритет над design
assumptions.

### Observer / analyst

Преобразует traces, costs, incidents и user outcomes в диагностический evidence.
Не меняет active policy автоматически. Специализации: trace analyst, FinOps,
quality analyst, drift detector.

### Adversary / challenger

Ищет counterexamples, abuse paths, hidden assumptions и correlated failures.
Red team не принимает финальное решение и не получает лишних production rights.

### Publisher / release manager

Проверяет package identity, version, provenance, changelog, compatibility,
signatures, gates и promotion. Publisher отличается от registry owner и автора.

### Incident roles

- commander — приоритеты, коммуникация и accountability;
- triage — severity и initial routing;
- investigator — competing hypotheses и evidence;
- containment/recovery operator — безопасные effectors;
- scribe — timeline и decisions;
- reviewer — post-incident learning и action tracking.

## Роли по слоям системы

### Agent

| Роль | Ответственность |
|---|---|
| Agent product owner | Outcome, users, risk tier, lifecycle |
| Agent architect | Contract, tools, memory, autonomy, failure model |
| Prompt/context engineer | Instructions, context selection, grounding |
| Tool/integration engineer | Typed tools, adapters, errors, idempotency |
| Eval engineer | Datasets, rubrics, graders, regression gates |
| Agent security engineer | Threat model, permissions, injection controls |
| Agent operator | SLO, traces, budgets, incidents |
| Agent registry steward | Versions, compatibility, status, deprecation |

### Subagents и команды

| Роль | Ответственность |
|---|---|
| Delegation designer | Task envelopes, context capsules, return schema |
| Team lead | Mission, assignments, conflict/escalation policy |
| Scheduler | Dependencies, leases, retries, backpressure |
| Specialist | Bounded domain deliverable |
| Integration owner | Contract fit, merge, end-to-end wiring |
| Communication moderator | Message schema, decision capture, loop prevention |
| Independent verifier | Outcome и cross-agent failure modes |

### Agent OS

| Роль | Ответственность |
|---|---|
| Platform owner | Service strategy, roadmap, adoption, SLO |
| Runtime engineer | Scheduler, execution, checkpoints, recovery |
| Registry/capability steward | Identity, versions, discovery, revocation |
| Policy owner | Rules, risk tiers, approval matrix |
| IAM/security owner | Identities, credentials, sandbox, network policy |
| Knowledge/memory steward | Provenance, retention, retrieval, deletion |
| Observability owner | Telemetry schema, dashboards, alert quality |
| Reliability/SRE owner | Capacity, resilience, incident readiness |
| Cost/FinOps owner | Budget model, allocation, anomaly response |
| Protocol/integration owner | MCP/A2A/adapters и compatibility |
| Assurance owner | Evals, audit, release gates, evidence retention |

### Skills и marketplace

| Роль | Ответственность |
|---|---|
| Skill sponsor | Need, audience, success and retirement |
| Skill architect/author | Boundary, workflow, instructions, package |
| Trigger/eval designer | Discovery precision и outcome evaluation |
| Script maintainer | Deterministic core, portability, security |
| Source curator | Provenance, licenses, freshness, external intake |
| Skill reviewer | Structure, usability, conflicts, permissions |
| Publisher | Version, package, signatures, release evidence |
| Marketplace owner | Taxonomy, entries, policy, availability |
| Consumer/migration steward | Compatibility, adoption, upgrade/deprecation |

## Lifecycle accountability

| Lifecycle phase | Responsible roles | Accountable role | Independent input/gate |
|---|---|---|---|
| Discover need | Scout/researcher, domain expert | Intent owner | Duplication/value review |
| Design | Architect, security, evaluator | Asset owner | ADR/threat/eval review |
| Build | Author, tool/context engineers | Delivery owner | Automated checks |
| Validate | Verifier, eval, red team | Assurance owner | Independent evidence |
| Approve/publish | Release manager, publisher | Risk/release owner | Policy + provenance gate |
| Operate | SRE, observer, support | Service owner | SLO and incident signals |
| Improve/upgrade | Owner, analyst, maintainer | Asset owner | Regression + migration gate |
| Deprecate | Steward, migration owner | Portfolio owner | Dependency inventory |
| Retire | Registry/IAM/data stewards | Accountable owner | Revocation + archive proof |

## Separation of duties

### Обязательные разделения для высокого риска

- author не является единственным verifier;
- policy author не является единственным approver исключения;
- deployer не является безусловным release approver;
- registry publisher не является единственным supply-chain/security reviewer;
- memory writer не является единственным fact/provenance verifier;
- eval author не может выбирать только выгодные production samples;
- incident fixer не закрывает root cause без независимого evidence review;
- agent, который запрашивает расширение прав, не выдаёт их себе;
- cost optimizer не может единолично понижать safety/quality floor;
- retirement выполняется отдельно от решения, что актив больше не нужен.

### Temporal separation для малой команды

Если людей мало, один человек MAY носить несколько ролей, но разделяйте фазы:

1. До реализации зафиксировать rubric и risk policy.
2. После реализации начать новый review context.
3. Использовать independent automated checks и immutable evidence.
4. Для irreversible/high-impact action получить второго approver.
5. Зафиксировать role switching в audit record.

LLM с другим prompt, но тем же контекстом и данными, — слабая независимость.
Сильнее независимость по данным, tools, model/runtime и организационной
подотчётности.

## Human oversight patterns

| Паттерн | Человек | Применение |
|---|---|---|
| Human-in-the-loop | Одобряет до действия | Деньги, publish, production, personal data |
| Human-on-the-loop | Наблюдает и может остановить | Reversible bounded automation |
| Human-over-the-loop | Задаёт policy, audits и risk envelope | Высокий объём low-risk runs |
| Human-out-of-the-loop | Не участвует в run | Только доказанный low-risk, reversible scope |

Интерфейс oversight показывает intent, proposed action, affected resources,
evidence, uncertainty, alternatives, reversibility и deadline. Кнопка «approve»
без этих данных создаёт automation bias.

## Role anti-patterns

- **Super-agent owner** — один агент ставит цель, исполняет, проверяет и одобряет.
- **Responsibility without authority** — роль отвечает за SLO, но не может
  остановить route/release.
- **Authority without evidence** — approver видит только summary.
- **Orchestrator as universal expert** — coordinator подменяет специалистов.
- **Invisible steward** — долгоживущий registry/memory/dataset не имеет owner.
- **Shared accountability** — «команда отвечает», но никто не принимает решение.
- **Permanent temporary role** — incident или migration owner остаётся навсегда.
- **Agent anthropomorphism** — persona считается доказательством компетенции.
- **Reviewer writes the answer** — verdict смешан с remediation и теряет
  независимость.

## Минимальная role assignment matrix

Используйте DACI/RACI только как карту ответственности, не как замену workflow.

| Актив | Driver/Responsible | Approver/Accountable | Contributors | Informed |
|---|---|---|---|---|
| Agent contract | Agent architect | Agent owner | Security, eval, domain | Operator |
| Skill release | Skill author | Publisher/portfolio owner | Reviewer, eval, security | Consumers |
| Workflow version | Orchestration engineer | Service owner | Runtime, policy, SRE | Teams |
| Policy change | Policy owner | Risk owner | Legal, security, operations | Affected owners |
| Memory corpus | Memory curator | Knowledge owner | Domain, privacy, security | Agents/users |
| Production promotion | Release manager | Release/risk owner | Eval, SRE, security | Support/users |
| Retirement | Migration steward | Portfolio owner | Registry, IAM, data, SRE | Dependents |

Матрица хранится рядом с inventory и пересматривается при смене risk tier,
owner, tool permissions, audience или deployment context.
