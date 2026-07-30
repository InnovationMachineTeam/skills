# Проектирование агента и его контракт

## Минимальная спецификация агента

Каждый production-агент MUST иметь версионируемый контракт:

```yaml
id: requirements-analyst
version: 1.0.0
purpose: Преобразовать проверенный intent в тестируемые требования
owns:
  - docs/requirements/
inputs:
  required: [intent, stakeholders, constraints]
  optional: [research, existing_specs]
outputs:
  schema: requirements-report-v1
  artifacts: [requirements.md, traceability.md]
tools:
  allow: [read_repo, search_docs, write_docs]
  deny: [deploy, delete, send_external]
permissions: read-mostly
done_when:
  - every requirement has id, rationale and verification
  - unresolved ambiguity is explicit
escalate_when:
  - two authoritative sources conflict
  - a high-impact decision lacks an accountable owner
budgets:
  max_turns: 12
  max_duration_minutes: 20
```

Синтаксис конкретного runtime может отличаться, но семантические поля должны
сохраняться.

## Инструкции

Хорошая инструкция отвечает на семь вопросов:

1. Какой результат агент создаёт?
2. Что он не делает?
3. Какие источники истины и в каком порядке использует?
4. Какие инструменты доступны и когда?
5. Как выглядит готовый результат?
6. Что проверяется перед завершением?
7. Когда агент останавливается и зовёт человека?

Практичный каркас:

```markdown
## Role
Узкая компетенция и ответственность.

## Goal
Наблюдаемый результат, а не список действий.

## Inputs and precedence
Источники, freshness и порядок разрешения конфликтов.

## Scope
In scope, out of scope, write-set.

## Process
Ключевые решения и gates; не микроменеджмент очевидных действий.

## Output contract
Схема ответа, артефакты, evidence и статус.

## Validation
Команды, rubrics, независимые проверки.

## Escalation and stop conditions
Блокеры, риск, бюджет и ожидание пользователя.
```

Инструкции SHOULD быть конкретными и декларативными. Важные запреты оформляются
как MUST NOT с причиной и проверкой. Не смешивайте persona, workflow и
платформенные обходные пути в одном неструктурированном тексте.

## Контракт задачи

Оркестратор передаёт не «помоги с проектом», а task envelope:

```yaml
task_id: REQ-042
objective: Найти пропущенные quality requirements для checkout
context_refs:
  - docs/product/prd.md
  - docs/architecture/context.md
constraints:
  - read_only: true
  - cite_file_and_line: true
expected_output:
  schema: review-findings-v1
acceptance:
  - findings classified by severity
  - every finding contains evidence and proposed verification
dependencies: []
deadline: 2026-07-30T16:00:00Z
```

Контекст передаётся ссылками и компактной выжимкой. Родитель не должен полагать,
что субагент видит историю диалога: Claude, Codex и Cursor подчёркивают
изолированный контекст субагентов
([Claude](https://code.claude.com/docs/en/sub-agents),
[Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[Cursor](https://cursor.com/docs/subagents)).

## Контракт результата

Результат MUST отличать выполненную работу от заявления о ней:

```yaml
task_id: REQ-042
status: completed | partial | blocked | failed
summary: Короткий вывод
artifacts:
  - path: docs/requirements/checkout-quality.md
    sha256: ...
evidence:
  - claim: p95 latency requirement is missing
    source: docs/product/prd.md#checkout
verification:
  - command: markdownlint docs/requirements/checkout-quality.md
    status: pass
open_questions: []
risks: []
handoff_to: requirements-owner
```

MUST возвращать частичный результат при отмене или исчерпании бюджета, если он
безопасен и полезен. `completed` недопустим без доказательств критериев done.

## Инструменты

Инструмент — часть интерфейса агента, а не просто API. Каждый tool SHOULD иметь:

- уникальное глагольное имя;
- одно назначение;
- строгую схему аргументов и результата;
- описание предусловий и side effects;
- примеры типичного и пограничного вызова;
- идемпотентность или idempotency key;
- понятные ошибки, позволяющие самокоррекцию;
- timeout, cancellation и bounded output;
- классификацию риска и requirement approval;
- audit event без лишних секретов.

Скрывайте редко используемые и опасные инструменты до момента необходимости.
Похожие инструменты объединяйте или делайте названия и параметры явно
различимыми. OpenAI и Anthropic связывают качество агента с качеством tool
interface ([OpenAI](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/),
[Anthropic](https://www.anthropic.com/engineering/building-effective-agents)).

## Ошибки и восстановление

Минимальная таксономия:

| Тип | Действие |
|---|---|
| Validation error | Исправить аргументы, одна ограниченная повторная попытка |
| Transient | Backoff + jitter в пределах retry budget |
| Auth / permission | Остановиться и запросить нужную авторизацию без вывода секрета |
| Policy denial | Не обходить; вернуть причину и безопасную альтернативу |
| Dependency unavailable | Зафиксировать состояние, предложить resume |
| Ambiguous high-impact choice | Human checkpoint |
| Irreversible side effect uncertain | Fail closed |
| Budget exceeded | Partial handoff + resume token |

Retry MUST быть привязан к типу ошибки. Повтор того же запроса без изменения
условий — не стратегия восстановления.

## Версии и совместимость

- Версионируйте agent contract, prompt, tool schema и output schema отдельно.
- Breaking change входа, выхода или полномочий требует major version.
- Оркестратор MUST проверять совместимость перед dispatch.
- В trace записываются фактические версии агента, модели, tools и policy.
- Поведение должно тестироваться на фиксированном corpus до и после обновления.

