# Companion skill dependencies

<!-- generated from catalog/dependencies.json; do not edit -->

Claude Code supports native same-marketplace plugin dependencies. Codex and Cursor do not share that manifest contract, so they use generated warnings and an explicit install plan. Companions remain separate plugins so their identities do not collide.

## Required for full route coverage

| Skill | Minimum | Why |
|---|---:|---|
| `agent-model-selector` | `1.0.0` | The design route delegates current model selection and evidence. |
| `agent-skill-mapper` | `1.0.0` | The map-capabilities route delegates governed agent-skill bindings. |
| `agent-team-architect` | `1.0.0` | The design route delegates team architecture. |
| `agent-team-builder` | `1.0.0` | The build route delegates staged team materialization. |
| `agent-team-orchestrator` | `1.0.0` | The operate route delegates runtime task orchestration. |

## Recommended

| Skill | Minimum | Why |
|---|---:|---|
| `agent-workspace-manager` | `1.0.0` | Recommended when an operation needs isolated worktrees or workspace lifecycle management. |

## Runtime rule

Before dispatching a route, compare its owning companion with the skills available in the current session. If a required companion is missing or older than the minimum, emit a visible `DEPENDENCY WARNING`, name the blocked route, and do not imitate that specialist. Other routes may continue when their companions are available. Missing recommended skills are informational unless the chosen workflow needs them. If installed state cannot be inspected, say that dependency status is unverified.

## Codex installation

From the marketplace repository, preview or execute the complete plan:

```bash
python3 scripts/manage_skill_dependencies.py plan agent-team-manager --host codex
python3 scripts/manage_skill_dependencies.py install agent-team-manager --host codex --execute
```

Manual equivalent:

```bash
codex plugin add agent-model-selector@im-skills
codex plugin add agent-skill-mapper@im-skills
codex plugin add agent-team-architect@im-skills
codex plugin add agent-team-builder@im-skills
codex plugin add agent-team-orchestrator@im-skills
codex plugin add agent-team-manager@im-skills
```

For Claude Code, install only the requested plugin; its generated `dependencies` array auto-installs required companions from the same marketplace.
