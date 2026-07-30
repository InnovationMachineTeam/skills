# Документация как операционная система проекта

## Зачем проекту `docs/`

Для агентной разработки `docs/` — не витрина после релиза, а разделяемая
долговременная память людей и агентов. Она отвечает на четыре вопроса:

1. Зачем существует система и какой outcome нужен?
2. Что система обязана делать и не делать?
3. Как она устроена и почему выбраны эти решения?
4. Как её построить, проверить, выпустить и эксплуатировать?

Код остаётся источником истины для текущей реализации, спецификация — для
ожидаемого поведения, decision records — для rationale, runbooks — для
операционных процедур. Нельзя объявлять один документ источником истины для
всех видов знания.

## Рекомендуемая структура

```text
docs/
├── README.md                  # карта документации и правила использования
├── product/                   # vision, outcomes, users, roadmap, bets
├── discovery/                 # research, interviews, hypotheses, experiments
├── requirements/              # functional, quality, constraints, traceability
├── architecture/              # context, containers, interfaces, data, risks
│   └── decisions/             # ADR/MADR
├── design/                    # UX, interaction, visual and service design
├── delivery/                  # plans, releases, migrations, change records
├── operations/                # runbooks, SLO, alerts, incidents, continuity
├── security/                  # threat models, data classification, controls
├── quality/                   # test strategy, evals, quality gates
├── agents/                    # agent catalog, workflows, policies, runbooks
├── reference/                 # APIs, schemas, glossary, commands
├── tutorials/                 # learning-oriented paths
├── how-to/                    # task-oriented guides
├── explanation/               # concepts and rationale
└── generated/                 # reproducible projections; do not edit manually
```

Это расширяет Diátaxis — tutorials, how-to, reference и explanation —
документами жизненного цикла продукта и агентной системы
([Diátaxis](https://diataxis.fr/)). Не создавайте пустые папки заранее: дерево
расширяется по фактическим потребностям.

## Классы документов

Каждый файл должен быть одним из классов:

| Класс | Примеры | Правило |
|---|---|---|
| Canonical | PRD, spec, API contract, policy | Единственный активный владелец истины данного типа |
| Decision | ADR, governance decision | Append-mostly; supersede, не переписывать историю |
| Operational | Runbook, rollback, incident plan | Проверять упражнениями и production signals |
| Guidance | How-to, tutorial, explanation | Оптимизировать под задачу читателя |
| Evidence | Test report, research, eval | Immutable snapshot с provenance |
| Projection | Индекс, dashboard, generated API docs | Пересоздавать из canonical sources |
| Ephemeral | Черновик, scratch analysis | TTL или явное архивирование |

## Метаданные документа

Canonical и operational документы SHOULD иметь frontmatter:

```yaml
---
id: arch-checkout
title: Checkout architecture
status: active
owner: checkout-team
reviewers: [security, platform]
version: 2.1.0
last_reviewed: 2026-07-30
review_interval: 90d
source_of_truth_for: [checkout-boundaries, checkout-data-flow]
depends_on: [prd-checkout, adr-0042]
supersedes: arch-checkout@2.0.0
sensitivity: internal
agent_access: read
---
```

Для небольшого проекта достаточно owner, status, last_reviewed и links. Не
добавляйте метаданные, которые никто не проверяет.

## Как агенты работают с документацией

### Перед задачей

1. Найти ближайшие `AGENTS.md`/runtime instructions.
2. Прочитать `docs/README.md` и релевантный domain index.
3. Определить canonical sources и проверить freshness.
4. Загрузить только необходимые документы.
5. Сообщить о конфликте документа с кодом, не выбирать молча.

### Во время задачи

- ссылаться на IDs и anchors, а не копировать длинные фрагменты;
- фиксировать решения в ADR, а не только в conversation;
- обновлять spec вместе с изменением намеренного поведения;
- вести evidence и traceability;
- не редактировать generated файлы напрямую;
- соблюдать document ownership и write-set.

### После задачи

- обновить документы, затронутые поведением или операцией;
- запустить docs checks;
- отметить superseded/archived материалы;
- сохранить evidence и release/change note;
- проверить ссылки и отсутствие stale statements;
- не объявлять завершение, если required documentation gate не пройден.

## Документация и код

Используйте двустороннюю проверку:

- **docs → code**: требования, interfaces и ADR подтверждены реализацией;
- **code → docs**: публичные интерфейсы, deployment и runbooks отражают текущий
  код.

GSD применяет doc verifier против live codebase; OpenSpec рекомендует review
proposal/spec до кода и coherence verification после реализации; gstack
генерирует Diátaxis-документы из shipped behavior. Общая практика: генерация
помогает, но независимая фактическая проверка обязательна.

## Иерархические инструкции

`AGENTS.md`, `CLAUDE.md` и Cursor rules — не замена `docs/`. Это компактный
операционный index:

- карта репозитория;
- команды build/test/verify;
- критические ограничения;
- definition of done;
- ссылки на подробные документы.

Инструкции SHOULD быть короткими и располагаться ближе к области действия.
Codex загружает цепочку от глобального файла до текущей директории, причём
ближайшие правила переопределяют общие
([AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)).
Не копируйте в каждый файл одну и ту же политику: держите каноническую версию и
ссылки.

## Диаграммы

Для архитектуры используйте минимально полезные уровни C4: system context и
containers обычно достаточны; component и code — только где добавляют ценность
([C4](https://c4model.com/diagrams)). Каждая диаграмма должна иметь:

- цель и аудиторию;
- scope и уровень абстракции;
- легенду;
- подписанные отношения;
- дату/версию;
- link на source DSL;
- owner.

Не смешивайте разные уровни в одной «карте из коробок».

## Архитектурные решения

ADR фиксирует один значимый выбор: context, decision drivers, рассмотренные
варианты, outcome, последствия и способ подтверждения. Используйте status
`proposed/accepted/rejected/superseded/deprecated`. MADR даёт компактный
Markdown-формат ([MADR](https://adr.github.io/madr/)).

Агент MAY предложить ADR, но accountable human или policy owner принимает
high-impact решение.

## Docs quality gates

- ссылки и anchors валидны;
- обязательные metadata присутствуют;
- нет необъяснённых TODO/placeholders;
- code snippets исполняются или проверяются;
- public API reference совпадает со schema;
- владелец и freshness определены;
- requirements имеют verification;
- диаграммы рендерятся;
- glossary terms используются согласованно;
- sensitive data отсутствуют;
- generated outputs воспроизводимы.

## Антипаттерны

- свалка `docs/misc/` без index и owner;
- дублирование одного требования в PRD, spec и plan без traceability;
- огромный `AGENTS.md`, который пытается заменить всю документацию;
- автогенерация текста без fact verification;
- хранение живого state только в conversation;
- удаление старого решения вместо `superseded`;
- runbook, который никогда не выполнялся;
- документирование внутренних деталей в behavioral spec;
- обновление docs отдельной поздней фазой после релиза.
