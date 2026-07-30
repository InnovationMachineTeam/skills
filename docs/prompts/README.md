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
| Проектирует agent/subagent/team/orchestrator | [agent-architect-skill.md](agent-architect-skill.md) |
| Создаёт evals и release evidence | [agent-evaluator-skill.md](agent-evaluator-skill.md) |
| Диагностирует и минимально исправляет | [agent-doctor-skill.md](agent-doctor-skill.md) |
| Улучшает здорового агента по метрике | [agent-optimizer-skill.md](agent-optimizer-skill.md) |
| Меняет boundaries и topology | [agent-refactor-skill.md](agent-refactor-skill.md) |
| Управляет registry, rollout и retirement | [agent-manager-skill.md](agent-manager-skill.md) |
| Оркестрирует полный lifecycle | [agent-builder-skill.md](agent-builder-skill.md) |
| Поддерживает evidence corpus практик | [agent-best-practices-skill.md](agent-best-practices-skill.md) |
| Собирает explicit composite toolkit | [agentkit-composite-skill.md](agentkit-composite-skill.md) |

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
