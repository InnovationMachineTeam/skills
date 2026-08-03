# skill-marketplace-manager

`skill-marketplace-manager` — мета-навык для проектирования, сборки, проверки, миграции и выпуска репозиториев навыков. Он ориентирован на переносимый Agent Skills layout, skill.sh и plugin harnesses, прежде всего Claude Code.

> Текущий статус: `1.4.0`. Навык создан как reviewable package. Он не выполняет публикацию, глобальную установку, удаление прежней структуры или миграционный cutover без явного разрешения.

## Что решает навык

Навык помогает ответить на вопросы уровня всего каталога:

- где находится канонический источник навыков;
- как организовать `skills/` и категории;
- как совместить skill.sh и Claude Code;
- нужен ли один aggregate plugin или несколько marketplace entries;
- как генерировать самодостаточный plugin bundle;
- как управлять версиями навыков и дистрибутива;
- как объявлять и проверять companion-зависимости без неподдерживаемых полей manifests;
- как проверить обнаружение, установку, обновление и rollback;
- как безопасно перенести существующий портфель в marketplace.

Он не заменяет `skill-architect` для проектирования поведения отдельного навыка и `skill-evaluator` для независимой оценки качества его работы.

## Режимы работы

| Маршрут | Типичный запрос | Результат |
|---|---|---|
| `inventory-audit` | «Проверь этот репозиторий навыков» | inventory, manifest map, collisions, risks |
| `architecture-design` | «Спроектируй marketplace для skill.sh и Claude Code» | целевая архитектура и ADR-подобное решение |
| `scaffold-marketplace` | «Создай каркас marketplace» | локальная структура, manifests, templates |
| `catalog-curation` | «Добавь/переклассифицируй навыки» | mapping и согласованные изменения каталога |
| `build-sync` | «Собери aggregate plugin» | самодостаточный generated bundle и hashes |
| `documentation` | «Документируй навыки и подготовь onboarding» | README, onboarding guide или audit report на основе канонических источников |
| `validate-compatibility` | «Проверь совместимость и установку» | evidence report с PASS/WARN/FAIL/NOT RUN |
| `migration` | «Перенеси текущие навыки в marketplace» | сначала DRAFT-план; apply только явно |
| `release-distribution` | «Подготовь или выпусти релиз» | release plan/package/pilot; публикация по разрешению |

Дополнительно применяется режим полномочий:

- `inspect` — только чтение;
- `plan` — план без изменений;
- `apply` — разрешённые локальные изменения;
- `verify` — проверки без автоматического ремонта.

Можно назвать маршрут прямо:

```text
Используй skill-marketplace-manager в режиме inventory-audit для ./repo.
```

Или описать цель естественным языком:

```text
Подготовь этот набор навыков к установке через skill.sh и Claude Code,
но пока ничего не публикуй.
```

Если контекста недостаточно, навык уточнит только решения, которые меняют архитектуру: целевые harnesses, visibility, canonical source, release boundary или допустимые мутации.

## Рекомендуемый workflow

```text
inventory-audit
      ↓
architecture-design
      ↓
scaffold-marketplace / catalog-curation
      ↓
build-sync
      ↓
validate-compatibility
      ↓
migration pilot или release-distribution
      ↓
cutover / rollout / rollback decision
```

Для существующего каталога начинать с `inventory-audit`. Для нового репозитория — с `architecture-design`. Для критичной миграции всегда отделять `plan` от `apply`.

## Рекомендуемая структура

```text
marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── skills/                         # canonical source
│   ├── metaskills/
│   ├── agent-workflows/
│   ├── product/
│   ├── development/
│   └── marketing/
├── plugin/                         # generated aggregate bundle
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   └── build-manifest.json
├── scripts/
├── tests/
└── README.md
```

Подробное обоснование находится в [references/best-practices.md](references/best-practices.md).

## Команды потребителей

skill.sh / Skills CLI:

```bash
npx skills add owner/repository --list
npx skills add owner/repository --skill skill-architect --agent claude-code --agent codex
```

Claude Code marketplace:

```text
/plugin marketplace add owner/repository
/plugin install metaskills@marketplace-name
```

Claude Code CLI:

```bash
claude plugin marketplace add owner/repository
claude plugin install metaskills@marketplace-name
claude --plugin-dir ./plugin
```

Не устанавливайте один и тот же навык через два канала в одну область видимости.

## Встроенные утилиты

### Portable validation

```bash
python3 scripts/validate_marketplace.py /path/to/marketplace
python3 scripts/validate_marketplace.py /path/to/marketplace --json
```

Проверяется:

- допустимая глубина `skills/`;
- `SKILL.md`, имя каталога и `metadata.version`;
- глобальная уникальность имён;
- небезопасные локальные ссылки;
- базовая структура marketplace и plugin manifests;
- существование объявленных локальных путей.

Эта проверка не заменяет официальные harness validators.

### Aggregate plugin build

```bash
python3 scripts/build_plugin_bundle.py /path/to/marketplace /new/staging/plugin \
  --plugin-name skill-toolkit \
  --version 1.0.0 \
  --description "Portable skill engineering toolkit"
```

Утилита принимает только новый output directory, копирует полные skill packages, исключает стандартный мусор (`.DS_Store`, `__pycache__`, `*.pyc`, `.git`), создаёт `plugin.json` и `build-manifest.json`. Она отклоняет symlinks и не удаляет существующие каталоги.

### Eval corpus

```bash
python3 scripts/check_evals.py evals
```

Проверяет целостность routing и behavioral cases. Harness-native или независимый evaluator должен отдельно выполнить сами кейсы.

## Полная проверка перед релизом

```bash
python3 scripts/validate_marketplace.py .
npx skills add . --list
claude plugin validate .
claude plugin validate ./plugin --strict
claude --plugin-dir ./plugin
```

Дополнительно прогнать trigger evals, behavior evals, обновление с предыдущей версии и security review. Если инструмент отсутствует, результат обозначается `NOT RUN`.

## Версии

- `SKILL.md → metadata.version` относится к одному навыку.
- `.claude-plugin/plugin.json → version` относится к plugin bundle.
- marketplace entry version относится к устанавливаемому предложению каталога.

Версии не должны автоматически считаться одинаковыми. При изменении устанавливаемого содержимого требуется новый distribution release.

## Безопасность

- Внешние навыки считать supply-chain input.
- До запуска изучать scripts и provenance.
- Не хранить secrets в skill packages, manifests, fixtures и логах.
- Собирать в staging, затем проверять и только потом продвигать.
- Проводить пилот до широкого rollout.
- Хранить предыдущий known-good release до завершения окна rollback.
- Публикация, глобальная установка и удаление требуют отдельного явного решения.

## Состав пакета

```text
skill-marketplace-manager/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── prompts/
├── references/
│   ├── best-practices.md
│   ├── integration-contracts.md
│   ├── manifest-patterns.md
│   └── migration-contract.md
├── scripts/
└── evals/
```

`references/best-practices.md` является канонической runtime-справкой. Центральный `skill-best-practices` может индексировать и обновлять источники, но установленный навык не зависит от соседних каталогов.

## Ограничения

- Форматы harnesses меняются; перед релизом требуется повторная проверка официальной документации.
- Portable validator проверяет только кроссплатформенные инварианты.
- Реальная installability подтверждается только загрузкой representative skill в целевом harness.
- Навык не принимает за пользователя решения о public/private visibility, лицензии, owners и release channel.

## Быстрые примеры

```text
Проведи read-only аудит ./skills-repo и найди коллизии skill.sh/Claude Code.
```

```text
Спроектируй marketplace с metaskills и development, один canonical source,
aggregate plugin для локального тестирования. Дай manifests на ревью.
```

```text
Составь пофазный план миграции ./legacy-skills, включая rollback и acceptance gates.
Не применяй изменения.
```

```text
Собери candidate plugin в новый staging-каталог и проверь drift.
Ничего не устанавливай и не публикуй.
```

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Design, inventory, scaffold, curate, build, document, validate, migrate, release, and audit repositories that distribute Agent Skills through skill.sh-compatible catalogs and plugin harnesses such as Claude Code.
- **Версия:** `1.4.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `marketplace`, `distribution`.

## Когда использовать

Marketplace topology, category design, marketplace.json or plugin.json generation, portable skills/ layouts, aggregate plugin builds, skill documentation and onboarding sets, catalog governance, version policy, compatibility checks, staged migrations, publishing plans, or repository-wide skill distribution.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/skill-marketplace-manager Проверь read-only репозиторий с 40 навыками: найди дубликаты имён, глубину категорий и manifest drift.
```

**Ожидаемый результат:** выбирается маршрут `основной маршрут навыка`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### route-inventory

- **Пример запроса:** “Проверь read-only репозиторий с 40 навыками: найди дубликаты имён, глубину категорий и manifest drift.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### route-architecture

- **Пример запроса:** “Предложи структуру каталога для skill.sh и Claude Code с выборочной установкой категорий.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### route-scaffold

- **Пример запроса:** “Создай локальный каркас нового marketplace с категориями metaskills и development, но не публикуй.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### route-curation

- **Пример запроса:** “Добавь эти три проверенных навыка в каталог, назначь одну категорию каждому и проверь коллизии.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### route-build

- **Пример запроса:** “Собери самодостаточный aggregate plugin в новый staging-каталог и сформируй hashes.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### route-documentation

- **Пример запроса:** “Документируй канонические навыки и создай onboarding от установки до первого проверенного результата.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### route-validation

- **Пример запроса:** “Проверь, обнаруживаются ли навыки через skills CLI и Claude plugin, ничего не исправляй.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### route-migration-plan

- **Пример запроса:** “Составь детальный план переноса outputs/* в marketplace с rollback. Пока не переноси.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.


## Ожидаемые результаты

- результат соответствует заявленному контракту и явно отделяет факты от предположений;
- изменённые артефакты перечислены, а выполненные проверки названы без выдуманных PASS-результатов;
- ограничения, остаточные риски, состояние отката и следующий шаг указаны явно.

## Как проходит выполнение

1. **Classify the request.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Establish the operating mode.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Run the common workflow.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Enforce architectural invariants.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Use deterministic helpers.** Выполняется соответствующий этап контракта из `SKILL.md`.
6. **Dispatch private documentation work.** Выполняется соответствующий этап контракта из `SKILL.md`.
7. **Apply route-specific rules.** Выполняется соответствующий этап контракта из `SKILL.md`.
8. **Coordinate with adjacent skills.** Выполняется соответствующий этап контракта из `SKILL.md`.
9. **Produce a completion report.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Authoring one skill.

Навык не должен расширять полученные полномочия, скрывать пропущенные проверки, выполнять необратимые или внешние действия без явного разрешения либо заявлять состояние host только по наличию файлов.

## Зависимости

Обязательные companion-навыки в каноническом dependency-графе не объявлены. Проверяйте доступность host-инструментов и ресурсов, на которые ссылается `SKILL.md`.

## Ресурсы пакета

- [`SKILL.md`](DONOR.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`private-skills/`](private-skills/) — внутренние навыки, доступные только владельцу.
- [`prompts/`](prompts/) — маршрутные и специализированные промпты.
- [`references/`](references/) — справочники, схемы и контракты.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/build_plugin_bundle.py`](scripts/build_plugin_bundle.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/check_evals.py`](scripts/check_evals.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/validate_marketplace.py`](scripts/validate_marketplace.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
