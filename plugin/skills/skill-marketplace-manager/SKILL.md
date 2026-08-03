---
name: skill-marketplace-manager
description: Design, inventory, scaffold, curate, build, document, validate, migrate, release, and audit repositories that distribute Agent Skills through skill.sh-compatible catalogs and plugin harnesses such as Claude Code. Use for marketplace topology, category design, marketplace.json or plugin.json generation, portable skills/ layouts, aggregate plugin builds, skill documentation and onboarding sets, catalog governance, version policy, compatibility checks, staged migrations, publishing plans, or repository-wide skill distribution. Do not use for authoring one skill's behavior, evaluating one skill's task quality, ordinary product documentation outside a skill marketplace, or managing only the installed runtime state of skills.
metadata:
  version: "1.4.1"
---

# Skill Marketplace Manager

Manage a skill catalog as a governed distribution product. Preserve one canonical skill source, generate harness-specific bundles, and separate inspection, planning, mutation, and publication authority.

## Classify the request

Choose one primary route. Add secondary routes only when the requested outcome requires them.

| Route | Use for | Default authority | Load |
|---|---|---|---|
| `inventory-audit` | Discover skills, manifests, categories, duplicates, drift, and portability risks | Read-only | `prompts/inventory-audit.md` |
| `architecture-design` | Choose canonical roots, categories, plugin boundaries, naming, and distribution channels | Plan-only | `prompts/architecture-design.md` |
| `scaffold-marketplace` | Create an approved catalog or plugin skeleton | Write local files | `prompts/scaffold-marketplace.md` |
| `catalog-curation` | Add, move, classify, deprecate, or document catalog entries | Plan first; write after scope is clear | `prompts/catalog-curation.md` |
| `build-sync` | Produce a self-contained plugin bundle from canonical skills and detect drift | Write generated output only | `prompts/build-sync.md` |
| `documentation` | Document canonical skills or create marketplace onboarding from verified repository evidence | Plan first; write only in approved documentation roots | `private-skills/skill-documentation-writer/SKILL.md` |
| `validate-compatibility` | Validate Agent Skills, skill.sh, Claude Code, links, security, and install smoke tests | Read-only unless fixes are requested | `prompts/validate-compatibility.md` |
| `migration` | Plan or apply a staged migration with checkpoints and rollback | Plan-only unless apply is explicit | `prompts/migration.md` |
| `release-distribution` | Version, package, publish, install-test, or retire releases | No external mutation without approval | `prompts/release-distribution.md` |

If the user names a route, use it. Otherwise infer the narrowest route from the requested outcome. If the evidence supports several materially different architectures, ask only for the decision that changes the result.

Read `prompts/base.md` for every public marketplace route, then read the selected route prompt from the table. For `documentation`, read [references/private-skill-registry.json](references/private-skill-registry.json) and dispatch the package-private [skill-documentation-writer](private-skills/skill-documentation-writer/SKILL.md) instead of treating it as a globally discoverable route.

## Establish the operating mode

Treat the route and the operating mode as separate dimensions:

- `inspect`: observe and report; do not modify files.
- `plan`: propose exact changes, gates, ownership, and rollback; do not apply them.
- `apply`: make explicitly authorized local changes and preserve unrelated work.
- `verify`: test declared contracts against actual artifacts; do not repair unless asked.

Default to `inspect` for audits, `plan` for migrations, and `verify` for validation. Never infer permission to publish, install globally, delete the old tree, rewrite release history, or rotate credentials.

## Run the common workflow

1. Define the target outcome, repository root, harnesses, visibility, and requested mode.
2. Inventory the current state before proposing topology or mutations.
3. Identify the canonical source of each skill and every generated or mirrored consumer.
4. Check names, category depth, versions, links, scripts, manifests, and distribution collisions.
5. Select one architecture and record rejected alternatives with concise rationale.
6. Execute only the chosen route and authorized mode.
7. Validate at three levels: static structure, harness discovery, and representative behavior.
8. Report artifacts, evidence, unresolved risks, rollback path, and next decision.

Read [best-practices.md](references/best-practices.md) for every architecture, migration, or release route. Read [manifest-patterns.md](references/manifest-patterns.md) before editing a manifest. Read [migration-contract.md](references/migration-contract.md) before planning or applying a migration. Read [integration-contracts.md](references/integration-contracts.md) when another skill specialist owns part of the work.

## Enforce architectural invariants

- Keep a single canonical `skills/` source tree. Treat plugin bundles as generated distribution artifacts.
- Support at most one category directory between `skills/` and a skill when skill.sh compatibility is required.
- Keep skill names globally unique across an aggregate plugin; categories are organization, not a namespace.
- Keep every distributed skill self-contained. Do not rely on paths outside its installed or cached package.
- Do not add plugin-to-plugin dependency fields to host manifests unless the
  target host documents them. Keep a canonical companion-skill graph, generate
  warnings and install plans from it, and bundle only when duplicate identities
  cannot result.
- Keep `metadata.version` in each `SKILL.md` distinct from plugin or marketplace release versions.
- Do not declare the same version in multiple manifests unless an automated consistency check enforces equality.
- Do not expose the same skill twice in the same harness scope through overlapping install channels.
- Prefer `agent-workflows` or `agent-skills` over `agents` as a catalog category to avoid confusion with a plugin's `agents/` component.
- Reject symlinks and parent-directory references in generated portable bundles unless the target harness explicitly guarantees them.
- Generate into a staging directory, validate it, then promote it. Do not build destructively in place.

## Use deterministic helpers

Run `scripts/validate_marketplace.py <repo>` for portable structural checks. Use `--json` for machine-readable output.

Run `scripts/build_plugin_bundle.py <repo> <new-output-dir> --plugin-name <name> --version <semver>` only when a generated aggregate Claude Code plugin is wanted. The output directory must not already exist.

Run `scripts/check_evals.py evals` after editing the evaluation corpus.

Harness-native validators remain authoritative. A portable helper can catch errors early but cannot certify a harness it does not execute.

## Dispatch private documentation work

Use `skill-documentation-writer` only for the `documentation` route and only through this parent skill. Pass an explicit dispatch envelope containing:

- exact canonical skills, catalog files, manifests and documentation roots;
- target audience, supported hosts and required document types;
- whether the operation is inspect, plan, create, update or verify;
- allowed writes, preserved handcrafted content and forbidden effects;
- required examples, expected outcomes, commands and verification evidence.

The private specialist may create or update skill README files, marketplace onboarding guides and documentation audits. It must not alter skill behavior, register or publish assets, bump versions, rebuild packages, activate a host, invent successful executions, or expose itself as a marketplace entry. This parent retains versioning, catalog, packaging, release and lifecycle decisions.

## Apply route-specific rules

### Inventory and validation

Return an evidence-based catalog, not a guessed summary. Distinguish `PASS`, `WARN`, `FAIL`, and `NOT RUN`. Include the exact path or manifest entry behind each finding. Do not convert a missing external CLI into a passing result.

### Architecture and scaffolding

Prefer the smallest catalog that satisfies current consumers. Create categories only when they contain skills or enforce a meaningful policy. Use tags for secondary classification. Keep `.claude-plugin/marketplace.json` at the marketplace root and `.claude-plugin/plugin.json` at each plugin root.

### Build and synchronization

Copy complete skill directories into a self-contained bundle. Preserve category layout and point the plugin manifest at directories that directly contain skill folders. Emit a content-hash manifest so CI can detect drift.

### Migration

Copy to a staging tree before any cutover. Keep the old source recoverable until acceptance gates pass and the user approves retirement. Define collision handling, link rewriting, validation, ownership, observability, rollback triggers, and rollback commands before apply mode.

### Release and distribution

Require explicit confirmation of repository, visibility, channel, version, and affected users before an external release. Use a pilot installation before broad rollout. Never expose secrets in manifests, logs, fixtures, or documentation.

## Coordinate with adjacent skills

- Hand individual skill creation or behavioral redesign to `skill-architect`.
- Hand independent task-quality evaluation and trigger testing to `skill-evaluator`.
- Hand diagnosis of a broken individual skill to `skill-doctor`.
- Hand capability merge/split decisions to `skill-refactor`.
- Hand installed-state activation, rollback, and lifecycle governance to `skill-manager`.
- Hand multi-stage orchestration across these specialists to `skill-builder`.
- Keep repository-backed skill documentation and onboarding production in the package-private `skill-documentation-writer`.

Remain responsible for repository topology, catalog manifests, generated plugin bundles, cross-harness discovery, distribution policy, and marketplace migration.

## Produce a completion report

Include:

1. route and operating mode;
2. scope and canonical source decision;
3. files created or changed;
4. validators and smoke tests actually run;
5. findings by severity;
6. release or migration status;
7. rollback state;
8. unresolved decisions and recommended next step.

Do not claim a marketplace is installable until the target harness has discovered and loaded at least one representative skill from the built artifact.
