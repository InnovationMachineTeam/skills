# Architecture

## Two planes: marketplace distribution and project agent assets

The repository separates globally distributable marketplace skills from
project-scoped agent assets. This is a capability boundary, not a claim that
private content is secret.

```text
skills/<category>/*                         public canonical skills
        │
        └── marketplace builders ─────────> plugins/ and plugin/

.agents/definitions/<agent>/agent.json     canonical agent definition
.agents/definitions/<agent>/skills/*       owner-only private skills
.agents/definitions/<agent>/commands/*     owner-only private commands
        │
        ├── AGENT-ASSET-REGISTRY.json      identity, hash, ownership, lifecycle
        ├── AGENT-SKILLS-MAP.json           versioned capability bindings
        └── adapter generator ─────────────> .codex/.claude/.cursor agent views
```

`docs/AGENT-ASSET-REGISTRY.json` and `docs/AGENT-SKILLS-MAP.json` are the
machine-readable sources of truth. Their Markdown counterparts are generated
review views. All registry/map mutations use optimistic revision preconditions,
candidate validation, and rollback through `manage_agent_assets.py
apply-transaction`.

The `register` command only renders a candidate asset record. It intentionally
refuses `--write`; place the record and its binding change in an
`apply-transaction` document. `sync-public` is the bounded reconciliation path
for unbound canonical marketplace skills.

Private skills and commands:

- live only below their owning agent definition;
- declare exactly one allowed consumer, equal to `owner_agent_ref`;
- are excluded from marketplace packaging;
- fail validation if orphaned, mapped to another agent, or moved into a public
  discovery root;
- are projected per host using the enforcement described in
  [HOST-CONFORMANCE.md](HOST-CONFORMANCE.md).

Agent definitions declare a capability budget. Registry validation rejects map
drift, version drift, duplicate bindings, orphan private capabilities, and
budgets that are exceeded. Private commands inherit the owning agent's SemVer
and keep only their own revision and content hash.

## Marketplace: one source, four distribution views

```text
skills/<category>/<name>/               canonical source of truth
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

Companion-skill relationships are canonical in `catalog/dependencies.json`.
Claude Code receives native same-marketplace plugin dependencies; Codex, Cursor
and generic Agent Skills consumers receive generated warnings and explicit
dependency-first plans. See [SKILL-DEPENDENCIES.md](SKILL-DEPENDENCIES.md).

## Host contracts

| Host | Repository entry point | Package manifest | Selective install |
|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` | `.claude-plugin/plugin.json` | one entry per skill |
| Codex | `.agents/plugins/marketplace.json` | `.codex-plugin/plugin.json` | one entry per skill |
| Cursor | `.cursor-plugin/marketplace.json` | `.cursor-plugin/plugin.json` | one entry per skill after native publication; Skills CLI while private |
| Agent Skills clients | `skills/<category>/*/SKILL.md` | skill frontmatter | client-specific |

The three plugin marketplaces all resolve to the same generated `plugins/<name>/` package. This avoids platform forks while allowing each host to receive its native manifest.

## Generated artifact policy

- `skills/*/` category roots and `catalog/` are authoritative.
- `plugins/`, `plugin/`, and all three marketplace manifests are generated and committed.
- Generated packages contain real files, never symlinks or references outside the package.
- CI rebuilds artifacts in `build/` and rejects any diff.
- Every generated manifest gets the same plugin name and SemVer as the canonical skill.
- The aggregate has independent SemVer because its installed contract changes whenever its composition or host support changes.

## Naming and categories

- Marketplace identifier: `im-skills` on all hosts.
- Individual plugin identifier: exact globally unique skill name.
- Aggregate plugin identifier: `im-skills-all`.
- Canonical and Cursor categories: `agent-os-skills`, `agent-team-skills`,
  `agent-skills`, `metaskills`, and `prompt-skills`.
- Codex install-surface category: `Developer Tools`.

Categories are presentation metadata, not identity boundaries. Skill and plugin names must remain globally unique inside an installed host scope.

## Trust boundary

Manifests declare only components that exist. Bundles do not include MCP servers, hooks, agents, commands, or variables unless those components are intentionally added and validated for every target host. Secrets are never embedded; future configurable integrations must use host-supported variable declarations and placeholders.

The marketplace builders only read `skills/`; they never package
`.agents/definitions/`. Repository validation independently verifies this
separation. Host projections are generated runtime/configuration artifacts and
must not be treated as a second canonical source.

## Portability

Each installed skill contains all required scripts, references, prompts, assets, evals, and host metadata. Parent references, absolute local runtime paths, symlinks, OS metadata, bytecode, VCS internals, and undeclared executable payloads are excluded or rejected.
