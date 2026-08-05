# Requirements and Quality Attributes

## Not just "functional and non-functional"

It is more practical to separate:

- **functional requirements** — observable behavior and business rules;
- **quality requirements** — how well the system behaves under conditions;
- **constraints** — external limitations on the solution or process;
- **interface/data requirements** — contracts, formats, semantics;
- **transition requirements** — migration, rollout, coexistence, rollback;
- **agent requirements** — autonomy, permissions, observability, escalation.

ISO/IEC 25010:2023 provides a model of nine quality characteristics for the
specification and evaluation of ICT/software products
([ISO](https://www.iso.org/standard/78176.html)). Do not copy categories into a
document mechanically; choose those that matter in context.

## Formula for a good requirement

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

Example:

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

"The system should be fast and reliable" is not a requirement.

## Quality for software and agent systems

Check the relevance of the following groups:

- functional suitability;
- performance efficiency;
- compatibility/interoperability;
- interaction capability/usability/accessibility;
- reliability/resilience/recoverability;
- security/privacy;
- maintainability/modifiability/testability;
- flexibility/adaptability;
- safety;
- for agents: groundedness, task success, tool accuracy, controllability,
  autonomy calibration, handoff quality, traceability, and cost/latency.

## Agent requirements

Extend business requirements:

```markdown
### AR-007 — Approval before external publication

The publishing agent MUST NOT make a public repository visible until an
accountable reviewer approves the exact release digest.

- Trigger: proposed visibility change
- Risk: irreversible disclosure
- Enforcement: policy engine blocks tool call without approval token bound to digest
- Verification: negative policy test + audit event assertion
```

It is important to specify enforcement rather than relying on a prompt
instruction.

## Requirements for errors and edges

For each capability, ask:

- invalid/empty/oversized input;
- duplicate, replay, and out-of-order;
- timeout, cancellation, and partial failure;
- stale state and concurrent update;
- dependency degradation;
- permission denied;
- retry/compensation;
- idempotency;
- data retention/deletion;
- abuse/misuse and prompt injection;
- handoff failure and unavailable agent;
- budget exhaustion;
- human unavailable;
- observability failure.

OpenSpec recommends Given/When/Then for happy and edge cases and separates the
behavioral spec from the implementation plan
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

Each link has a type and status. Automatically search for:

- requirement without a source;
- requirement without verification;
- task without a requirement;
- test without a claim;
- ADR without a decision driver;
- release without a production signal;
- production failure without a regression eval.

Traceability is not needed for the sake of a matrix; it is needed for impact
analysis and outcome proof.

## Priority

Priority accounts for user/business value, risk reduction, dependency,
uncertainty learning, and cost of delay. MUST separately mark mandatory
regulatory/security constraints: they must not lose to feature ranking.

For user stories, the independently testable vertical slice principle from Spec
Kit is useful. For discovery, a bet with a resolution signal from ADLC. For
high assurance, risk-based levels and traceability, as in BMAD Test Architect.

## Review checklist

- one requirement, one verifiable statement;
- observable subject and response;
- RFC 2119 keyword chosen intentionally;
- conditions and boundaries defined;
- quality target measurable;
- no hidden implementation in the behavioral requirement;
- positive, negative, and recovery scenarios;
- assumptions and non-goals explicit;
- conflicting sources resolved or marked;
- source, owner, and verification linked;
- human judgment marked where automation is insufficient.
