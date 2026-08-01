# Companion skill dependencies

<!-- generated from catalog/dependencies.json; do not edit -->

Claude Code supports native same-marketplace plugin dependencies. Codex and Cursor do not share that manifest contract, so they use generated warnings and an explicit install plan. Companions remain separate plugins so their identities do not collide.

## Required for full route coverage

None.

## Recommended

| Skill | Minimum | Why |
|---|---:|---|
| `skill-builder` | `1.4.0` | Recommended for evidence-backed skill lifecycle and productionization gates. |
| `skill-architect` | `1.2.0` | Recommended for capability form, visibility, boundary and host-native package decisions. |
| `skill-evaluator` | `1.1.0` | Recommended for independent frozen skill evaluation and holdout evidence. |
| `prompt-optimize` | `3.0.0` | Recommended for durable orchestrator and role-agent system prompts. |
| `agent-team-architect` | `1.1.0` | Recommended when the process justifies multiple standalone role agents. |
| `agent-model-selector` | `1.0.0` | Recommended when model selection must be evidence-backed per role. |
| `agent-os-architect` | `1.0.0` | Recommended when durable shared runtime planes are justified. |
| `agent-observer` | `1.0.0` | Recommended for operational logs, traces, metrics, SLOs and incident design. |
| `agent-os-bootstrapper` | `1.0.0` | Recommended when an approved harness walking skeleton must be materialized. |
| `agent-os-evaluator` | `1.0.0` | Recommended for independent harness integration, recovery and lifecycle evidence. |

## Runtime rule

Before dispatching a route, compare its owning companion with the skills available in the current session. If a required companion is missing or older than the minimum, emit a visible `DEPENDENCY WARNING`, name the blocked route, and do not imitate that specialist. Other routes may continue when their companions are available. Missing recommended skills are informational unless the chosen workflow needs them. If installed state cannot be inspected, say that dependency status is unverified.

## Codex installation

From the marketplace repository, preview or execute the complete plan:

```bash
python3 scripts/manage_skill_dependencies.py plan agent-master --host codex
python3 scripts/manage_skill_dependencies.py install agent-master --host codex --execute
```

Manual equivalent:

```bash
codex plugin add agent-master@im-skills
```

For Claude Code, install only the requested plugin; its generated `dependencies` array auto-installs required companions from the same marketplace.
