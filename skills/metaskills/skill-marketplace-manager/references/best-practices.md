# Skill Marketplace Design Best Practices

Status: canonical operating reference for `skill-marketplace-manager`
Last source verification: July 30, 2026

## Contents

1. [Core decisions](#core-decisions)
2. [Canonical structure](#canonical-structure)
3. [Categories and naming](#categories-and-naming)
4. [skill.sh compatibility](#skillsh-compatibility)
5. [Claude Code: plugin and marketplace](#claude-code-plugin-and-marketplace)
6. [Versions and releases](#versions-and-releases)
7. [Build and portability](#build-and-portability)
8. [Validation and testing](#validation-and-testing)
9. [Security and governance](#security-and-governance)
10. [Migration](#migration)
11. [Documentation and maintenance](#documentation-and-maintenance)
12. [Resolving contradictions](#resolving-contradictions)
13. [Sources](#sources)

## Core decisions

1. Keep skills in a single canonical `skills/` tree.
2. Allow no more than one category level: `skills/<category>/<skill>/SKILL.md`.
3. Generate harness-specific artifacts instead of maintaining multiple manual copies.
4. Use a separate marketplace manifest and a separate self-contained aggregate plugin.
5. Treat categories as catalog organization, not as the skill namespace.
6. Separate the skill version, plugin version, and catalog version.
7. Allow a release only after static, integration, and behavioral verification.
8. Perform migration through staging, a pilot, reversible cutover, and explicit confirmation before removing the old structure.
9. Do not invent dependency fields in host manifests: keep the companion graph separately and generate warnings plus a dependency-first install plan.

## Canonical structure

Recommended repository shape:

```text
skill-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── skills/                         # the only source of truth
│   ├── metaskills/
│   │   └── skill-architect/
│   │       ├── SKILL.md
│   │       └── ...
│   ├── agent-workflows/
│   ├── product/
│   ├── development/
│   └── marketing/
├── plugin/                         # generated aggregate plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   └── build-manifest.json
├── scripts/
├── tests/
└── README.md
```

Why this structure:

- `skills/` matches the Agent Skills model and is discoverable by skill.sh.
- `.claude-plugin/marketplace.json` describes installable catalog offerings.
- `plugin/` lets you verify the whole set locally via `claude --plugin-dir ./plugin`.
- the generated copy protects against dependencies outside the plugin cache.

Do not keep two peer manual copies of the same skill. If a consumer requires a different layout, create a deterministic build and verify absence of drift by hashes.

## Categories and naming

Use categories only for stable domains and ownership policies. The current portfolio uses `agent-os-skills`, `agent-team-skills`, `agent-skills`, `metaskills`, and `prompt-skills`; keep secondary classification in `tags`. Add future categories only when stable content and an owner exist.

Good examples:

- `metaskills`
- `agent-workflows`
- `product`
- `development`
- `marketing`

Do not use `agents` for skills if the same repository contains Claude Code plugins: `agents/` already means a custom subagents directory. The `agent-workflows` category removes the ambiguity.

Rules:

- the skill name is lowercase kebab-case and matches the directory name;
- the name is unique across the entire aggregate plugin;
- the category is a single primary taxonomy;
- `tags` provide secondary faceted classification;
- do not create empty categories;
- moving between categories must not change `name` if the skill's behavior and identity are unchanged.

## skill.sh compatibility

The `skills` CLI accepts a GitHub/GitLab URL, `owner/repo`, a direct path to a skill, and a local path. For a compatible catalog, support:

```text
skills/<skill>/SKILL.md
skills/<category>/<skill>/SKILL.md
```

Do not add another nesting level. Verify discovery before publication:

```bash
npx skills add . --list
npx skills add owner/repo --list
npx skills add owner/repo --skill skill-architect --agent claude-code --agent codex
```

Do not install the same skill at the same time through skill.sh and the Claude marketplace into one visibility scope. That creates duplicates, unclear version precedence, and trigger conflicts.

## Claude Code: plugin and marketplace

### Plugin

The plugin root contains `.claude-plugin/plugin.json`; components live alongside `.claude-plugin`, not inside it. For categories, list the directories that directly contain skill folders:

```json
{
  "name": "skill-toolkit",
  "displayName": "Skill Toolkit",
  "version": "1.0.0",
  "description": "Portable skill engineering toolkit",
  "skills": [
    "./skills/metaskills",
    "./skills/agent-workflows"
  ]
}
```

Local verification:

```bash
claude --plugin-dir ./plugin
```

Plugin skills receive a namespace from the plugin name. Do not rely on namespace as a substitute for uniqueness within a single aggregate plugin.

### Marketplace

Keep the manifest in `.claude-plugin/marketplace.json`. For a monorepo, a shared-root pattern is acceptable: the marketplace entry specifies `source: "./"`, `strict: false`, and an explicit `skills` path. Example:

```json
{
  "name": "skill-toolkit-marketplace",
  "owner": { "name": "Skill Toolkit Maintainers" },
  "plugins": [
    {
      "name": "metaskills",
      "source": "./",
      "strict": false,
      "description": "Skills for creating and governing skills",
      "version": "1.0.0",
      "category": "metaskills",
      "tags": ["skills", "meta", "governance"],
      "skills": "./skills/metaskills"
    }
  ]
}
```

With `strict: false`, the marketplace entry defines its own components. Do not duplicate conflicting component paths in the root plugin manifest.

Verify the user path:

```text
/plugin marketplace add owner/repository
/plugin install metaskills@skill-toolkit-marketplace
```

And the CLI equivalent:

```bash
claude plugin marketplace add owner/repository
claude plugin install metaskills@skill-toolkit-marketplace
```

## Versions and releases

Distinguish three independent concepts:

| Version | Where | What changes |
|---|---|---|
| Skill version | `SKILL.md → metadata.version` | Contract and content of an individual skill |
| Plugin version | `plugin.json → version` | Installable aggregate bundle |
| Marketplace entry version | `marketplace.json → plugins[].version` | Release of a catalog offering |

Use SemVer as the project policy. When versions are explicit, bump them in every release; otherwise the consumer may not see the update. Do not set the same release version in both `plugin.json` and the marketplace entry without automatic equality verification. In Claude Code, version resolution priority depends on the manifest/entry/source revision, so manual duplication creates a divergence risk.

For a change to only one skill:

1. bump the skill's `metadata.version`;
2. rebuild the bundle;
3. bump the version of the installable offering that contains the skill;
4. record changelog/release notes at the repository level;
5. verify upgrade from the previous published version.

## Build and portability

A plugin installed from a marketplace is cached. Therefore, each bundle must be self-contained:

- copy the entire skill directory, including `scripts/`, `references/`, `assets/`, `prompts/`, `evals/`, and `agents/`;
- exclude only predeclared non-runtime junk: `.DS_Store`, `__pycache__`, `*.pyc`, `.git`;
- leave no `../` links to the source monorepo;
- do not use absolute local paths;
- reject symlinks unless target-harness behavior has been explicitly verified;
- create the build in a new staging directory;
- write a build manifest with SHA-256;
- compare the build manifest in CI to detect drift;
- do not edit the generated bundle manually.

### Dependencies between skills

Claude Code supports `dependencies` in `plugin.json` and can automatically install companion plugins from the same marketplace. Codex has no documented field for one plugin depending on another; in `agents/openai.yaml`, only `dependencies.tools` is supported, meaning dependencies on MCP tools rather than skills. Therefore, the portable model must have one source and different host projections:

- `required` means that without the companion skill, its owned route is blocked, but not necessarily the entire installed skill;
- `recommended` is neither installed nor blocking automatically;
- the graph is stored separately from strict manifests and validated for unknown names, versions, duplicates, and cycles;
- required edges are projected into the Claude manifest; the package README and machine-readable metadata include a visible warning and a fallback installation order for other hosts;
- the dependency-aware helper first shows a dry run and performs installation only after explicit `--execute`;
- the orchestrator must not imitate a missing specialist;
- dependencies must not be copied into each individual plugin if that creates multiple active copies of one skill identity.

If the user needs one installable unit, it is safer to release a separate suite/aggregate plugin with a unique install boundary and verify that it is not activated at the same time as overlapping individual plugins.

## Validation and testing

Minimum release matrix:

| Layer | Check | Required result |
|---|---|---|
| Agent Skills | YAML, `name`, `description`, directory match, self-containment | PASS for every skill |
| Catalog | unique names, category depth, links, versions | PASS |
| Portable CLI | `npx skills add . --list` | all expected skills discovered |
| Claude marketplace | `claude plugin validate .` | PASS |
| Claude plugin | `claude plugin validate ./plugin --strict` | PASS |
| Local load | `claude --plugin-dir ./plugin` | representative skill is available |
| Routing | positive, negative, ambiguous, collision prompts | defined threshold |
| Behavior | at least one scenario per critical route | PASS |
| Upgrade | previous → candidate | new version detected |
| Security | secrets, traversal, executable provenance, unsafe install | PASS |

This skill's portable helper does not replace harness-native validators. If a CLI is unavailable, mark `NOT RUN`, not `PASS`.

In CI, separate fast pull request checks from more expensive release gates. Do not publish when there is drift, a collision, an invalid manifest, a broken link, a failed smoke test, or a missing version bump.

## Security and governance

- treat a third-party skill as an executable supply-chain artifact;
- verify provenance, license, commit/tag, and integrity;
- read scripts before execution and run them with minimum authority;
- do not store tokens or credentials in manifests, prompts, fixtures, or logs;
- pin trusted marketplace sources by administrative policy;
- separate author, reviewer, and publisher for important releases;
- maintain allowlist/denylist controls and an urgent revocation procedure;
- document telemetry without user prompt contents or secrets;
- run a pilot in an isolated visibility scope;
- ensure recovery of the previous version.

For a private marketplace, separately verify authentication for target users and CI. Do not treat the author's access as proof of consumer availability.

## Migration

Migration order:

1. Record the inventory and hashes of the source structure.
2. Agree on the `source → target` mapping, categories, and owners.
3. Copy skills into staging; do not move the source.
4. Fix only internal portability defects.
5. Create the marketplace manifest.
6. Build the aggregate plugin from the staging source.
7. Run the full verification matrix.
8. Perform a pilot installation.
9. Approve cutover.
10. Leave the old structure recoverable for the defined period.
11. Delete or archive it only through a separate confirmed action.

Rollback must be described before cutover and include the source of the previous version, the reinstallation method, activation criteria, and the responsible owner.

## Documentation and maintenance

The marketplace README must include:

- purpose and supported harnesses;
- the offerings catalog and categories;
- installation and removal commands;
- local development;
- versioning and compatibility policy;
- security/reporting policy;
- contribution and review gates;
- known limitations;
- ownership and release process.

Keep this file inside the skill as the canonical operating reference. The central `skill-best-practices` may index and track sources, but it must not become a runtime dependency of the installed `skill-marketplace-manager`.

## Resolving contradictions

### "One plugin" vs. "one plugin per category"

Use both representations for different jobs: a generated aggregate plugin for local development and the full set; category-based marketplace entries for selective installation. The canonical source remains single.

### `plugin.json` vs. `strict: false`

Use `plugin.json` for a self-contained plugin. Use `strict: false` for shared-root marketplace entries with explicit component paths. Do not force one root manifest to describe incompatible component sets for multiple entries.

### README inside the skill

General context-efficiency guidance recommends not adding supporting documentation to every skill. Here, the README is an explicitly requested user interface for a complex multi-mode tool. Runtime instructions remain in `SKILL.md`, and the README is not required for route execution.

### Flat catalog vs. categories

A flat layout is simpler, but categories are useful for a large portfolio. The one-level limit preserves skill.sh compatibility and prevents arbitrary taxonomy depth.

## Sources

Primary and official sources:

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills — Best practices](https://agentskills.io/skill-creation/best-practices)
- [Agent Skills — Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Agent Skills — Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)
- [Agent Skills — Using scripts](https://agentskills.io/skill-creation/using-scripts)
- [Agent Skills — Adding skills support](https://agentskills.io/client-implementation/adding-skills-support)
- [Claude Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Vercel Skills CLI / skill.sh](https://github.com/vercel-labs/skills)
- [Anthropic: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)

Analyzed public implementations and patterns:

- [garrytan/gstack](https://github.com/garrytan/gstack)
- [garrytan/gbrain](https://github.com/garrytan/gbrain)

Before changing a manifest format or release workflow, recheck the current harness-specific documents: these contracts can change independently of the Agent Skills specification.
