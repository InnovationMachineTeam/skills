# Architecture

## Two planes: marketplace distribution and project agent assets

The repository separates globally distributable marketplace skills from
project-scoped agent assets. This is a capability boundary, not a claim that
private content is secret.

The [Onboarding Guide](ONBOARDING.md) applies this architecture to individual
agents, teams, and Agentic OS. [Worked use cases](use-cases/README.md) show the
same boundaries across software, learning, research, innovation, and business.

```text
skills/<category>/*                         public canonical skills
        │
        ├── <skill>/private-skills/*       parent-only bundled subskills
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

Package-private subskills are a different, narrower mechanism. They may live
under one public skill's `private-skills/<name>/SKILL.md` only when the parent
is their sole consumer and explicitly dispatches them. They are bundled as
progressively loaded parent resources, have independent internal versions and
evals, but receive no catalog entry, global registry identity, UI metadata or
independent host binding. Marketplace and asset scanners recognize this exact
layout without adding the subskills to global discovery. A second independent
consumer requires extraction and public/private placement assessment; copying
or widening the parent-only allow-list is not allowed.

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
| Cursor | `.cursor-plugin/marketplace.json` | `.cursor-plugin/plugin.json` | public repository supports Skills CLI now; native publication still requires Cursor review |
| Agent Skills clients | `skills/<category>/*/SKILL.md` | skill frontmatter | client-specific |

The three plugin marketplaces all resolve to the same generated `plugins/<name>/` package. This avoids platform forks while allowing each host to receive its native manifest.

## Generated artifact policy

- `skills/*/` category roots and `catalog/` are authoritative.
- `plugins/`, `plugin/`, and all three marketplace manifests are generated and committed.
- Generated packages contain real files, never symlinks or references outside the package.
- CI rebuilds artifacts in `build/` and rejects any diff.
- Every generated manifest gets the same plugin name and SemVer as the canonical skill.
- The aggregate has independent SemVer because its installed contract changes whenever its composition or host support changes.

## Instruction hierarchy

Important canonical directories contain byte-identical `CLAUDE.md` and
`AGENTS.md` pairs. The pair at the repository root defines global constraints;
deeper pairs add only local instructions for docs, skills, categories, catalog,
or scripts. Changing either peer requires changing the other at the same level.
Repository validation rejects a missing or divergent peer.

Instruction files are operating guidance, not a replacement for skill
frontmatter, registries, schemas, policy enforcement, or user authority.

## Documentation and knowledge plane

`docs/` is the portable, human-reviewable memory plane. Agent definitions
declare exact read/write roots, ownership, provenance, review, and freshness.
Domain branches are created on demand for named consumers. Machine-readable
registries remain canonical for typed state; Markdown views remain review
surfaces.

LLM Wiki, Obsidian, Graphify, vector retrieval, graph databases, and GraphRAG
may project or enrich this plane only after a measured need and an approved
setup, access, provenance, deletion, freshness, and rebuild contract. Derived
indexes never become trusted merely because retrieval returned them.

## Non-discoverable candidates

`candidates/` contains reviewable bundles that are intentionally outside the
marketplace lifecycle. They may be validated directly and may vendor renamed
read-only donor snapshots, but repository builders must not scan or package
them. A candidate has no catalog entry, generated plugin, marketplace entry or
host activation claim.

Promotion is a separate transaction: pass the documented maturity gate, freeze
evaluation and rollback evidence, create the canonical `skills/` entry, update
registry/catalog/dependencies, regenerate packages, and verify host discovery.

## Naming and categories

- Marketplace identifier: `im-skills` on all hosts.
- Individual plugin identifier: exact globally unique skill name.
- Aggregate plugin identifier: `im-skills-all`.
- Canonical and Cursor categories: `agent-master`, `agent-os-skills`,
  `agent-team-skills`, `agent-skills`, `metaskills`, and `prompt-skills`.
- Codex install-surface category: `Developer Tools`.

Categories are presentation metadata, not identity boundaries. Skill and plugin names must remain globally unique inside an installed host scope.

## Trust boundary

Manifests declare only components that exist. Bundles do not include MCP servers, hooks, agents, commands, or variables unless those components are intentionally added and validated for every target host. Secrets are never embedded; future configurable integrations must use host-supported variable declarations and placeholders.

The marketplace builders only read `skills/`; they include package-private
subskills inside their owning public bundle but never expose them as top-level
entries. They never package `.agents/definitions/`. Repository validation
independently verifies this separation. Host projections are generated
runtime/configuration artifacts and must not be treated as a second canonical
source.

## Portability

Each installed skill contains all required scripts, references, prompts, assets, evals, and host metadata. Parent references, absolute local runtime paths, symlinks, OS metadata, bytecode, VCS internals, and undeclared executable payloads are excluded or rejected.
