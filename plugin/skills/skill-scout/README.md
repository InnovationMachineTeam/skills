# skill-scout

`skill-scout` находит потенциально полезные навыки в текущей сессии, явно переданных экспортированных сессиях, документах, репозиториях и истории задач. Он проверяет существующее покрытие и решает, нужно ли создавать новый навык, расширять существующий, использовать готовый навык, автоматизацию или оставить задачу ad hoc.

Навык не создаёт и не устанавливает другие навыки.

## Решения

- `CREATE_NEW`
- `EXTEND_EXISTING`
- `USE_EXISTING`
- `USE_AUTOMATION`
- `KEEP_AD_HOC`
- `RESEARCH`

## Основной результат

- ранжированный отчёт возможностей;
- `opportunities.json` с evidence, coverage, context plan, рисками и eval-планом;
- bounded handoff для `skill-harvester`, `skill-architect`, `skill-optimizer` или `skill-manager`.

## Проверки

```bash
python3 scripts/validate_opportunities.py opportunities.json
python3 scripts/rank_opportunities.py opportunities.json
python3 scripts/check_evals.py evals
```

Числовой рейтинг используется только для последовательной сортировки и не доказывает спрос, ROI, безопасность или разрешение на создание.
