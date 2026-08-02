# Prompt-skill category consolidation

Status: `STAGED` repository candidate; no publication or host activation is
implied.

## Decision

The public `prompt-master@1.0.1` identity moves without a behavior change:

| Previous canonical locator | New canonical locator |
|---|---|
| `skills/prompts/prompt-master` | `skills/prompt-skills/prompt-master` |

`prompt-skills` is now the only top-level prompt category. It owns both the
bounded `prompt-optimize` route and the full-package `prompt-master` route. The
old category's reconstruction-safety rule is preserved in the surviving
category instructions.

## Acceptance gates

- all direct `skills/*` category directories contain a `README.md`;
- catalog and current agent registry resolve `prompt-master` to
  `skills/prompt-skills/prompt-master`;
- generated marketplace and plugin projections contain no `skills/prompts`
  canonical projection;
- routing, behavior, dependency, documentation, repository, and full unit
  validation pass;
- skill identity and version remain `prompt-master@1.0.1` because runtime
  behavior and installed skill contents are unchanged.

## Rollback

Before publication, restore the previous repository revision. After a released
cutover, restore the `prompts` category mapping, rebuild all generated
projections from staging, and republish a new repository release; do not edit
installed caches or generated packages by hand.
