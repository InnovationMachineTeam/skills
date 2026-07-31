# Skill dependency policy

Status: implemented for marketplace release `3.1.0`.

## Decision

`catalog/dependencies.json` is the only hand-maintained source of truth for
companion-skill relationships. It distinguishes:

- `required`: needed for the route owned by that companion; a missing or stale
  companion produces `DEPENDENCY WARNING` and blocks that route;
- `recommended`: useful for conditional workflows, but installed only when the
  user opts in.

The graph records minimum skill versions, validates identity and version
integrity, rejects duplicate edges, self-dependencies and required cycles, and
keeps explanatory rationale with every edge.

## Host projections

| Host | Projection | Installation behavior |
|---|---|---|
| Claude Code | Generated `.claude-plugin/plugin.json → dependencies` | Required same-marketplace plugins are installed automatically with the requested plugin. |
| Codex | No plugin dependency field; generated warning and install plan | `manage_skill_dependencies.py install ... --execute` installs the dependency closure first. |
| Cursor | No shared dependency contract used by this marketplace | Generated warning and explicit companion list; install through the supported channel. |
| Agent Skills clients | Canonical runtime reference inside the affected skill | The agent warns and blocks only a route whose specialist is unavailable. |

Codex `agents/openai.yaml → dependencies.tools` is reserved for MCP tool
dependencies and must not be used for companion skills.

## Commands

Validate and regenerate runtime references:

```bash
python3 scripts/manage_skill_dependencies.py validate
python3 scripts/manage_skill_dependencies.py render
python3 scripts/manage_skill_dependencies.py render --check
```

Preview, install and verify a Codex dependency closure:

```bash
python3 scripts/manage_skill_dependencies.py plan skill-builder --host codex
python3 scripts/manage_skill_dependencies.py install skill-builder --host codex --execute
python3 scripts/manage_skill_dependencies.py check skill-builder --host codex
```

For Claude Code, one target command is sufficient because the generated
manifest declares the required companion plugins:

```bash
claude plugin install skill-builder@im-skills
```

Use `--include-recommended` only when the planned workflow needs optional
companions. `install` remains a dry run unless `--execute` is present.

## Packaging invariants

1. Individual packages continue to bundle exactly one canonical skill.
2. Dependencies remain separate installable plugins; they are not copied into
   dependent packages, avoiding duplicate identities and ambiguous routing.
3. Every affected package contains `skill-dependencies.json` and a visible
   README warning generated from the canonical graph.
4. Every affected orchestrator contains a generated
   `references/skill-dependencies.md` and must not imitate a missing specialist.
5. Generated packages, runtime references and Claude manifests are checked for
   drift in CI.

## Sources

- [Claude Code plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Codex: Build skills](https://developers.openai.com/plugins/build/skills)
- [Codex: Package plugins](https://developers.openai.com/plugins/build/plugins)
