# skill-marketplace-manager

`skill-marketplace-manager` — мета-навык для проектирования, сборки, проверки, миграции и выпуска репозиториев навыков. Он ориентирован на переносимый Agent Skills layout, skill.sh и plugin harnesses, прежде всего Claude Code.

> Текущий статус: `1.3.0`. Навык создан как reviewable package. Он не выполняет публикацию, глобальную установку, удаление прежней структуры или миграционный cutover без явного разрешения.

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
