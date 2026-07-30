# Evaluation and completion

Match evidence to the claim being made.

| Claim | Minimum evidence |
|---|---|
| worthwhile opportunity | recurrence/leverage evidence, stable triggers, coverage check, maintenance and eval plan |
| context collected | source inventory, provenance, locators, rights, contradictions and explicit gaps |
| skill created | exact bundle plus official structural validation |
| routing works | positive, negative, ambiguous and neighboring-skill cases |
| behavior works | realistic task artifacts and assertions against observable outputs |
| script works | positive, boundary and failure execution without unsafe side effects |
| repaired | original failing case passes under comparable conditions plus regressions |
| improved | comparable baseline/post metric and no blocking regression |
| refactored | topology, consumers, old/new routing, facade and rollback verified |
| installed or active | target-host discovery and execution evidence |
| production-ready | all applicable gates plus documented residual risk and operational ownership |

## Evaluation order

Review intended quality before encoding it as regression behavior. Then use deterministic checks, official validators, routing evals, behavior evals, adversarial/failure cases, E2E, catalog coexistence, and host verification as applicable.

Use `skill-evaluator` to freeze the evaluation contract, create or audit evals, run independent evidence collection, and compare revisions. The specialist that creates or mutates a candidate may propose tests, but it must not alter the frozen acceptance gates or holdout after seeing candidate results. Confirmed defects return to doctor; healthy improvement hypotheses return to optimizer; boundary failures return to refactor. Each mutation creates a new candidate revision and a new run.

Independent forward tests should receive realistic inputs and the skill artifact, not the intended route or answer. Use multiple models or providers only when the risk and expected information justify cost and data disclosure.

Report per-layer `PASS`, `FAIL`, `INCONCLUSIVE`, `BLOCKED`, or `NOT_EVALUATED`. A blocking security, authority, consumer, or recovery failure cannot be offset by a better aggregate score. Manager may use an evaluator release recommendation when deciding activation, but only host read-back proves lifecycle state.

## Waivers

Record the skipped gate, reason, approving authority when needed, risk created, and whether the result is still usable. A waiver changes the completion claim: for example, missing host verification permits “reviewable bundle,” not “active.”

## False completion patterns

- scaffold exists;
- validator passes;
- structural score is high;
- tests only reproduce implementation details;
- specialist says “done” without artifacts;
- files appear in a skill directory;
- installation command returns success without read-back;
- evaluation uses leaked expected answers.

None of these alone proves the user outcome.
