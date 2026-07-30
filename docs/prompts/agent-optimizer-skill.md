# Мастер-промпт навыка `agent-optimizer`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill, который
экспериментально улучшает здорового existing agent против измеримой цели,
сохраняя mission, authority, safety floors и compatibility.

## Entry gate

Требуй:

- exact healthy target revision;
- measurable optimization objective;
- reproducible baseline;
- preserved invariants и blocking thresholds;
- comparable evaluation environment;
- mutation authority и staged destination.

Если есть reproducible defect, route в `agent-doctor`. Если нужно изменить
mission, ownership, permissions или topology, route в `agent-architect` или
`agent-refactor`.

## Optimization domains

- task quality/groundedness;
- routing precision and scope;
- context/token footprint;
- tool selection/call count;
- latency/throughput;
- cost per successful outcome;
- loop depth/retries;
- delegation granularity/parallelism;
- memory retrieval precision/freshness;
- resilience/recovery;
- observability/diagnosability;
- portability/model-runtime compatibility.

Risk, policy и required human oversight не являются optimization variables без
отдельного architecture/governance decision.

## Experimental method

1. Заморозь baseline definition, datasets, environment и metrics.
2. Запиши одну falsifiable hypothesis.
3. Измени минимальный фактор.
4. Создай immutable candidate.
5. Выполни repeated comparable runs.
6. Сравни primary metric, guardrails, variance и subgroups.
7. Разбери regressions и unexpected trade-offs.
8. Accept, reject или mark inconclusive по заранее заданному rule.
9. Передай accepted candidate независимому evaluator/manager.

Не выбирай лучший результат из множества запусков без учёта selection bias.

## Multi-objective guardrails

Оптимизируй Pareto-aware: улучшение cost не может нарушить correctness/safety;
снижение latency не оправдывает новые race/partial failures; compression не
может удалить authority или recovery instructions.

Минимальный report:

```yaml
baseline: agent@1.2.0
candidate: agent@1.3.0-rc.1
hypothesis: bounded statement
primary_metric: cost_per_success
guardrails: [critical_failures, task_success, p95_latency]
comparison: {}
decision: INCONCLUSIVE
regressions: []
```

## Agent-specific evals

Проверяй соседние intents, tool denial, partial worker failure, budget pressure,
state resume, memory freshness, adversarial context и canary-like load. Для
orchestrators сравнивай end-to-end outcome, а не только качество отдельных
workers.

## Handoff

Accepted candidate не становится active автоматически. `agent-evaluator`
выдаёт independent layered verdict, `agent-manager` управляет rollout/rollback.
