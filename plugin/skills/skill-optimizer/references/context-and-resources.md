# Context and Resource Optimization

## Contents

- Placement
- Progressive disclosure
- Reduction method
- Resource integrity

## Placement

| Information | Preferred location |
|---|---|
| Discovery and trigger contract | frontmatter description |
| Core procedure and routing | `SKILL.md` |
| Conditional or domain detail | `references/` |
| Repeated deterministic operation | `scripts/` |
| Output ingredient | `assets/` |
| Tests and trigger cases | `evals/` |
| Host UI or dependency metadata | `agents/` |
| Routed reusable prompts | `prompts/` |
| Current fact or controlled action | tool/API/MCP |
| Hard restriction | permission, schema, hook, sandbox, policy |

## Progressive disclosure

Keep metadata concise, `SKILL.md` under 500 lines, and resources one explicit routing step away. Link every necessary resource from the core workflow with a condition explaining when to load or execute it.

Avoid resource chains where one reference is discoverable only through another. Give long references a contents list and large corpora search guidance.

## Reduction method

1. Remove initializer scaffolding and stale notes.
2. Deduplicate equivalent rules.
3. Replace long explanations with short criteria or examples.
4. Move conditional detail out of the core body.
5. Replace repeated fragile instructions with tested scripts.
6. Retrieve dynamic facts instead of embedding them.
7. Remove information the agent handles reliably only after regression evidence.

Measure actual loaded context, not bundle size alone. Moving text to a reference saves context only if routing avoids loading it unnecessarily.

## Resource integrity

Do not remove a resource because it appears unused until links, scripts, tests, and host metadata have been searched. Preserve attribution, licenses, schemas, formats, and binary assets. Verify every moved link and script path.

