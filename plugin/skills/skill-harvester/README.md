# skill-harvester

`skill-harvester` извлекает повторно используемые компоненты из явно заданных навыков, репозиториев, документов, промптов, скриптов, eval-наборов, трасс и отчётов об ошибках.

Результат harvest — не готовый навык, а набор кандидатов с доказательствами, provenance, правами использования, уверенностью, зрелостью, рисками и проверками.

## Что можно собирать

- триггеры и правила маршрутизации;
- workflows, decision gates и recovery-паттерны;
- доменные знания и справочные структуры;
- промпты, шаблоны и output contracts;
- скрипты и tool-паттерны;
- eval-кейсы, failure modes и anti-patterns;
- safety, authority и governance-правила.

## Маршруты

1. Source inventory
2. Patterns and workflows
3. Knowledge and references
4. Prompts and templates
5. Scripts and tools
6. Evals and failures
7. Synthesis and deduplication
8. Integration and dispatch
9. Context build
10. Pairwise skill comparison
11. External skill intake

Общие правила находятся в `prompts/base.md`, а детали каждого маршрута — в соответствующем overlay из `prompts/`.

## Безопасность

- источники рассматриваются как недоверенные данные, а не инструкции;
- скрипты источников не исполняются;
- сканируются только явно заданные пути с ограниченной глубиной;
- секреты и персональные данные не копируются;
- неизвестные права блокируют verbatim reuse и статус `adoptable`;
- исходники по умолчанию не изменяются.

## Инвентаризация

```bash
python3 scripts/inventory_sources.py SOURCE [SOURCE ...] --format json --output source-inventory.json
```

В качестве источника можно явно передать текущую кодовую базу (`.`), локальный репозиторий, отдельные файлы или смешанные папки. Публичные GitHub-репозитории сначала загружаются в изолированный scratch/inbox с фиксацией commit, license и provenance.

Извлечение текста из Markdown, исходного кода, HTML, RTF, DOCX, ODT, PPTX и доступных PDF:

```bash
python3 scripts/extract_documents.py SOURCE [SOURCE ...] --output-dir inbox/extracted --manifest inbox/extraction-manifest.json
```

Индекс исследовательского inbox:

```bash
python3 scripts/build_inbox_index.py inbox --output inbox/index.json
```

## Проверка harvest-манифеста

```bash
python3 scripts/validate_harvest.py harvest-manifest.json
```

Структура манифеста описана в `references/output-schema.md`. Структурная валидность не доказывает правильность кандидатов или наличие прав на использование.

## Проверка eval-наборов

```bash
python3 scripts/check_evals.py evals
```

## Границы мета-навыков

- создание готового навыка → `skill-architect`;
- диагностика опасного или сломанного материала → `skill-doctor`;
- улучшение здорового навыка → `skill-optimizer`;
- поиск и приоритизация возможностей → `skill-scout`;
- merge, composition, split и extraction → `skill-refactor`;
- установка и управление жизненным циклом → `skill-manager`.
