# Референсная архитектура Agent OS

## Назначение

Agent OS превращает отдельные prompts и tools в управляемую систему. Она должна
отделять **что агент умеет** от **кто, когда и с какими полномочиями может это
запустить**.

## Слои

```text
Experience plane
  CLI · IDE · chat · dashboard · API · automation triggers
                         │
Control plane
  intent router · planner · scheduler · policy · approvals · budgets
                         │
Execution plane
  agents · workflows · models · tools · sandboxes · worktrees
                         │
Knowledge and state plane
  docs · specs · task graph · artifacts · memory · registry · provenance
                         │
Assurance plane
  evals · verification · security · tracing · metrics · audit · incident response
```

Assurance — сквозной слой, а не финальный этап.

## Реестр возможностей

Registry MUST хранить для каждого агента, workflow и tool:

- стабильный ID, owner и semantic version;
- purpose, inputs, outputs и examples;
- required permissions и risk class;
- поддерживаемые runtime/model;
- dependencies и compatibility range;
- evaluation status и last verified;
- lifecycle: experimental, active, deprecated, revoked;
- подпись, digest и provenance поставки.

Роутер выбирает не имя агента из prompt, а capability, удовлетворяющую policy и
контракту. Для внешних систем A2A Agent Card предоставляет discovery,
capabilities, interfaces и security schemes
([A2A specification](https://a2a-protocol.org/latest/specification/)).

## Control plane

Control plane отвечает за:

- нормализацию intent;
- выбор уровня автономности;
- построение DAG;
- проверку совместимости;
- выделение budget и permission envelope;
- lease/ownership;
- approvals и checkpoints;
- отмену, retries и recovery;
- итоговую synthesis/verification;
- policy decision log.

LLM может предложить план, но policy engine и scheduler SHOULD быть
детерминированными.

## Execution plane

Каждый run получает:

- immutable run ID и parent trace;
- agent/tool/model versions;
- isolated workspace или read-only view;
- scoped credentials;
- network policy;
- input snapshot и artifact refs;
- token/time/tool-call budget;
- cancellation signal;
- output sink и audit channel.

Worktree изолирует изменения файлов, но не обязательно `.git`, permissions,
plugins или secrets. Поэтому worktree MUST дополняться sandbox и policy
([Claude worktrees](https://code.claude.com/docs/en/worktrees)).

## State model

Разделяйте:

1. **Source state** — код, канонические specs, policies.
2. **Workflow state** — задачи, leases, checkpoints, retries.
3. **Session state** — текущий контекст и временные результаты.
4. **Memory** — проверенные повторно используемые знания.
5. **Observability data** — append-only traces, metrics и audit.
6. **Artifacts** — версии результатов с provenance.

Markdown удобен для людей и агентов, но task scheduler SHOULD иметь строгую
схему. GSD Core использует файловый `STATE.md`; GSD Pi сочетает локальную БД с
Markdown projections. Рекомендуемый компромисс: структурированное каноническое
состояние + человекочитаемые проекции, проверяемые на расхождение.

## Artifact protocol

Артефакт MUST иметь:

```yaml
artifact_id: spec-checkout-v3
type: specification
schema_version: 2
created_by: requirements-agent@1.4.0
run_id: run_...
sources: [prd@sha256:..., interview@sha256:...]
created_at: 2026-07-30T12:00:00Z
status: draft | reviewed | approved | superseded
owner: product-checkout
content_digest: sha256:...
```

Производные документы ссылаются на источники; изменение канонического документа
помечает зависимые артефакты stale.

## Policy и уровни автономности

| Уровень | Поведение |
|---|---|
| A0 | Только совет, без tools |
| A1 | Read-only tools |
| A2 | Локальные обратимые изменения |
| A3 | Внешние изменения с предварительным approval |
| A4 | Делегированные действия в заранее утверждённом envelope |
| A5 | Полностью автономный bounded loop с post-review |

Уровень назначается по сочетанию agent trust, action risk, data sensitivity и
environment. Агент не может сам повысить свой уровень.

## Runtime adapters

Универсальный контракт переводится в платформенные поверхности:

- Codex: AGENTS.md, skills, custom agents, sandbox и worktrees;
- Claude Code: CLAUDE.md, subagents, teams, hooks, workflows и worktrees;
- Cursor: rules, subagents, cloud agents, automations, Bugbot и approval agents;
- сервисные runtime: SDK, queue, sandbox, A2A/MCP и telemetry.

Адаптер MUST документировать несовпадения: глубину делегирования, наследование
permissions, resume, background behavior, tool syntax и supported metadata.

## Расширения

Практика GSD Pi полезна как модель:

- `core` — недеактивируемый минимум;
- `bundled` — поставляется с системой, но отключаем;
- `community` — внешнее расширение;
- manifest перечисляет version, compatibility, capabilities и dependencies;
- topological load order;
- уникальные namespaced tool IDs;
- state reconstruction на всех lifecycle events;
- bounded tool output и cancellation.

Расширение без manifest MAY работать в development, но не должно попадать в
управляемый registry.

## Lifecycle

```text
proposed → experimental → evaluated → active → deprecated → revoked → archived
```

Переходы требуют evidence. Revocation должна немедленно отключать новые runs и
определять судьбу уже запущенных. Upgrade выполняется через compatibility check,
canary evals и rollback.

## Минимальный Agent OS

Не начинайте с полной платформы. Достаточный MVP:

1. registry agents/tools;
2. task envelope и result envelope;
3. deterministic permission policy;
4. durable run/task state;
5. sandbox/worktree adapter;
6. traces и cost metrics;
7. eval suite;
8. human approval queue;
9. documentation index.

