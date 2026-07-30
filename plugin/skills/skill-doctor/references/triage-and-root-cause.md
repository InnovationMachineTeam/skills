# Triage and Root Cause

## Contents

- Triage
- Reproduction
- Differential diagnosis
- Evidence standard

## Triage

First contain unsafe side effects, data exposure, repeated external actions, and destructive loops. Preserve logs and partial state. Do not destroy evidence by repeatedly retrying.

## Reproduction

- Use the smallest input that still fails.
- Match the reported host, model, tools, permissions, working directory, and environment.
- Prefer read-only, local, mock, sandbox, or dry-run reproduction.
- Record exact commands, inputs, outputs, exit codes, and side effects.
- Repeat only when nondeterminism or transience is part of the hypothesis.

## Differential diagnosis

List a small number of plausible causes and a discriminating check for each. Order checks by safety, information gain, reversibility, cost, and likelihood.

Use a cause table:

```text
Candidate cause:
Supporting evidence:
Contradicting evidence:
Discriminating check:
Result:
Status: confirmed/excluded/open
```

## Evidence standard

Confirm a root cause when it explains the symptom, the discriminating check supports it, and reasonable alternatives are excluded. A linter warning, recent change, or correlation alone is not root-cause proof.

If reproduction fails, report the diagnosis as unconfirmed and identify the missing environment or evidence.

