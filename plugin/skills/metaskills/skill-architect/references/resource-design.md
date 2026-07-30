# Resource Design

## Contents

- Degree of freedom
- Resource selection
- Progressive disclosure
- Resource quality

## Degree of freedom

Match instruction precision to task fragility:

- **High freedom**: prose heuristics for contextual judgment with many valid approaches.
- **Medium freedom**: pseudocode, parameterized templates, or configurable scripts when a preferred pattern exists.
- **Low freedom**: narrow deterministic scripts for fragile, repetitive, or consistency-critical operations.

## Resource selection

| Need | Resource |
|---|---|
| Core routing and procedure | `SKILL.md` |
| Long, conditional, or domain knowledge | `references/` |
| Repeated or fragile deterministic operation | `scripts/` |
| File copied or transformed into the deliverable | `assets/` |
| UI discovery metadata | `agents/openai.yaml` |
| Live facts or external actions | tool/API/MCP, not frozen text |
| Hard security boundary | permission, schema, hook, sandbox, or policy |

Do not create a resource merely because its folder exists. Do not duplicate content between `SKILL.md` and references.

## Progressive disclosure

Use three levels:

1. `name` and `description` for discovery;
2. concise `SKILL.md` for the active procedure;
3. resources loaded only when their named condition applies.

Keep `SKILL.md` under 500 lines. Keep references one link away from it. Add a contents list to references longer than 100 lines. For very large sources, give search terms or section routing rather than requiring full reads.

## Resource quality

- Make scripts non-interactive by default, parameterized, and safe to rerun where practical.
- Send machine results to stdout, diagnostics to stderr, and failures through nonzero exit codes.
- Validate input paths, types, sizes, and exact mutation targets.
- Avoid hidden network calls, undeclared dependencies, and embedded secrets.
- Distinguish example files from normative templates.
- Prefer small representative examples to verbose explanations.
- Keep generated outputs outside the skill bundle unless they are reusable assets or fixtures.

