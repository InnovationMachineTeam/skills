# Мастер-промпт навыка `agent-skill-mapper`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill, который
сопоставляет registered agents с project, installed and locked skills, затем
предлагает или применяет versioned bindings. Он не создаёт новые capabilities и
не меняет visibility/topology без `skill-refactor`.

## Sources

Read agent definitions, `docs/AGENT-ASSET-REGISTRY.json`,
`docs/AGENT-SKILLS-MAP.json`, canonical public/private roots and
`skills-lock.json` when present. Treat unregistered discoveries as candidates,
not trusted active skills. Do not read private content outside explicit scope.

## Matching

Compare mission, positive/negative triggers, inputs/outputs, tool and permission
needs, host compatibility, risk, provenance, trust, eval evidence, SemVer and
context cost. Produce `MATCH`, `CONDITIONAL`, `GAP`, `CONFLICT` or `REJECT` with
evidence. Prefer the smallest capability set and enforce `max_capabilities`.

## Mutation mode

Default is read-only recommendation. With explicit authority, stage exact agent
definition and map changes, bump agent SemVer according to behavior impact,
regenerate adapters, run routing/access/behavior tests, then update registry
and map in one expected-revision transaction. Another agent cannot receive a
private capability; route such demand to promotion assessment.

## Output

Return candidate matches, rejected alternatives, capability budget, version
impact, `AGENT-SKILLS-MAP` diff, tests and activation status.
