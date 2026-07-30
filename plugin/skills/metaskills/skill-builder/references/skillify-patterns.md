# Adapted skillify patterns

The builder adopts lifecycle ideas observed in gbrain `skillify` while keeping the workflow portable and separating specialist roles.

Source provenance: `garrytan/gbrain`, `skills/skillify/SKILL.md` and its scaffold/check implementation, inspected at commit `b3b43d0f915e75ccf1479b28b2396fe02e8938e8`. The repository is MIT-licensed. The rules below are paraphrased architectural adaptations rather than copied host-specific instructions.

## Adopted

1. **Worth gate before scaffolding.** Repeated value, coherent triggers, and non-trivial reusable work must justify a skill.
2. **One capability and coherent trigger family.** Split unrelated intents before creating a mega-skill.
3. **Completeness audit.** Check contract, resources, deterministic code, tests, routing, coexistence, E2E, filing/lifecycle, and provenance.
4. **Deterministic scaffolding with unfinished sentinels.** Generated placeholders must remain visibly incomplete until replaced and tested.
5. **Quality review before tests lock behavior.** First establish that the intended result is worth preserving; then encode regression tests.
6. **Real user trigger phrases.** Routing fixtures must reflect natural requests and nearby negative cases.
7. **Resolver/catalog coexistence.** New skills must be reachable, non-orphaned, non-ambiguous, and free of accidental duplicate ownership.
8. **E2E verification.** Test trigger through observable artifact or side effect.
9. **Machine-readable audit.** Use structured state and evidence so automation does not parse prose.
10. **Idempotency and resumption.** Re-entry must not duplicate resolver rows, files, installs, migrations, or other consequential actions.

## Adapted rather than copied

- Cross-provider evaluation is a risk-based option, not a universal requirement. Record model identities, cost, disclosure, and failure semantics when used.
- Official host validators and our routing/behavior evals replace gbrain-only `check-resolvable` commands when running elsewhere.
- Portable frontmatter uses `name` and `description`; host-specific triggers, tools, versions, dependencies, and policies belong in adapters or manifests.
- `skill-scout`, `skill-harvester`, `skill-architect`, `skill-evaluator`, `skill-doctor`, `skill-optimizer`, `skill-refactor`, and `skill-manager` remain distinct specialists instead of one monolithic implementation.

## Rejected as universal rules

- A fixed line-count or recurrence threshold as proof that a skill is worthwhile.
- A single checklist score as proof of behavioral quality.
- Mandatory live integration tests when they would create unauthorized external side effects.
- Hard-coded provider or model names.
- Automatic retrieval of private memory from recent days.
- Execution of repository scripts during intake.
- Tests that merely lock in an unreviewed scaffold.

## Gate ordering

```text
worth → boundary → source/context → create or change → freeze evaluation contract
→ independent regression/holdout → routing coexistence → E2E → lifecycle verification
```

Order may skip inapplicable gates, but it must not invert a dependency. For example, do not install before supply-chain review, optimize before health recovery, or retire an old version before consumers and rollback are verified.
