# Каталог паттернов навыков

## Навык как capability package

Skill — versioned пакет инструкций, references, scripts и evals, который
предоставляет ограниченную capability агенту. Он не обязан быть агентом:
agent владеет целью и runtime-решениями, skill задаёт повторяемый метод или
специализацию, tool исполняет операцию, workflow координирует шаги.

Хороший skill имеет узкую семантическую границу, точное описание триггера,
progressive disclosure, проверяемый результат и явные permissions/side effects.

## Структурные паттерны

### Atomic skill

Одна capability, один класс intent, один основной workflow. Это default: проще
trigger evals, versioning, reuse и least privilege. Разделяйте skill, если его
режимы требуют разных owners, прав, контекстов или release cadence.

### Method skill

Инкапсулирует метод: threat modeling, migration review, requirements linting.
`SKILL.md` хранит decision process и навигацию, подробные rubrics/templates — в
references. Метод обязан определять вход, выход, stop conditions и evidence.

### Adapter skill

Переводит канонический процесс на платформу или toolchain: Claude Code, Codex,
Cursor, GitHub. Core semantics остаётся общей, adapter содержит только команды,
manifest rules и platform limits. Это предотвращает дублирование всей логики.

### Script-backed skill

Детерминированные, повторяемые или чувствительные операции выполняет script, а
модель готовит параметры, интерпретирует результат и обрабатывает исключения.
Scripts используют explicit arguments, dry-run, typed output, stable exit codes,
idempotency и tests. Скрипт не должен скрывать изменение внешнего состояния.

### Reference-backed skill

Основной файл кратко маршрутизирует к тематическим references. Каждый reference
имеет понятный триггер чтения; данные с высокой изменчивостью содержат source,
checked date и refresh procedure. Копия документации без provenance становится
скрытым fork.

### Generator–validator pair

Одна часть создаёт artifact, другая независимо проверяет schema, semantics и
task outcome. Validator может быть script, eval suite или отдельный read-only
skill. Авторский self-check полезен, но не заменяет независимый gate.

### Context-builder

Skill собирает минимальный evidence pack до основной работы: questions,
sources, code/doc excerpts, assumptions и gaps. Inbox — временная staging area,
а не каноническая память; финальная synthesis должна удалить дубликаты, отметить
конфликты и сохранить provenance.

### Evaluator skill

Описывает dataset, positive/negative triggers, rubrics, graders, thresholds,
variance policy и regression comparison. Он не должен менять оцениваемый skill
во время одного evaluation run.

### Guard / decorator

Добавляет preflight, approval, security scan или postcondition к другому skill.
Composition order MUST быть явным. Guard в prompt не является enforcement:
реальный блокирующий control располагается у tool/runtime boundary.

## Композиционные паттерны

### Composite / skillpack

Единая точка входа маршрутизирует к нескольким donor skills или встроенным
режимам. Нужны:

- непересекающиеся mode contracts и explicit command form;
- default/fallback behavior при неоднозначности;
- donor manifest с точными versions и compatibility range;
- provenance каждого заимствованного prompt/script/reference;
- запрет скрытого редактирования donors;
- integration и routing evals поверх evals каждого donor;
- upgrade workflow с diff, migration notes, eval gate и rollback.

Skillpack оправдан общим user journey, но не желанием скрыть большое число
несвязанных skills под одним именем.

### Router skill

Классифицирует intent и запускает один подходящий capability. Description
отвечает «когда использовать», а не перечисляет внутренности. Проверяйте
пересекающиеся intents, near-miss negative triggers, confidence и вопросы для
недостающего контекста.

### Strategy / mode

Общий domain имеет несколько algorithms: `create`, `optimize`, `doctor`,
`evaluate`. Mode contract фиксирует дополнительные arguments и side effects.
Если modes развиваются независимо, оставьте их отдельными donor skills и
используйте router/composite только как facade.

### Pipeline skill

Шаги образуют стабильный artifact flow: context → design → build → evaluate →
package. Каждый stage имеет schema и может быть возобновлён. Если порядок
динамический, orchestration должна находиться в workflow/agent, а skill —
предоставлять отдельные capabilities.

### Extension point

Core skill публикует versioned hook contract, а extensions добавляют domain или
platform behavior без правки core. Hook declaring side effects, order,
timeout, failure semantics и compatibility обязательны. Не выполняйте найденные
extensions автоматически только по имени файла.

## Паттерны описания и активации

### Trigger contract

Description содержит capability + ситуацию/intent + ключевые ограничения. Он не
должен обещать более широкий outcome, чем поддерживает skill. Полезный формат:

```text
Use when <user intent/context>. Handles <bounded capability> and produces
<artifact/outcome>. Do not use for <nearest confusing alternatives>.
```

### Progressive disclosure

1. Registry загружает name/description.
2. При выборе читается весь `SKILL.md`.
3. References/scripts/assets открываются только по явной routing instruction.

Основной файл — control document, не энциклопедия. Но критические safety rules и
порядок действий не прячутся глубоко в references.

### Decision table

Когда branching зависит от 2–4 признаков, используйте таблицу вместо длинной
прозы. Для каждого route задайте вход, required context, action, output и
fallback. Большой динамический граф следует вынести в workflow-as-code.

## Lifecycle-паттерны навыков

### Source-of-truth manifest

Manifest фиксирует name, semantic version, owner, publisher, status, license,
dependencies, compatibility, permissions, data handling, entrypoint, eval refs,
provenance и replacement. YAML frontmatter не должен быть единственным местом,
если marketplace требует отдельный canonical manifest; поля синхронизируются
validator-ом.

### Donor lock and upgrade

Composite skill хранит donor, resolved version, source commit/content hash,
included components и transformation notes. Upgrade:

1. разрешает текущие и доступные versions;
2. завершает без изменений, если hashes совпадают;
3. показывает semantic и file diff;
4. проверяет compatibility/migrations;
5. пересобирает candidate, не active version;
6. запускает donor + integration + regression evals;
7. публикует и canary-promotes только после gate;
8. сохраняет rollback target.

### Deprecation bridge

Deprecated skill остаётся discoverable ограниченное время, предупреждает о
replacement, содержит migration guide и перестаёт принимать новые dependents.
Retirement удаляет routes/credentials, но сохраняет immutable release и audit
metadata для воспроизводимости старых runs.

### Harvest–curate–publish

External material сначала помещается в quarantine/inbox, затем проходит license,
security, provenance, relevance и duplication review. Извлечённый паттерн
переписывается под локальный контракт и evals; чужой skill не публикуется как
доверенный только потому, что его можно скачать.

## Минимальные evals

| Слой | Что проверять |
|---|---|
| Discovery | skill находится по целевым формулировкам |
| Negative triggers | не активируется на соседних и опасных intents |
| Routing | выбирает правильный mode и задаёт нужные вопросы |
| Procedure | соблюдает required order, gates и stop conditions |
| Artifact | schema, correctness, completeness и usability |
| Tool/script | exit codes, errors, dry-run, idempotency, portability |
| Safety | permissions, prompt injection, secrets, destructive actions |
| Composition | donor compatibility, context transfer, no hidden mutation |
| Regression | новый release не ухудшает согласованные baselines |

## Антипаттерны навыков

- **Mega-skill** — несвязанные capabilities, общий контекст и широкие права.
- **Trigger soup** — description перечисляет все возможные слова и конкурирует со
  всем marketplace.
- **Prompt-only enforcement** — запрет существует только как текстовая просьба.
- **Hidden side effect** — install, network write или publish без preflight.
- **Reference maze** — вложенные ссылки без routing и обязательного порядка.
- **Copied knowledge snapshot** — нет источника, даты и refresh policy.
- **Scripts as opaque binaries** — неясные inputs, outputs и changes.
- **Auto-upgrade in place** — active behavior меняется до diff и evals.
- **Version without semantics** — номер есть, compatibility и migrations нет.
- **Evals written to implementation** — tests подтверждают шаги, а не outcome.
- **Composite that edits donors** — невозможно воспроизвести или обновить пакет.
- **Skill as implicit agent** — skill начинает ставить новые цели и делегировать
  вне пользовательского intent.

## Решение: skill, agent, tool или workflow

| Нужда | Основной механизм |
|---|---|
| Повторяемая инструкция/метод | Skill |
| Детерминированное действие | Tool/script |
| Адаптивное достижение bounded goal | Agent |
| Стабильная последовательность и durable state | Workflow |
| Единая точка входа к связанным capabilities | Router/composite skill |
| Политика и блокировка действий | Policy service + enforcement point |

Часто правильна композиция: workflow вызывает агента, агент активирует skill,
skill подготавливает безопасный tool call, runtime применяет policy.
