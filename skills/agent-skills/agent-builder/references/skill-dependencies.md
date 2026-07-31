# Companion skill dependencies

<!-- generated from catalog/dependencies.json; do not edit -->

Claude Code supports native same-marketplace plugin dependencies. Codex and Cursor do not share that manifest contract, so they use generated warnings and an explicit install plan. Companions remain separate plugins so their identities do not collide.

## Required for full route coverage

| Skill | Minimum | Why |
|---|---:|---|
| `agent-architect` | `1.0.0` | Creation and redesign scenarios delegate individual-agent architecture. |
| `agent-context` | `1.0.0` | Research scenarios delegate provenance-bearing context building. |
| `agent-doctor` | `1.0.0` | Repair and incident scenarios delegate diagnosis and recovery. |
| `agent-evaluator` | `1.0.0` | All release and comparison gates require independent evaluation. |
| `agent-manager` | `1.0.0` | Lifecycle transitions and host verification belong to the manager. |
| `agent-optimizer` | `1.0.0` | Measured improvement scenarios delegate healthy-agent optimization. |
| `agent-refactor` | `1.0.0` | Boundary and topology scenarios delegate refactoring. |
| `agent-scout` | `1.0.0` | Full lifecycle begins with the agent worth and coverage gate. |

## Recommended

| Skill | Minimum | Why |
|---|---:|---|
| `agent-best-practices` | `1.0.0` | Provides shared evidence for pattern and lifecycle decisions. |

## Runtime rule

Before dispatching a route, compare its owning companion with the skills available in the current session. If a required companion is missing or older than the minimum, emit a visible `DEPENDENCY WARNING`, name the blocked route, and do not imitate that specialist. Other routes may continue when their companions are available. Missing recommended skills are informational unless the chosen workflow needs them. If installed state cannot be inspected, say that dependency status is unverified.

## Codex installation

From the marketplace repository, preview or execute the complete plan:

```bash
python3 scripts/manage_skill_dependencies.py plan agent-builder --host codex
python3 scripts/manage_skill_dependencies.py install agent-builder --host codex --execute
```

Manual equivalent:

```bash
codex plugin add agent-architect@im-skills
codex plugin add agent-context@im-skills
codex plugin add agent-doctor@im-skills
codex plugin add agent-evaluator@im-skills
codex plugin add agent-manager@im-skills
codex plugin add agent-optimizer@im-skills
codex plugin add agent-refactor@im-skills
codex plugin add agent-scout@im-skills
codex plugin add agent-builder@im-skills
```

For Claude Code, install only the requested plugin; its generated `dependencies` array auto-installs required companions from the same marketplace.
