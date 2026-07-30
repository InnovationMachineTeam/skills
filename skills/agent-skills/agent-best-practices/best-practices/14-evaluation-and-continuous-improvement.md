# Оценка и непрерывное улучшение

## Оценивайте систему, а не красноречие

Главная метрика — доля задач, где требуемый outcome доказан при допустимых
риске, стоимости и времени. Отдельно оцениваются:

1. отдельный агент;
2. tool use;
3. routing/delegation;
4. handoff;
5. workflow/team end-to-end;
6. policy и approvals;
7. recovery;
8. production impact.

## Eval pyramid

```text
production outcomes and incidents
end-to-end workflow scenarios
multi-agent coordination and recovery
single-agent task evals
tool/schema/policy unit tests
static validation
```

Нижние уровни быстрые и детерминированные; верхние реалистичнее, но дороже.

## Dataset

Corpus SHOULD включать:

- representative happy paths;
- ambiguous requests;
- boundary/edge/error/recovery;
- adversarial и prompt injection;
- permission denials;
- stale/conflicting context;
- missing agent/tool;
- timeout/cancel/retry;
- parallel conflicts и duplicated work;
- long-running resume;
- platform-specific cases;
- реальные production failures.

Разделяйте train/development и held-out regression set. Не подгоняйте prompt по
held-out cases.

## Rubric

Пример dimension set:

| Dimension | Что измеряется |
|---|---|
| Goal achievement | Достигнут ли observable outcome |
| Correctness | Факты, расчёты, code behavior |
| Completeness | Покрытие обязательных требований |
| Grounding | Claims подтверждены источниками/evidence |
| Scope discipline | Нет лишних действий |
| Tool correctness | Выбор, аргументы, порядок, side effects |
| Delegation quality | Правильные задачи и контекст |
| Handoff quality | Полнота статуса и продолжения |
| Safety | Policy, privacy, approvals, injection resistance |
| Recovery | Ошибки, retries, cancel/resume |
| Efficiency | Cost/latency/tool calls при успехе |
| Operability | Trace, artifacts, diagnosability |

Для каждого score задайте behavioral anchors, а не только 1–5.

## Graders

Используйте комбинацию:

- deterministic assertions;
- schema validators;
- test execution;
- source/code comparison;
- policy simulator;
- LLM judge с rubric;
- pairwise comparison;
- human/domain expert review.

LLM judge не должен быть единственным судьёй для security, money, compliance и
необратимых side effects. Проверяйте judge calibration и inter-rater agreement.

## Проверка оркестрации

Тестируйте не только финальный ответ:

- router выбрал правильный path;
- ненужный агент не был запущен;
- context pack минимален и достаточен;
- child permissions не расширились;
- DAG и waves корректны;
- no duplicate write ownership;
- aggregator сохранил dissent/evidence;
- budget и max depth соблюдены;
- failure не был замаскирован общим успехом;
- cancel/retry/resume идемпотентны.

## Team evals

Сравнивайте team с single-agent baseline:

- quality lift;
- latency и cost multiplier;
- coordination overhead;
- conflict/duplicate rate;
- critical-path speedup;
- diversity/independence specialists;
- synthesis loss;
- operator intervention.

Если team не даёт измеримого выигрыша, вернитесь к более простой архитектуре.

## Trigger/routing evals

Набор positive, negative и near-miss prompts измеряет precision/recall. Особенно
важны:

- запросы, где agent MUST сработать;
- похожие запросы, где срабатывать не должен;
- конфликт нескольких agents;
- недостаточный context;
- explicit override пользователя;
- multilingual/paraphrase cases.

## Security evals

- direct/indirect prompt injection;
- exfiltration через tool arguments/output;
- privilege escalation и confused deputy;
- malicious memory/doc/tool/agent card;
- approval replay или digest mismatch;
- unsafe handoff;
- network allowlist bypass;
- unsafe code execution;
- audit tampering;
- resource exhaustion;
- emergency revoke.

Связывайте их с OWASP Agentic Top 10 и локальным threat model.

## Efficiency optimization

OpenAI рекомендует сначала установить quality baseline на сильной модели, затем
заменять её более дешёвой там, где eval target сохраняется
([guide](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)).

Оптимизируйте по порядку:

1. устранить ненужные calls/tools/agents;
2. улучшить routing и context retrieval;
3. уменьшить variable outputs;
4. кэшировать стабильный context;
5. подобрать модель по узлу DAG;
6. параллелить только critical path;
7. сокращать retries через descriptive errors.

## Release gate агента

Перед новой версией:

- static/schema checks pass;
- unit/tool/policy tests pass;
- held-out eval не регрессировал сверх budget;
- critical safety cases pass;
- cost/latency в envelope;
- docs/contract/changelog обновлены;
- compatibility и migration проверены;
- canary cohort и rollback определены;
- owner/approver подписали evidence bundle.

## Production learning loop

```text
trace/feedback/incident
  → classify failure
  → reproduce as eval
  → root cause: prompt/tool/context/model/policy/orchestration
  → minimal change
  → regression suite
  → canary
  → monitor
```

Не изменяйте prompt вслепую по единичному примеру. Сначала классифицируйте слой
причины; часто проблема в tool contract, stale docs или permissions.

## Eval report

```markdown
# Agent evaluation report

## Versions and environment
## Dataset and exclusions
## Baseline
## Results by dimension and risk class
## Failure clusters
## Cost and latency
## Security findings
## Regressions
## Human review disagreements
## Decision and rollout
## Follow-up owners
```

Results без версии prompt/model/tools/policy и dataset digest невоспроизводимы.
