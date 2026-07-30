# Coordination and Downstream Handoffs

## Handoff contract

Pass exact candidate IDs, source locators, evidence, confidence, maturity, rights, assumptions, risks, intended destination, allowed files, preserved invariants, required validation, and forbidden side effects.

## Route by downstream outcome

- New skill or substantial redesign: `skill-architect`.
- Broken, unsafe, or inconsistent source skill: `skill-doctor`.
- Healthy skill needing measurable improvement: `skill-optimizer`.
- Installation, activation, version policy, conflict, or retirement: `skill-manager`.
- Opportunity discovery and build/no-build prioritization: `skill-scout`.
- Composition, merge, split, extraction, or compatibility topology: `skill-refactor`.
- Multi-stage research-to-skill, external adoption, or compare-refactor-migrate workflow: `skill-builder`.

Harvesting may recommend a route but does not authorize its mutations.

## Avoid recursive ambiguity

Do not ask a downstream meta-skill to "use everything." Provide a bounded candidate set and an acceptance contract. Avoid overlapping write ownership when multiple specialists work in parallel.

## Return evidence

Require downstream results to map changes and decisions back to candidate IDs. Rejected or deferred candidates should return reasons so the harvest remains auditable.
