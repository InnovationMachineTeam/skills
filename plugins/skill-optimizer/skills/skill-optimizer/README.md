# skill-optimizer

Мета-навык для измеряемой оптимизации существующих агентных навыков.

## Принцип работы

1. Получает существующий skill bundle и цель улучшения.
2. Фиксирует baseline до изменения файлов.
3. Классифицирует первичную причину проблемы.
4. Загружает [общий промпт](prompts/base.md) и один специализированный промпт.
5. Проверяет одну гипотезу минимальным изменением.
6. Сравнивает результаты в одинаковой среде и принимает, отклоняет или помечает изменение как недоказанное.

## Направления оптимизации

- routing и discovery;
- context и resource architecture;
- workflow и reliability;
- scripts и tool integration;
- safety и authority;
- evaluation и regression;
- portability и packaging;
- performance и context cost.

## Структура

```text
skill-optimizer/
├── SKILL.md
├── agents/openai.yaml
├── prompts/          # базовый и специализированные optimization-промпты
├── references/       # методика и критерии
├── evals/            # trigger-, routing- и behavioral-сценарии
└── scripts/          # анализ baseline и сравнение отчётов
```

## Статический анализ

```bash
python3 scripts/analyze_skill.py path/to/skill
python3 scripts/analyze_skill.py path/to/skill --format json --output before.json
```

После изменения:

```bash
python3 scripts/analyze_skill.py path/to/skill --format json --output after.json
python3 scripts/compare_reports.py before.json after.json
```

Структурные метрики не доказывают поведенческое улучшение. Используйте [routing.json](evals/routing.json) и [behavior.json](evals/behavior.json) вместе с функциональными тестами целевого навыка.

Проверка структуры и покрытия eval-наборов:

```bash
python3 scripts/check_evals.py evals
```

Пакет не изменяет и не устанавливает production-навыки без явного разрешения.
