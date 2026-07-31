# Лучшие практики создания агентных систем

Этот каталог — практическое руководство по проектированию агентов, субагентов,
оркестраторов, команд агентов и Agent OS. Он объединяет официальные рекомендации
OpenAI, Anthropic, Claude Code, Cursor, Google ADK, A2A, MCP и Microsoft с
паттернами из Agent OS, BMAD, GSD Core, GSD Pi, gstack, Spec Kit и OpenSpec.

Актуальность исследования: **2026-07-30**. Ограничения и численные лимиты
конкретных платформ следует перепроверять по ссылкам в файлах источников.

## Быстрый маршрут

1. Начните с [01-foundations-and-selection.md](01-foundations-and-selection.md),
   чтобы выбрать минимально достаточную архитектуру.
2. Оформите контракт агента по
   [02-agent-design-and-contracts.md](02-agent-design-and-contracts.md).
3. Если нужна декомпозиция, используйте
   [03-subagents-and-delegation.md](03-subagents-and-delegation.md) и
   [04-orchestration-and-agent-teams.md](04-orchestration-and-agent-teams.md).
4. Для платформенного слоя смотрите
   [05-agent-os-reference-architecture.md](05-agent-os-reference-architecture.md).
5. Для проектной документации —
   [07-documentation-as-operating-system.md](07-documentation-as-operating-system.md)
   и [08-docs-catalog-and-templates.md](08-docs-catalog-and-templates.md).
6. Роли и процессы находятся в
   [09-agent-role-catalog.md](09-agent-role-catalog.md) и
   [10-lifecycle-and-orchestration-processes.md](10-lifecycle-and-orchestration-processes.md).
7. Требования, наблюдаемость, безопасность и evals разобраны в файлах 11–14.
8. Практические реализации и разрешённые противоречия — в файлах 15–16.
9. Для углублённого проектирования используйте каталоги паттернов агентов,
   Agent OS и skills в файлах 17–19.
10. Циклы, lifecycle, ролевое разделение и operating model находятся в файлах
    20–22.

## Основной принцип

> Используйте наименее сложную архитектуру, которая стабильно достигает
> требуемого качества, безопасности и времени выполнения.

Порядок усложнения:

```text
детерминированный код
  → один вызов модели
  → workflow из вызовов
  → один агент с инструментами
  → менеджер + субагенты
  → команда агентов
  → распределённая Agent OS
```

Переход на следующий уровень оправдан только измеримым выигрышем в evals или
необходимостью разделить контекст, инструменты, права, владение или параллельную
работу. Больше агентов означает больше задержки, стоимости, состояний отказа и
поверхности атаки.

## Нормативные слова

- **MUST** — обязательное правило; нарушение делает систему небезопасной или
  ненадёжной.
- **SHOULD** — рекомендуемое правило; отклонение документируется.
- **MAY** — допустимый вариант.
- **Платформенное правило** — факт конкретного runtime, а не универсальная
  практика. Такие правила вынесены в адаптеры или помечены названием платформы.

## Карта файлов

| Файл | Назначение |
|---|---|
| `01-foundations-and-selection.md` | Термины, критерии выбора и лестница сложности |
| `02-agent-design-and-contracts.md` | Контракт, инструкции, инструменты, выходы и ошибки |
| `03-subagents-and-delegation.md` | Границы задач, handoff, контекст и владение файлами |
| `04-orchestration-and-agent-teams.md` | Топологии, параллелизм, команды и workflow-as-code |
| `05-agent-os-reference-architecture.md` | Control plane, execution plane, state, policy и registry |
| `06-context-memory-and-state.md` | Контекст, долговременная память и восстановление |
| `07-documentation-as-operating-system.md` | `docs/` как разделяемая память людей и агентов |
| `08-docs-catalog-and-templates.md` | Варианты документов, дерево и минимальные шаблоны |
| `09-agent-role-catalog.md` | Типовые агенты PDLC/SDLC/ADLC/Discovery/Delivery |
| `10-lifecycle-and-orchestration-processes.md` | Сценарии от discovery до эксплуатации |
| `11-requirements-and-quality-attributes.md` | FR, quality attributes, constraints и traceability |
| `12-task-tracking-monitoring-and-observability.md` | Состояния задач, события, метрики и дашборды |
| `13-security-approvals-and-governance.md` | Least privilege, approvals, isolation и supply chain |
| `14-evaluation-and-continuous-improvement.md` | Evals агентов, команд, маршрутизации и production |
| `15-implementation-case-studies.md` | Сравнение семи исследованных репозиториев |
| `16-conflicts-and-resolutions.md` | Противоречия практик и принятые решения |
| `17-agent-and-orchestration-pattern-catalog.md` | Паттерны одного агента, делегирования, оркестраторов и команд |
| `18-agent-os-and-runtime-pattern-catalog.md` | Control/execution/knowledge/assurance/operations patterns Agent OS |
| `19-skill-design-pattern-catalog.md` | Atomic, composite, adapter, script, eval и lifecycle patterns skills |
| `20-agentic-cycles-and-lifecycles.md` | ReAct, OODA, MAPE-K, PDCA, ADLC и lifecycle assets |
| `21-role-patterns-and-separation-of-duties.md` | Ролевые архетипы, accountability и separation of duties |
| `22-operating-model-and-pattern-selection.md` | Selection model, recipes, risk tiers и maturity |
| `sources-platforms.md` | Платформенные и протокольные источники |
| `sources-frameworks.md` | Репозитории и практические реализации |
| `sources-standards-and-docs.md` | Стандарты, безопасность и документация |
| `sources-patterns-and-cycles.md` | Каталоги паттернов, циклы и operating sources |

## Что этот каталог не утверждает

- Многоагентность не является целью сама по себе.
- Worktree — это изоляция изменений, но не полноценная security boundary.
- LLM-review не заменяет автоматические проверки и ответственного человека.
- Память не является источником истины без provenance, срока жизни и проверки.
- Документ, который не имеет владельца, триггера обновления и потребителя,
  быстро становится шумом.
