# skill-refactor

`skill-refactor` оценивает и безопасно изменяет границы существующих навыков: оставляет их раздельными, соединяет через composition, физически объединяет, разделяет, извлекает references или subskills и создаёт временные compatibility facades.

## Решения

- `KEEP_SEPARATE`
- `COMPOSE`
- `MERGE`
- `SPLIT`
- `EXTRACT_REFERENCE`
- `EXTRACT_SUBSKILL`
- `CREATE_FACADE`
- `PROMOTE_PUBLIC`
- `DEMOTE_PRIVATE`

По умолчанию навык выполняет read-only assessment. Мутации требуют точного плана, разрешения, validation и rollback.

## Проверки

```bash
python3 scripts/analyze_boundaries.py SKILL_DIR [SKILL_DIR ...] --output boundaries-before.json
python3 scripts/validate_refactor_plan.py refactor-plan.json
python3 scripts/compare_boundaries.py boundaries-before.json boundaries-after.json
python3 scripts/check_evals.py evals
```

Структурная валидность и уменьшение числа файлов не доказывают корректность routing, поведения, consumers или host discovery.

Visibility migration учитывает registry/map, owner-agent version, consumers и
host discovery. `private` означает agent-scoped binding, а не секретность.
