# Оркестрация и команды агентов

## Выбор control plane

| Control plane | Сильная сторона | Основной риск |
|---|---|---|
| Код / state machine | Предсказуемость, тестируемость, бюджет | Слабая адаптация к новому |
| LLM-оркестратор | Динамическая декомпозиция и routing | Непредсказуемость и drift |
| Гибрид | Код держит gates, LLM решает локально | Сложнее интерфейсы |

По умолчанию используйте гибрид: программа владеет lifecycle, permissions,
budgets и durable state; модель — классификацией, планированием и выбором внутри
ограниченного набора действий. OpenAI Agents SDK явно разделяет LLM и code
orchestration, а Google ADK предлагает deterministic sequential, parallel и loop
workflows ([OpenAI](https://openai.github.io/openai-agents-python/multi_agent/),
[Google ADK](https://adk.dev/agents/workflow-agents/)).

## Основные топологии

### Router

Классифицирует запрос и передаёт его одному специалисту. Хорош для непересекающихся
доменов. Routing output MUST быть типизирован, иметь confidence и fallback.

### Manager / agents as tools

Менеджер остаётся владельцем диалога, вызывает специалистов и синтезирует
результат. Выбирайте, когда нужна единая политика, тон ответа или финальная
ответственность.

### Handoff network

Специалист получает контроль и может передать его дальше. Подходит для service
triage, но требует защиты от ping-pong, максимума переходов и route history.

### Orchestrator–workers

Оркестратор динамически строит подзадачи, workers выполняют их, затем результат
собирается и проверяется. Лучший случай — сложная работа, где число и тип частей
неизвестны заранее.

### Pipeline

Последовательные узкие агенты: research → plan → implement → verify. Полезен,
когда выход каждого шага является контрактным входом следующего.

### Fan-out / fan-in

Независимые специалисты работают параллельно, aggregator нормализует и
разрешает конфликты. Используйте для разных источников, аспектов review или
competing hypotheses.

### Evaluator–optimizer

Producer улучшает артефакт по feedback evaluator до pass или бюджета. Критерии
и лимит должны задаваться до запуска.

### Debate / jury

Несколько независимых кандидатов и судья. Применяется там, где diversity
обоснована evals. Участники не должны видеть ответы друг друга до первой оценки,
иначе независимость фиктивна.

## Команда агентов

Команда нужна не для любой параллельности. В отличие от субагентов, peers могут
координироваться напрямую и разделять task board. Это полезно для:

- параллельного исследования с обменом открытиями;
- разделения frontend/backend/infra с чёткими interfaces;
- проверки конкурирующих debugging hypotheses;
- adversarial review, где критики оспаривают план друг друга;
- длительных работ, где lead перераспределяет задачи.

Не используйте team для строгой последовательности, короткой задачи, сильного
пересечения файлов или когда все решения должен принимать один контекст.

Claude рекомендует начинать с 3–5 teammates и нескольких чётких задач на
каждого, но это платформенная эвристика, не универсальная норма
([agent teams](https://code.claude.com/docs/en/agent-teams)). Начните с 2–3
исполнителей и масштабируйте после измерения bottleneck.

## Командный charter

Перед запуском команда получает:

```yaml
mission: Доказать готовность checkout к релизу
lead: release-orchestrator
members:
  - id: qa
    owns: [tests/e2e/**]
  - id: security
    mode: read_only
  - id: reliability
    owns: [docs/runbooks/checkout.md]
shared_artifacts:
  task_board: .agent/tasks.json
  decisions: docs/decisions/
communication:
  message_schema: agent-message-v1
  max_rounds: 4
merge_owner: lead
exit:
  - all blocking tasks terminal
  - release gate evaluated
```

MUST определить lead, owners, каноническое состояние, протокол сообщений,
write-set, merge owner и stop conditions.

## Task graph и scheduler

Каждая задача имеет:

- стабильный ID;
- parent goal и acceptance criteria;
- зависимости;
- owner и lease;
- risk class и approvals;
- input/output refs;
- status и timestamps;
- attempt, budget и heartbeat;
- evidence и terminal reason.

Scheduler MUST предотвращать двойное владение, проверять leases и не считать
задачу завершённой по одному сообщению агента. Состояние переходов должно быть
машиночитаемым и идемпотентным.

## Workflow-as-code

Когда сценарий повторяется или содержит десятки шагов, план переносится из
prompt в version-controlled code. Claude Code workflows подчёркивают, что код
держит план и промежуточное состояние, а в основной контекст возвращается
финальный результат ([workflows](https://code.claude.com/docs/en/workflows)).

Workflow SHOULD иметь:

- dry-run и визуализацию плана;
- deterministic gates и typed payloads;
- checkpoints/resume;
- retry и compensation policy;
- unit tests для routing и transitions;
- trace correlation;
- возможность отмены;
- явный human-in-the-loop;
- ограниченный набор разрешённых agents/tools.

Перед выполнением сгенерированного workflow человек должен видеть его raw plan,
особенно side effects и сеть.

## Разрешение конфликтов

Aggregator не должен «усреднять» несовместимые результаты. Он:

1. нормализует claims и evidence;
2. отличает factual conflict от различия предпочтений;
3. проверяет authoritative sources и freshness;
4. запрашивает дополнительное доказательство;
5. применяет предопределённую policy;
6. передаёт человеку high-impact неоднозначность.

Решение фиксируется как ADR/decision record с отклонёнными альтернативами.

## Distributed-systems reality

Многоагентная система наследует проблемы распределённых систем: duplicate
delivery, потерю сообщений, split brain, stale reads, network partition,
cascading retries и orphan jobs. Microsoft рекомендует учитывать эти режимы до
выбора multi-agent pattern
([Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)).

Применяйте correlation IDs, idempotency keys, leases, heartbeats, durable queue,
dead-letter state, backpressure, circuit breakers и reconciliation jobs.
