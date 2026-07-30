# Architecture

## One source, four distribution views

```text
skills/metaskills/<name>/                canonical source of truth
        │
        ├── build_individual_plugins.py ──> plugins/<name>/
        │                                  ├── .claude-plugin/plugin.json
        │                                  ├── .codex-plugin/plugin.json
        │                                  ├── .cursor-plugin/plugin.json
        │                                  └── skills/<name>/...
        │
        ├── generate_marketplace.py ──────> .claude-plugin/marketplace.json
        │                                  .agents/plugins/marketplace.json
        │                                  .cursor-plugin/marketplace.json
        │
        └── build_aggregate.py ───────────> plugin/ (all skills, three manifests)
```

The canonical tree keeps the one-category layout used by skill.sh and other Agent Skills clients. Generated plugin bundles flatten the category so every `SKILL.md` is an immediate child of the package's `skills/` directory, as required by Codex plugin ingestion and used by Cursor component discovery.

## Host contracts

| Host | Repository entry point | Package manifest | Selective install |
|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` | `.claude-plugin/plugin.json` | one entry per skill |
| Codex | `.agents/plugins/marketplace.json` | `.codex-plugin/plugin.json` | one entry per skill |
| Cursor | `.cursor-plugin/marketplace.json` | `.cursor-plugin/plugin.json` | one entry per skill after native publication; Skills CLI while private |
| Agent Skills clients | `skills/metaskills/*/SKILL.md` | skill frontmatter | client-specific |

The three plugin marketplaces all resolve to the same generated `plugins/<name>/` package. This avoids platform forks while allowing each host to receive its native manifest.

## Generated artifact policy

- `skills/metaskills/` and `catalog/` are authoritative.
- `plugins/`, `plugin/`, and all three marketplace manifests are generated and committed.
- Generated packages contain real files, never symlinks or references outside the package.
- CI rebuilds artifacts in `build/` and rejects any diff.
- Every generated manifest gets the same plugin name and SemVer as the canonical skill.
- The aggregate has independent SemVer because its installed contract changes whenever its composition or host support changes.

## Naming and categories

- Marketplace identifier: `im-skills` on all hosts.
- Individual plugin identifier: exact globally unique skill name.
- Aggregate plugin identifier: `im-skills-all`.
- Canonical and Cursor category: `metaskills`.
- Codex install-surface category: `Developer Tools`.

Categories are presentation metadata, not identity boundaries. Skill and plugin names must remain globally unique inside an installed host scope.

## Trust boundary

Manifests declare only components that exist. Bundles do not include MCP servers, hooks, agents, commands, or variables unless those components are intentionally added and validated for every target host. Secrets are never embedded; future configurable integrations must use host-supported variable declarations and placeholders.

## Portability

Each installed skill contains all required scripts, references, prompts, assets, evals, and host metadata. Parent references, absolute local runtime paths, symlinks, OS metadata, bytecode, VCS internals, and undeclared executable payloads are excluded or rejected.
