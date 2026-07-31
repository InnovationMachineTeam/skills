# Лучшие практики проектирования маркетплейса навыков

Статус: каноническая операционная справка `skill-marketplace-manager`  
Последняя проверка источников: 30 июля 2026 года

## Содержание

1. [Главные решения](#главные-решения)
2. [Каноническая структура](#каноническая-структура)
3. [Категории и именование](#категории-и-именование)
4. [Совместимость со skill.sh](#совместимость-со-skillsh)
5. [Claude Code: плагин и маркетплейс](#claude-code-плагин-и-маркетплейс)
6. [Версии и релизы](#версии-и-релизы)
7. [Сборка и переносимость](#сборка-и-переносимость)
8. [Валидация и тестирование](#валидация-и-тестирование)
9. [Безопасность и корпоративное управление](#безопасность-и-корпоративное-управление)
10. [Миграция](#миграция)
11. [Документация и сопровождение](#документация-и-сопровождение)
12. [Разрешение противоречий](#разрешение-противоречий)
13. [Источники](#источники)

## Главные решения

1. Хранить навыки в одном каноническом дереве `skills/`.
2. Допускать не более одного уровня категории: `skills/<category>/<skill>/SKILL.md`.
3. Генерировать harness-specific артефакты, а не поддерживать несколько ручных копий.
4. Использовать отдельный marketplace manifest и отдельный самодостаточный aggregate plugin.
5. Считать категории организацией каталога, но не пространством имён навыков.
6. Разделять версию навыка, версию плагина и версию каталога.
7. Пропускать релиз только после статической, интеграционной и поведенческой проверки.
8. Выполнять миграцию через staging, пилот, обратимый cutover и явное подтверждение удаления старой структуры.

## Каноническая структура

Рекомендуемая форма репозитория:

```text
skill-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── skills/                         # единственный source of truth
│   ├── metaskills/
│   │   └── skill-architect/
│   │       ├── SKILL.md
│   │       └── ...
│   ├── agent-workflows/
│   ├── product/
│   ├── development/
│   └── marketing/
├── plugin/                         # генерируемый aggregate plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   └── build-manifest.json
├── scripts/
├── tests/
└── README.md
```

Почему так:

- `skills/` соответствует модели Agent Skills и обнаруживается skill.sh.
- `.claude-plugin/marketplace.json` описывает устанавливаемые предложения каталога.
- `plugin/` позволяет проверить весь набор локально через `claude --plugin-dir ./plugin`.
- генерируемая копия защищает от зависимостей за пределами кэша плагина.

Не хранить две равноправные ручные копии одного навыка. Если потребитель требует другой layout, создать детерминированную сборку и проверять отсутствие drift по хешам.

## Категории и именование

Использовать категории только для устойчивых доменов и ownership-политик. В
текущем портфеле используются `agent-os-skills`, `agent-team-skills`,
`agent-skills`, `metaskills` и `prompt-skills`; вторичную классификацию хранить в
`tags`. Будущие категории добавлять только по мере появления устойчивого
содержимого и владельца.

Хорошие примеры:

- `metaskills`
- `agent-workflows`
- `product`
- `development`
- `marketing`

Не использовать `agents` для навыков, если тот же репозиторий содержит Claude Code plugins: `agents/` уже означает каталог custom subagents. Категория `agent-workflows` снимает неоднозначность.

Правила:

- имя навыка — lowercase kebab-case, совпадает с именем каталога;
- имя уникально во всём aggregate plugin;
- категория — одна основная таксономия;
- `tags` — вторичная фасетная классификация;
- пустые категории не создавать;
- перенос между категориями не должен менять `name`, если поведение и идентичность навыка прежние.

## Совместимость со skill.sh

CLI `skills` принимает GitHub/GitLab URL, `owner/repo`, прямой путь к навыку и локальный путь. Для совместимого каталога поддерживать:

```text
skills/<skill>/SKILL.md
skills/<category>/<skill>/SKILL.md
```

Не добавлять ещё один уровень вложенности. Проверять обнаружение до публикации:

```bash
npx skills add . --list
npx skills add owner/repo --list
npx skills add owner/repo --skill skill-architect --agent claude-code --agent codex
```

Не устанавливать один и тот же навык одновременно через skill.sh и Claude marketplace в одну область видимости. Это создаёт дубликаты, неочевидный приоритет версий и конфликт триггеров.

## Claude Code: плагин и маркетплейс

### Плагин

Корень плагина содержит `.claude-plugin/plugin.json`; компоненты располагаются рядом с `.claude-plugin`, а не внутри неё. Для категорий перечислить директории, непосредственно содержащие папки навыков:

```json
{
  "name": "skill-toolkit",
  "displayName": "Skill Toolkit",
  "version": "1.0.0",
  "description": "Portable skill engineering toolkit",
  "skills": [
    "./skills/metaskills",
    "./skills/agent-workflows"
  ]
}
```

Локальная проверка:

```bash
claude --plugin-dir ./plugin
```

Навыки плагина получают namespace от имени плагина. Не полагаться на namespace как на замену уникальности внутри одного aggregate plugin.

### Маркетплейс

Манифест хранить в `.claude-plugin/marketplace.json`. Для монорепозитория допустим shared-root pattern: marketplace entry указывает `source: "./"`, `strict: false` и явный `skills` path. Пример:

```json
{
  "name": "skill-toolkit-marketplace",
  "owner": { "name": "Skill Toolkit Maintainers" },
  "plugins": [
    {
      "name": "metaskills",
      "source": "./",
      "strict": false,
      "description": "Skills for creating and governing skills",
      "version": "1.0.0",
      "category": "metaskills",
      "tags": ["skills", "meta", "governance"],
      "skills": "./skills/metaskills"
    }
  ]
}
```

При `strict: false` marketplace entry сам определяет компоненты. Не дублировать конфликтующие component paths в root plugin manifest.

Проверять пользовательский путь:

```text
/plugin marketplace add owner/repository
/plugin install metaskills@skill-toolkit-marketplace
```

И CLI-эквивалент:

```bash
claude plugin marketplace add owner/repository
claude plugin install metaskills@skill-toolkit-marketplace
```

## Версии и релизы

Различать три независимых понятия:

| Версия | Где | Что меняется |
|---|---|---|
| Версия навыка | `SKILL.md → metadata.version` | Контракт и содержимое отдельного навыка |
| Версия плагина | `plugin.json → version` | Устанавливаемый aggregate bundle |
| Версия marketplace entry | `marketplace.json → plugins[].version` | Релиз предложения каталога |

Использовать SemVer как политику проекта. При явных версиях повышать их в каждом релизе; иначе потребитель может не увидеть обновление. Не задавать одну и ту же release version одновременно в `plugin.json` и marketplace entry без автоматической проверки равенства. У Claude Code приоритет разрешения версии зависит от manifest/entry/source revision, поэтому дублирование вручную создаёт риск расхождения.

Для изменения только одного навыка:

1. повысить `metadata.version` навыка;
2. пересобрать bundle;
3. повысить версию устанавливаемого предложения, которое содержит навык;
4. зафиксировать changelog/release notes на уровне репозитория;
5. проверить обновление из предыдущей опубликованной версии.

## Сборка и переносимость

Плагин, установленный из marketplace, кэшируется. Поэтому каждый bundle должен быть самодостаточным:

- копировать весь каталог навыка, включая `scripts/`, `references/`, `assets/`, `prompts/`, `evals/` и `agents/`;
- исключать только заранее объявленный non-runtime мусор: `.DS_Store`, `__pycache__`, `*.pyc`, `.git`;
- не оставлять `../` ссылки на исходный монорепозиторий;
- не использовать абсолютные локальные пути;
- отклонять symlink, если поведение целевого harness не проверено явно;
- создавать сборку в новом staging-каталоге;
- писать build manifest с SHA-256;
- сравнивать build manifest в CI для обнаружения drift;
- не редактировать generated bundle вручную.

## Валидация и тестирование

Минимальная матрица релиза:

| Слой | Проверка | Обязательный результат |
|---|---|---|
| Agent Skills | YAML, `name`, `description`, directory match, self-containment | PASS для каждого навыка |
| Каталог | уникальные имена, глубина категорий, ссылки, версии | PASS |
| Portable CLI | `npx skills add . --list` | все ожидаемые навыки обнаружены |
| Claude marketplace | `claude plugin validate .` | PASS |
| Claude plugin | `claude plugin validate ./plugin --strict` | PASS |
| Local load | `claude --plugin-dir ./plugin` | representative skill доступен |
| Routing | positive, negative, ambiguous, collision prompts | заданный threshold |
| Behavior | минимум один сценарий на критичный маршрут | PASS |
| Upgrade | previous → candidate | новая версия обнаружена |
| Security | secrets, traversal, executable provenance, unsafe install | PASS |

Portable helper этого навыка не заменяет harness-native validators. Если CLI недоступен, ставить `NOT RUN`, а не `PASS`.

В CI разделить быстрые проверки pull request и более дорогие release gates. Не публиковать при drift, collision, invalid manifest, broken link, failed smoke test или отсутствующем version bump.

## Безопасность и корпоративное управление

- считать сторонний навык исполняемым supply-chain артефактом;
- проверять provenance, лицензию, commit/tag и целостность;
- читать скрипты до выполнения и запускать с минимальными полномочиями;
- не хранить токены и credentials в манифестах, prompts, fixtures или логах;
- закреплять доверенные marketplace sources административной политикой;
- разделять author, reviewer и publisher для важных релизов;
- поддерживать allowlist/denylist и процедуру срочного отзыва;
- документировать телеметрию без содержимого пользовательских prompts и секретов;
- проводить пилот в изолированной области видимости;
- обеспечивать восстановление предыдущей версии.

Для private marketplace отдельно проверить authentication целевых пользователей и CI. Не считать доступ автора доказательством доступности для потребителя.

## Миграция

Порядок миграции:

1. Зафиксировать inventory и hashes исходной структуры.
2. Согласовать mapping `source → target`, категории и owners.
3. Скопировать навыки в staging; не перемещать источник.
4. Исправить только внутренние portability defects.
5. Создать marketplace manifest.
6. Собрать aggregate plugin из staging source.
7. Запустить полную матрицу проверок.
8. Провести пилотную установку.
9. Согласовать cutover.
10. Оставить старую структуру recoverable на установленный срок.
11. Удалить или архивировать её только отдельным подтверждённым действием.

Rollback должен быть описан до cutover и включать источник предыдущей версии, способ переустановки, критерии запуска и ответственного.

## Документация и сопровождение

README маркетплейса должен содержать:

- назначение и поддерживаемые harnesses;
- каталог предложений и категории;
- команды установки и удаления;
- локальную разработку;
- политику версий и совместимости;
- security/reporting policy;
- contribution и review gates;
- known limitations;
- ownership и release process.

Хранить этот файл внутри навыка как каноническую операционную справку. Центральный `skill-best-practices` может индексировать и отслеживать источники, но не должен становиться runtime-зависимостью установленного `skill-marketplace-manager`.

## Разрешение противоречий

### «Один плагин» против «плагин на категорию»

Использовать оба представления для разных задач: generated aggregate plugin — для локальной разработки и полного набора; marketplace entries по категориям — для выборочной установки. Канонический source при этом остаётся один.

### `plugin.json` против `strict: false`

Для self-contained plugin использовать `plugin.json`. Для shared-root marketplace entries с явными component paths использовать `strict: false`. Не заставлять один root manifest описывать несовместимые наборы компонентов нескольких entries.

### README внутри навыка

Общая экономия контекста рекомендует не добавлять вспомогательную документацию в каждый навык. Здесь README является явно запрошенным пользовательским интерфейсом сложного multi-mode инструмента. Runtime-инструкции остаются в `SKILL.md`, а README не требуется для выполнения маршрутов.

### Плоский каталог против категорий

Плоский layout проще, но категории полезны при большом портфеле. Ограничение в один уровень обеспечивает совместимость с skill.sh и предотвращает произвольную глубину таксономии.

## Источники

Первичные и официальные источники:

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills — Best practices](https://agentskills.io/skill-creation/best-practices)
- [Agent Skills — Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Agent Skills — Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)
- [Agent Skills — Using scripts](https://agentskills.io/skill-creation/using-scripts)
- [Agent Skills — Adding skills support](https://agentskills.io/client-implementation/adding-skills-support)
- [Claude Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Vercel Skills CLI / skill.sh](https://github.com/vercel-labs/skills)
- [Anthropic: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)

Анализируемые публичные реализации и паттерны:

- [garrytan/gstack](https://github.com/garrytan/gstack)
- [garrytan/gbrain](https://github.com/garrytan/gbrain)

Перед изменением формата манифеста или release workflow повторно проверить актуальные harness-specific документы: эти контракты могут изменяться независимо от Agent Skills specification.
