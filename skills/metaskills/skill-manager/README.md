# skill-manager

`skill-manager` управляет жизненным циклом портфеля public и agent-private
навыков: инвентаризирует явно заданные корни и registry, выявляет конфликты,
планирует установку и обновление, управляет областью обнаружения, проверяет
цепочку поставки и безопасный вывод навыков из эксплуатации.

Навык по умолчанию работает в режиме **read-only**. Наличие папки не считается доказательством того, что навык установлен, активен, отключён или затенён: итоговое состояние нужно проверять в целевом клиенте.

## Границы ответственности

- `skill-manager` — портфель, состояние, конфликты, зависимости, установка, доступность и governance;
- `skill-architect` — создание нового навыка или существенная переработка;
- `skill-doctor` — диагностика неисправного, нестабильного или небезопасного навыка;
- `skill-optimizer` — измеримое улучшение уже здорового навыка.

## Маршруты

1. Inventory and discovery
2. Install and update
3. Enable, disable, and surface
4. Conflict resolution
5. Dependencies and supply chain
6. Governance and portfolio
7. Retirement and recovery
8. Dispatch and coordination

Для каждого маршрута есть компактный overlay в `prompts/`; общие требования находятся в `prompts/base.md`.

## Инвентаризация

```bash
python3 scripts/inventory_skills.py ROOT [ROOT ...] --format json --output inventory-before.json
```

Скрипт работает только с явно переданными корнями, не исполняет содержимое
навыков, вычисляет детерминированные хеши и отмечает предполагаемые конфликты по
порядку корней. Для canonical agent-private path он дополнительно выводит
`visibility`, `scope`, `discoverability` и owner agent. Сканирование `/` и
домашнего каталога отклоняется.

Private roots передаются отдельно и не должны входить в global discovery.
`private` — scope использования, а не гарантия секретности файлов.

Сравнение снимков:

```bash
python3 scripts/compare_inventories.py inventory-before.json inventory-after.json
```

## Проверки

```bash
python3 scripts/check_evals.py evals
```

Набор `evals/routing.json` проверяет триггеры и выбор маршрута. `evals/behavior.json` фиксирует безопасное поведение, доказательность утверждений о состоянии и границы полномочий.

## Структура

- `SKILL.md` — основной workflow;
- `agents/openai.yaml` — интерфейсные метаданные;
- `prompts/` — базовый и маршрутные мастер-промпты;
- `references/` — модель жизненного цикла, идентичность, конфликты, supply chain и governance;
- `scripts/` — read-only инвентаризация, сравнение снимков и проверка eval-наборов;
- `evals/` — маршрутизация и поведенческие сценарии.
