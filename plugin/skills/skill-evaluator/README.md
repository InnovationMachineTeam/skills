# skill-evaluator

`skill-evaluator` проектирует, пишет, запускает, проверяет и сравнивает eval-наборы для агентных навыков.

Trigger fixtures хранятся в `evals/routing.json`; отдельный `triggers`-формат не нужен. Контракты `evaluation-plan.json`, наборов и нормализованных run reports описаны в `references/artifact-contracts.md`.

## Маршруты

1. `evaluation-plan`
2. `routing-and-triggers`
3. `behavior-and-quality`
4. `script-and-tooling`
5. `security-and-authority`
6. `catalog-and-coexistence`
7. `run-evaluation`
8. `audit-evaluation`
9. `compare-evaluations`

Навык владеет доказательствами и verdict-ами, но не исправляет, не оптимизирует и не активирует оцениваемый пакет. Результаты передаются в `skill-doctor`, `skill-optimizer`, `skill-architect`, `skill-refactor`, `skill-builder` или `skill-manager`.

Основные проверки:

```bash
python3 scripts/validate_eval_plan.py evaluation-plan.json
python3 scripts/validate_eval_suite.py evals/
python3 scripts/score_routing.py routing-results.json
python3 scripts/compare_eval_runs.py baseline.json candidate.json
python3 scripts/check_evals.py evals/
python3 scripts/run_fixture_evals.py
```

Пакет не устанавливает себя автоматически.
