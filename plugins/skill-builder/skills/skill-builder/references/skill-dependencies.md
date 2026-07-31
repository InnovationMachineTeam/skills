# Companion skill dependencies

<!-- generated from catalog/dependencies.json; do not edit -->

Claude Code supports native same-marketplace plugin dependencies. Codex and Cursor do not share that manifest contract, so they use generated warnings and an explicit install plan. Companions remain separate plugins so their identities do not collide.

## Required for full route coverage

| Skill | Minimum | Why |
|---|---:|---|
| `prompt-optimize` | `3.0.0` | The prompt-development scenario delegates prompt design and optimization. |
| `skill-architect` | `1.2.0` | Creation and topology scenarios delegate skill architecture. |
| `skill-doctor` | `1.0.0` | Repair scenarios delegate diagnosis and minimal repair. |
| `skill-evaluator` | `1.1.0` | Evaluation and release gates require independent skill evaluation. |
| `skill-harvester` | `1.1.0` | Research and external intake scenarios delegate evidence harvesting. |
| `skill-manager` | `1.2.0` | Lifecycle, installation and governance scenarios delegate installed-state management. |
| `skill-optimizer` | `1.0.0` | Measured improvement scenarios delegate healthy-skill optimization. |
| `skill-refactor` | `1.2.0` | Split, merge, extraction and boundary-change scenarios delegate refactoring. |
| `skill-scout` | `1.1.0` | Opportunity-discovery scenarios delegate skill scouting. |

## Recommended

None.

## Runtime rule

Before dispatching a route, compare its owning companion with the skills available in the current session. If a required companion is missing or older than the minimum, emit a visible `DEPENDENCY WARNING`, name the blocked route, and do not imitate that specialist. Other routes may continue when their companions are available. Missing recommended skills are informational unless the chosen workflow needs them. If installed state cannot be inspected, say that dependency status is unverified.

## Codex installation

From the marketplace repository, preview or execute the complete plan:

```bash
python3 scripts/manage_skill_dependencies.py plan skill-builder --host codex
python3 scripts/manage_skill_dependencies.py install skill-builder --host codex --execute
```

Manual equivalent:

```bash
codex plugin add prompt-optimize@im-skills
codex plugin add skill-architect@im-skills
codex plugin add skill-doctor@im-skills
codex plugin add skill-evaluator@im-skills
codex plugin add skill-harvester@im-skills
codex plugin add skill-manager@im-skills
codex plugin add skill-optimizer@im-skills
codex plugin add skill-refactor@im-skills
codex plugin add skill-scout@im-skills
codex plugin add skill-builder@im-skills
```

For Claude Code, install only the requested plugin; its generated `dependencies` array auto-installs required companions from the same marketplace.
