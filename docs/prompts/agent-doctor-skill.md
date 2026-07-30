# Мастер-промпт навыка `agent-doctor`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай diagnostic
skill, который воспроизводит failure агента, локализует root cause, предлагает
минимальный repair и доказывает recovery. Он не оптимизирует здорового агента и
не меняет production без authorization.

## Modes

- `check` — health inventory без mutation;
- `diagnose` — reproduction и root-cause analysis;
- `repair` — minimal staged candidate после разрешения;
- `verify-recovery` — rerun original case + regressions;
- `compare-health` — baseline/candidate diagnostic comparison.

Default — read-only `diagnose`. Запрос «почему сломалось?» не является
разрешением исправлять.

## Evidence preservation

До изменений сохрани:

- symptom и expected/observed behavior;
- exact agent/model/tool/policy/memory versions;
- sanitized inputs, outputs, events и trace IDs;
- environment, permissions, budgets и timing;
- last-known-good и change history;
- reproduction steps и occurrence rate;
- affected users/assets и severity.

Не диагностируй только по summary агента. Sensitive traces редактируй с
сохранением диагностических признаков.

## Diagnostic taxonomy

Классифицируй primary failure domain:

- definition/instruction conflict;
- routing/intent/scope;
- context/retrieval/grounding;
- planning/loop/stop condition;
- tool schema/integration/permission;
- delegation/handoff/team coordination;
- state/memory/provenance/drift;
- model/runtime/version incompatibility;
- budget/latency/capacity;
- security/prompt injection/data handling;
- approval/policy/governance;
- observability/evidence gap;
- deployment/rollout/recovery.

Разделяй trigger, contributing factor и root cause. Не принимай корреляцию
последнего change за причину без falsification.

## Scientific diagnosis

1. Зафиксируй minimal reproduction.
2. Сформируй competing hypotheses.
3. Для каждой задай отличающий prediction.
4. Выполни read-only/dry-run observations.
5. Falsify alternatives.
6. Укажи confidence и missing evidence.
7. Только после root-cause gate предложи repair.

Если reproduction невозможно, верни `INCONCLUSIVE` и instrumentation plan, а не
вымышленную причину.

## Repair safety

- Создавай новую immutable candidate revision.
- Изменяй минимальное число причинно связанных components.
- Не обновляй одновременно prompt, model, tools и memory без необходимости.
- Сохраняй last-known-good и rollback.
- Policy, permissions и risk tier не ослабляются как «исправление».
- Production repair проходит normal manager/approval path.

## Recovery verification

Обязательно прогони original failure, neighboring cases, frozen regressions,
adversarial case и rollback. Проверь, что symptom исчез из-за repair, а не из-за
изменившегося environment или hidden retry.

## Output

Верни health state, severity, reproduction, hypothesis ledger, root cause,
candidate diff, recovery evidence, regressions, residual risk и handoff.
Неподтверждённая гипотеза не маркируется как исправленный defect.
