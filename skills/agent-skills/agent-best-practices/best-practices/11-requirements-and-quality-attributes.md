# Требования и атрибуты качества

## Не только «функциональные и нефункциональные»

Практичнее разделять:

- **functional requirements** — наблюдаемое поведение и бизнес-правила;
- **quality requirements** — насколько хорошо система ведёт себя в условиях;
- **constraints** — внешние ограничения решения или процесса;
- **interface/data requirements** — contracts, formats, semantics;
- **transition requirements** — migration, rollout, coexistence, rollback;
- **agent requirements** — autonomy, permissions, observability, escalation.

ISO/IEC 25010:2023 даёт модель из девяти характеристик качества для
спецификации и оценки ICT/software products
([ISO](https://www.iso.org/standard/78176.html)). Не переносите категории в
документ механически; выбирайте значимые для контекста.

## Формула хорошего требования

Functional requirement:

```text
WHEN <trigger> [AND <condition>]
THE SYSTEM MUST <observable response>
[WITHIN <boundary>]
```

Quality attribute scenario:

```text
Source → Stimulus → Environment → Artifact → Response → Measure
```

Пример:

```markdown
### QR-PERF-003 — Checkout confirmation latency

- Source: authenticated shopper
- Stimulus: submits a valid order
- Environment: normal load, 500 RPS, payment provider p95 ≤ 400 ms
- Artifact: checkout API
- Response: accepts or rejects order and returns stable order ID
- Measure: p95 ≤ 1.5 s, p99 ≤ 3 s over 15 minutes
- Verification: load-test/checkout-submit.js
```

«Система должна быть быстрой и надёжной» не является требованием.

## Качество software и agent system

Проверяйте релевантность следующих групп:

- functional suitability;
- performance efficiency;
- compatibility/interoperability;
- interaction capability/usability/accessibility;
- reliability/resilience/recoverability;
- security/privacy;
- maintainability/modifiability/testability;
- flexibility/adaptability;
- safety;
- для агентов: groundedness, task success, tool accuracy, controllability,
  autonomy calibration, handoff quality, traceability и cost/latency.

## Требования к агенту

Дополните бизнес-требования:

```markdown
### AR-007 — Approval before external publication

The publishing agent MUST NOT make a public repository visible until an
accountable reviewer approves the exact release digest.

- Trigger: proposed visibility change
- Risk: irreversible disclosure
- Enforcement: policy engine blocks tool call without approval token bound to digest
- Verification: negative policy test + audit event assertion
```

Важно указывать enforcement, а не полагаться на инструкцию в prompt.

## Требования к ошибкам и краям

Для каждой capability спросите:

- invalid/empty/oversized input;
- duplicate, replay и out-of-order;
- timeout, cancellation и partial failure;
- stale state и concurrent update;
- dependency degradation;
- permission denied;
- retry/compensation;
- idempotency;
- data retention/deletion;
- abuse/misuse и prompt injection;
- handoff failure и unavailable agent;
- budget exhaustion;
- human unavailable;
- observability failure.

OpenSpec рекомендует Given/When/Then для happy и edge cases и отделяет
behavioral spec от implementation plan
([Writing Good Specs](https://github.com/Fission-AI/OpenSpec/blob/main/docs/writing-specs.md)).

## Traceability

```text
signal/bet
  → stakeholder need
    → requirement
      → architecture decision
        → implementation task
          → test/eval/evidence
            → release
              → production signal
```

Каждая связь имеет type и status. Автоматически ищите:

- requirement без source;
- requirement без verification;
- task без requirement;
- test без claim;
- ADR без decision driver;
- release без production signal;
- production failure без regression eval.

Traceability нужна не ради матрицы, а для impact analysis и доказательства
outcome.

## Приоритет

Приоритет учитывает user/business value, risk reduction, dependency,
uncertainty learning и cost of delay. MUST отдельно отмечать обязательные
regulatory/security constraints: они не должны проигрывать feature ranking.

Для user stories полезен принцип independently testable vertical slice из Spec
Kit. Для discovery — bet с resolution signal из ADLC. Для high assurance —
risk-based levels и traceability, как в BMAD Test Architect.

## Review checklist

- одно требование — одно проверяемое утверждение;
- observable subject и response;
- RFC 2119 keyword выбран осознанно;
- условия и границы заданы;
- quality target измерим;
- нет скрытой реализации в behavioral requirement;
- positive, negative и recovery scenarios;
- assumptions и non-goals явны;
- конфликтующие источники разрешены или помечены;
- source, owner и verification связаны;
- human judgment отмечен там, где automation недостаточна.
