# Migration contract

Read this file before producing or applying a marketplace migration.

## Required plan sections

1. Status, scope, non-goals, assumptions, and decision deadline.
2. Current inventory with hashes and ownership.
3. Exact source-to-target mapping.
4. Canonical-source and generated-artifact decisions.
5. Category, name, namespace, and collision policy.
6. Manifest and version strategy.
7. Phases with entry criteria, actions, artifacts, exit criteria, and rollback.
8. Static, discovery, behavior, upgrade, and security acceptance gates.
9. Pilot cohort and observability.
10. Cutover, support window, and retirement approval.
11. Open decisions for review.

## Default safety constraints

- Start in plan mode.
- Copy to a new staging tree; do not move or delete the source.
- Preserve unrelated and uncommitted work.
- Do not rewrite history or published tags.
- Do not publish or globally install without explicit authorization.
- Do not remove the previous distribution until the support window ends and the user approves retirement.

## Required rollback record

For every mutating phase record:

- rollback trigger;
- previous known-good artifact or revision;
- exact recovery action;
- data or state that cannot be recovered;
- responsible owner;
- maximum tolerated recovery time.

If any element is missing, keep the phase blocked from apply mode.

## Migration report states

- `DRAFT`: architecture and plan are awaiting review.
- `APPROVED`: decisions are accepted but no mutation is implied.
- `STAGED`: candidate tree exists; old source remains canonical.
- `PILOT`: selected consumers use the candidate.
- `CUTOVER`: candidate is canonical; rollback remains available.
- `RETIRED`: old tree was removed or archived through separate approval.

Never conflate `APPROVED` with permission to publish or retire.
