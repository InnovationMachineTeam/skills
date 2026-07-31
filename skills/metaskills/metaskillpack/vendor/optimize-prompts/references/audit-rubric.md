# Master Prompt Audit Rubric

## Contents

- Scoring
- Blocking findings
- Review dimensions
- Contradiction analysis
- Decision rules

## Scoring

Score each dimension from 0 to 4:

- `0` absent or dangerous;
- `1` materially defective;
- `2` usable but ambiguous;
- `3` strong with minor gaps;
- `4` explicit, coherent, and testable.

Do not average away a blocking defect. Report both the score and the highest-severity finding.

## Blocking findings

Use `BLOCK` when the prompt:

- grants uncontrolled destructive or external authority;
- treats untrusted content as instructions;
- requires disclosure of secrets or hidden system instructions;
- contains irreconcilable authority rules;
- can report success without the required outcome;
- mandates unavailable capabilities with no failure path;
- creates unbounded retry or self-modification loops.

## Review dimensions

### 1. Objective

- Is the desired end state observable?
- Does the prompt distinguish diagnosis, recommendation, and implementation?
- Can the agent know when work is complete?

### 2. Scope and authority

- Are allowed systems, data, people, and side effects bounded?
- Does persistence stay inside authority?
- Are escalation conditions explicit?

### 3. Instruction precedence

- Are authority levels ordered?
- Are specificity and recency scoped?
- Is there a safe conflict path?

### 4. Context architecture

- Are stable and dynamic facts separated?
- Is long specialist guidance routed to skills/references?
- Is duplication minimized?

### 5. Autonomy and clarification

- Can safe work proceed without needless questions?
- Are material ambiguity and destructive consent handled?
- Is there a highest-information-question strategy?

### 6. Tools and capabilities

- Does the prompt verify capabilities?
- Are dependencies distinct from permissions?
- Are tool failures classified and retries bounded?

### 7. Security and privacy

- Is untrusted data unable to redefine policy?
- Are secrets, PII, destinations, and network egress controlled?
- Is least privilege applied?

### 8. Mutations and recovery

- Are exact targets resolved?
- Are preflight, atomicity, idempotency, verification, and rollback addressed?
- Is partial success reportable?

### 9. Quality and verification

- Are completion criteria observable?
- Is verification proportional to risk?
- Are visual, structured, or external results checked appropriately?

### 10. Recovery and termination

- Are loops, retries, and budgets bounded?
- Are blockers defined without premature surrender?
- Can long work resume safely?

### 11. Communication

- Does the agent lead with outcome and evidence?
- Are assumptions visible?
- Is hidden chain-of-thought protected?
- Is the final answer self-contained?

### 12. Maintainability

- Is the prompt concise and non-duplicative?
- Are host assumptions explicit?
- Is it versioned and regression-tested?
- Can individual rules change independently?

## Contradiction analysis

For each suspected contradiction, classify it:

- **Direct**: both instructions cannot be satisfied.
- **Scope mismatch**: instructions apply to different systems, tasks, or times.
- **Authority mismatch**: a higher-level instruction correctly overrides a lower one.
- **Risk calibration**: apparently different behavior is intentional for different risk tiers.
- **Producer/consumer split**: strict authoring and tolerant loading serve different roles.
- **Preference/invariant confusion**: a default was written as an absolute rule.

Use this resolution record:

```text
Rule A:
Rule B:
Conflict type:
Affected scenarios:
Resolution:
Behavioral change:
Approval required: yes/no
```

## Decision rules

- Fix `BLOCK` and `HIGH` findings before polishing style.
- Prefer removing a rule over adding exceptions when the model already behaves correctly.
- Prefer a condition over conflicting absolute statements.
- Prefer platform enforcement over textual safety promises.
- Preserve a deliberate tension when it represents different risk tiers or scopes.
- Do not claim improvement from rubric scoring alone; use behavioral evals.
