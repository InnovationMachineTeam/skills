# skill-architect

Мета-навык для проектирования, создания, обновления и проверки агентных навыков.

## Совместимость со встроенным навыком

- `$skill-architect` используется явно, для классификации архетипа, архитектурных решений, routed master prompts и handoff из созданной мета-системы.
- Встроенный `$skill-creator` остаётся маршрутом по умолчанию для обычного безымянного запроса «создай или обнови навык» без архитектурной специализации.
- Переименование не изменяет встроенный пакет и не подменяет его официальный валидатор.

## Как работает

1. Принимает идею, требования, примеры, существующий навык или другие исходные материалы.
2. Если вход отсутствует или существенно неоднозначен, задаёт короткие уточняющие вопросы.
3. Выбирает минимальную форму capability: inline, private command, private
   skill, public skill, tool/script или workflow.
4. Классифицирует основной архетип навыка и дополнительные свойства.
5. Загружает [общий промпт](prompts/base.md), один архетипный prompt и при
   необходимости профиль placement/registration.
6. Создаёт ресурсы, `SKILL.md`, UI-метаданные и candidate registry/map entries.
7. Проверяет структуру, discovery scope, scripts, triggers и поведение.

## Архетипы

- Knowledge/reference
- Workflow/procedure
- Tool integration
- Script-backed automation
- Artifact/template production
- Evaluation/review
- Orchestration/composition
- Meta/router

Подробные критерии приведены в [таксономии](references/taxonomy.md).

## Структура

```text
skill-architect/
├── SKILL.md
├── agents/openai.yaml
├── prompts/          # базовый, восемь архетипов и visibility profile
├── references/       # таксономия, visibility и правила проектирования
├── evals/            # проверки триггеров и поведения
└── scripts/          # переносимый структурный валидатор
```

## Проверка

```bash
python3 scripts/validate_skill.py . --fail-on warning
```

Файлы [routing.json](evals/routing.json) и [behavior.json](evals/behavior.json) содержат готовые проверочные сценарии, а не демонстрационные заглушки.

Пакет не устанавливает себя автоматически. Имя `skill-architect` отделяет этот мета-навык от встроенного `skill-creator`, который остаётся официальным контрактом и валидатором среды.

`private` в этом контракте означает agent-scoped discovery/binding, а не
конфиденциальность файлов. Все private skills остаются versioned, evaluated и
registered; runtime loader обязан исключать их из global discovery.
