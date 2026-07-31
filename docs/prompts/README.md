# Мастер-промпты для создания навыков по работе с агентами

Эти prompts создают **agent-oriented skills**: навыки, которые проектируют,
исследуют, оценивают, диагностируют, оптимизируют, управляют или оркестрируют
agents. Они не являются готовыми production agents и не дают права активировать
agent в runtime.

## Правило композиции

Всегда используйте:

```text
agent-skill-base.md + ровно один specialist prompt
```

Base задаёт общий skill-creation contract. Specialist prompt добавляет
agent-domain procedure. Не объединяйте все prompts в один mega-prompt.

## Маршрутизация

| Желаемый skill | Prompt |
|---|---|
| Ищет обоснованные возможности для agents | [agent-scout-skill.md](agent-scout-skill.md) |
| Собирает context из repositories/docs/traces | [agent-context-skill.md](agent-context-skill.md) |
| Проектирует одного agent или subagent | [agent-architect-skill.md](agent-architect-skill.md) |
| Создаёт evals и release evidence | [agent-evaluator-skill.md](agent-evaluator-skill.md) |
| Диагностирует и минимально исправляет | [agent-doctor-skill.md](agent-doctor-skill.md) |
| Улучшает здорового агента по метрике | [agent-optimizer-skill.md](agent-optimizer-skill.md) |
| Меняет boundaries и topology | [agent-refactor-skill.md](agent-refactor-skill.md) |
| Управляет registry, rollout и retirement | [agent-manager-skill.md](agent-manager-skill.md) |
| Оркестрирует полный lifecycle | [agent-builder-skill.md](agent-builder-skill.md) |
| Поддерживает evidence corpus практик | [agent-best-practices-skill.md](agent-best-practices-skill.md) |
| Собирает explicit composite toolkit | [agentkit-composite-skill.md](agentkit-composite-skill.md) |

## Team lifecycle prompts

Эти prompts также применяются после `agent-skill-base.md`:

| Желаемый skill | Prompt |
|---|---|
| Проектирует роли, topology и team contract | [agent-team-architect-skill.md](agent-team-architect-skill.md) |
| Управляет lifecycle и specialist routes | [agent-team-manager-skill.md](agent-team-manager-skill.md) |
| Материализует approved team spec | [agent-team-builder-skill.md](agent-team-builder-skill.md) |
| Исполняет approved team task graph | [agent-team-orchestrator-skill.md](agent-team-orchestrator-skill.md) |
| Сопоставляет agents и skills | [agent-skill-mapper-skill.md](agent-skill-mapper-skill.md) |
| Выбирает актуальные модели под роли | [agent-model-selector-skill.md](agent-model-selector-skill.md) |
| Управляет worktrees/workspaces | [agent-workspace-manager-skill.md](agent-workspace-manager-skill.md) |
| Управляет docs/wiki/graph knowledge | [agent-knowledge-manager-skill.md](agent-knowledge-manager-skill.md) |

## Agentic OS prompts

Для platform capability используй композицию:

```text
agent-skill-base.md + agent-os-base.md + ровно один Agentic OS specialist
```

| Plane/capability | Prompt |
|---|---|
| Architecture and ADRs | [agent-os-architect-skill.md](agent-os-architect-skill.md) |
| Walking skeleton bootstrap | [agent-os-bootstrapper-skill.md](agent-os-bootstrapper-skill.md) |
| Asset desired-state registry | [agent-registry-manager-skill.md](agent-registry-manager-skill.md) |
| Durable task/runtime lifecycle | [agent-runtime-manager-skill.md](agent-runtime-manager-skill.md) |
| Policy, approvals and credentials | [agent-policy-manager-skill.md](agent-policy-manager-skill.md) |
| Telemetry, SLO and incidents | [agent-observer-skill.md](agent-observer-skill.md) |
| Multi-model routing | [agent-model-router-skill.md](agent-model-router-skill.md) |
| MCP/A2A/host adapters | [agent-protocol-manager-skill.md](agent-protocol-manager-skill.md) |
| Independent platform evaluation | [agent-os-evaluator-skill.md](agent-os-evaluator-skill.md) |

Knowledge plane использует `agent-knowledge-manager-skill.md` с invariants из
`agent-os-base.md`; не создавай второй дублирующий knowledge skill без отдельного
permission/state/SLO boundary.

## Placement overlays

Перед созданием capability для конкретного agent запустите
[agent-capability-placement.md](agent-capability-placement.md). Он выбирает
inline rule, private command, private skill, public skill, tool/script или
workflow.

| Решение | Дополнительный prompt |
|---|---|
| Private agent skill | [agent-private-skill.md](agent-private-skill.md) после base + primary archetype |
| Private agent command | [agent-private-command.md](agent-private-command.md) |
| Promotion/demotion | [agent-skill-visibility-migration.md](agent-skill-visibility-migration.md) через `skill-refactor` |

Visibility overlay не является новым primary archetype. `private` означает
agent-scoped discovery/binding; он не делает файлы секретными.

Когда skill создаёт, изменяет, оценивает или активирует agent definition,
добавляйте [agent-documentation-contract.md](agent-documentation-contract.md)
как общий профиль. Он не заменяет specialist prompt.

## Входной envelope

Перед запуском нормализуйте запрос:

```yaml
skill_to_create: agent-architect
user_outcome: проектировать безопасных tool-using agents
target_hosts: [codex, claude-code]
agent_assets: [agent_card, workflow, eval_plan]
sources: []
examples:
  positive: []
  negative: []
authority:
  write_project: true
  install: false
  publish: false
  runtime_activate: false
constraints: []
destination: path/to/reviewable/bundle
```

Если `user_outcome`, target или destination материально неоднозначны, задайте
один–три вопроса. Для остальных пробелов используйте безопасные assumptions.

## Как применять

1. Полностью прочитать [agent-skill-base.md](agent-skill-base.md).
2. Выбрать один specialist prompt по observable outcome.
3. Передать user input, source artifacts, target-host rules и approvals.
4. Выполнить prompt, а не копировать его в итоговый `SKILL.md`.
5. Передать immutable candidate независимому `skill-evaluator`.
6. Installation/publication/runtime activation выполнять отдельным lifecycle
   действием после approval.

## Общие выходы

Каждый prompt должен создать или обновить reviewable skill bundle и вернуть:

- classification и capability boundary;
- положительные, отрицательные и ambiguous triggers;
- созданные files/resources;
- schemas agent artifacts;
- validation и eval evidence;
- authority, security и lifecycle risks;
- installation/publication status;
- точный следующий handoff.

## Терминология

- **Agent definition** — immutable design/configuration candidate.
- **Agent instance/run** — конкретное runtime исполнение.
- **Agent-oriented skill** — skill, который работает с definitions, runs,
  traces, registry или lifecycle.
- **Agent OS** — platform control/execution/knowledge/assurance/operations layer.
- **Activation** — разрешение runtime маршрутизировать реальные задачи к
  определённой agent version.
