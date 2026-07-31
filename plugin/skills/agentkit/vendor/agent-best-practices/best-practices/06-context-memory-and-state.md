# Контекст, память и состояние

## Четыре разных понятия

| Понятие | Горизонт | Пример |
|---|---|---|
| Context | Один model call/run | task brief, выбранные файлы |
| Session state | Один диалог | текущий plan, tool results |
| Workflow state | До завершения процесса | DAG, leases, checkpoints |
| Memory | Между runs | подтверждённые решения и learnings |

Смешивание этих слоёв создаёт stale decisions, неконтролируемое разрастание
prompt и невозможность recovery.

## Context engineering

Контекст — ограниченный бюджет. Формируйте его как пакет:

1. цель и acceptance criteria;
2. актуальные ограничения;
3. минимальные source excerpts или ссылки;
4. текущий state snapshot;
5. tools и permissions;
6. output contract;
7. открытые вопросы.

Порядок важен: high-signal инструкции и критерии не должны тонуть в raw logs.
Большие tool outputs обрезаются, сохраняются как артефакт и передаются ссылкой.
GSD Pi устанавливает явный предел на переменный вывод tools как защиту от
context overflow ([репозиторий](https://github.com/open-gsd/gsd-pi)).

## Progressive disclosure

Агент сначала получает индекс и summaries, затем загружает детали по запросу:

```text
docs/INDEX.md
  → domain summary
    → canonical document
      → code/test evidence
```

Не загружайте весь `docs/`, всю память или все tools «на всякий случай».
Retrieval должен учитывать scope, freshness, authority и permission.

## Durable state

Значимое решение MUST быть записано до контекстной границы или dispatch.
Хороший state spine содержит:

- текущую цель/phase;
- статус задач и owners;
- принятые решения;
- blockers и approvals;
- ссылки на artifacts;
- последнее доказанное состояние;
- resume instruction.

GSD Core показывает преимущество plain-text `.planning/STATE.md`; OpenSpec —
change folders; gstack — context-save/context-restore. Общий паттерн: важное
состояние живёт вне диалога, версионируется и читается новым контекстом.

## Memory pipeline

```text
candidate → sanitize → verify → classify → approve → store → retrieve → revalidate
```

Memory item SHOULD иметь:

```yaml
id: learning-checkout-timeout
type: decision | fact | preference | pitfall | procedure
content: ...
source_refs: [...]
confidence: 0.9
scope: repo:checkout
owner: checkout-team
created_at: ...
last_verified_at: ...
expires_at: ...
sensitivity: internal
status: candidate | approved | stale | revoked
```

Автоматически найденная «информация» остаётся candidate до проверки. Cursor
предупреждает, что persistent memories могут быть отравлены недоверенным input
([automations](https://cursor.com/docs/cloud-agent/automations)).

## Что хранить

Храните:

- устойчивые решения с rationale;
- подтверждённые особенности codebase;
- повторяющиеся failure modes и fixes;
- предпочтения пользователя с явным scope;
- проверенные команды и runbooks;
- итоги ретроспектив и eval regressions.

Не храните:

- secrets и токены;
- необработанный chain-of-thought;
- неподтверждённые предположения как факты;
- случайные tool outputs;
- персональные данные без основания;
- сведения без provenance или срока пересмотра.

## Сводка и compaction

Сводка MUST сохранять:

- цель;
- решения и их основания;
- изменения и hashes;
- проверки;
- незавершённое и blockers;
- следующую конкретную операцию.

Она не должна быть хронологическим пересказом. Сравнивайте summary с durable
artifacts; при расхождении источник истины — проверенный artifact/code, а не
текст сводки.

## Восстановление

Resume protocol:

1. определить repo/worktree/branch;
2. загрузить task/workflow state;
3. проверить, что referenced commits и artifacts существуют;
4. выявить drift с момента checkpoint;
5. подтвердить leases и истечение approvals;
6. восстановить только необходимый context;
7. продолжить с первой незавершённой проверяемой операции.

Нельзя просто доверять строке «продолжить с шага 4» без проверки живого
состояния.

## Knowledge freshness

У документа или memory item должны быть owner и обновляющий триггер:

- изменение API/code path;
- релиз;
- incident;
- изменение policy;
- истечение review period;
- выявленный конфликт;
- провал eval.

Stale knowledge не удаляется молча: оно помечается, исключается из
автоматического применения и отправляется владельцу на review.
