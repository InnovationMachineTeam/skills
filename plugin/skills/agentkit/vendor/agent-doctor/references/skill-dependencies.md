# Companion skill dependencies

<!-- generated from catalog/dependencies.json; do not edit -->

Claude Code supports native same-marketplace plugin dependencies. Codex and Cursor do not share that manifest contract, so they use generated warnings and an explicit install plan. Companions remain separate plugins so their identities do not collide.

## Required for full route coverage

None.

## Recommended

| Skill | Minimum | Why |
|---|---:|---|
| `agent-evaluator` | `1.0.0` | Provides frozen reproduction and independent recovery evidence. |

## Runtime rule

Before dispatching a route, compare its owning companion with the skills available in the current session. If a required companion is missing or older than the minimum, emit a visible `DEPENDENCY WARNING`, name the blocked route, and do not imitate that specialist. Other routes may continue when their companions are available. Missing recommended skills are informational unless the chosen workflow needs them. If installed state cannot be inspected, say that dependency status is unverified.

## Codex installation

From the marketplace repository, preview or execute the complete plan:

```bash
python3 scripts/manage_skill_dependencies.py plan agent-doctor --host codex
python3 scripts/manage_skill_dependencies.py install agent-doctor --host codex --execute
```

Manual equivalent:

```bash
codex plugin add agent-doctor@im-skills
```

For Claude Code, install only the requested plugin; its generated `dependencies` array auto-installs required companions from the same marketplace.
