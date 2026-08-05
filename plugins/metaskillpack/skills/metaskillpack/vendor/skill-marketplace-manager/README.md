# skill-marketplace-manager

`skill-marketplace-manager` is a meta-skill for designing, building, validating, migrating, and releasing skill repositories. It is oriented toward a portable Agent Skills layout, skill.sh, and plugin harnesses, primarily Claude Code.

> Current status: `1.4.0`. The skill is created as a reviewable package. It does not perform publication, global installation, removal of the previous structure, or migration cutover without explicit permission.

## What the skill solves

The skill helps answer catalog-wide questions:

- where the canonical skill source lives;
- how to organize `skills/` and categories;
- how to align skill.sh and Claude Code;
- whether to use one aggregate plugin or multiple marketplace entries;
- how to generate a self-contained plugin bundle;
- how to manage skill and distribution versions;
- how to declare and validate companion dependencies without unsupported manifest fields;
- how to verify discovery, installation, upgrade, and rollback;
- how to migrate an existing portfolio into a marketplace safely.

It does not replace `skill-architect` for designing the behavior of an individual skill or `skill-evaluator` for independently assessing the quality of its work.

## Operating modes

| Route | Typical request | Result |
|---|---|---|
| `inventory-audit` | “Review this skill repository” | inventory, manifest map, collisions, risks |
| `architecture-design` | “Design a marketplace for skill.sh and Claude Code” | target architecture and an ADR-like decision |
| `scaffold-marketplace` | “Create a marketplace scaffold” | local structure, manifests, templates |
| `catalog-curation` | “Add or reclassify skills” | mapping and coordinated catalog changes |
| `build-sync` | “Build an aggregate plugin” | self-contained generated bundle and hashes |
| `documentation` | “Document the skills and prepare onboarding” | README, onboarding guide, or audit report based on canonical sources |
| `validate-compatibility` | “Check compatibility and installation” | evidence report with PASS/WARN/FAIL/NOT RUN |
| `migration` | “Move the current skills into a marketplace” | DRAFT plan first; apply only explicitly |
| `release-distribution` | “Prepare or publish a release” | release plan/package/pilot; publication by permission |

An authority mode is also applied:

- `inspect` — read-only;
- `plan` — plan with no changes;
- `apply` — authorized local changes;
- `verify` — checks without automatic repair.

You can name a route directly:

```text
Use skill-marketplace-manager in inventory-audit mode for ./repo.
```

Or describe the goal in natural language:

```text
Prepare this skill set for installation through skill.sh and Claude Code,
but do not publish anything yet.
```

If context is insufficient, the skill will clarify only decisions that change the architecture: target harnesses, visibility, canonical source, release boundary, or permitted mutations.

## Recommended workflow

```text
inventory-audit
      ↓
architecture-design
      ↓
scaffold-marketplace / catalog-curation
      ↓
build-sync
      ↓
validate-compatibility
      ↓
migration pilot or release-distribution
      ↓
cutover / rollout / rollback decision
```

For an existing catalog, start with `inventory-audit`. For a new repository, start with `architecture-design`. For a critical migration, always separate `plan` from `apply`.

## Recommended structure

```text
marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── skills/                         # canonical source
│   ├── metaskills/
│   ├── agent-workflows/
│   ├── product/
│   ├── development/
│   └── marketing/
├── plugin/                         # generated aggregate bundle
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   └── build-manifest.json
├── scripts/
├── tests/
└── README.md
```

Detailed rationale is in [references/best-practices.md](references/best-practices.md).

## Consumer commands

skill.sh / Skills CLI:

```bash
npx skills add owner/repository --list
npx skills add owner/repository --skill skill-architect --agent claude-code --agent codex
```

Claude Code marketplace:

```text
/plugin marketplace add owner/repository
/plugin install metaskills@marketplace-name
```

Claude Code CLI:

```bash
claude plugin marketplace add owner/repository
claude plugin install metaskills@marketplace-name
claude --plugin-dir ./plugin
```

Do not install the same skill through two channels into the same visibility scope.

## Built-in utilities

### Portable validation

```bash
python3 scripts/validate_marketplace.py /path/to/marketplace
python3 scripts/validate_marketplace.py /path/to/marketplace --json
```

Checks:

- allowed `skills/` depth;
- `SKILL.md`, directory name, and `metadata.version`;
- global uniqueness of names;
- unsafe local links;
- baseline marketplace and plugin manifest structure;
- existence of declared local paths.

This check does not replace official harness validators.

### Aggregate plugin build

```bash
python3 scripts/build_plugin_bundle.py /path/to/marketplace /new/staging/plugin \
  --plugin-name skill-toolkit \
  --version 1.0.0 \
  --description "Portable skill engineering toolkit"
```

The utility accepts only a new output directory, copies full skill packages, excludes standard junk (`.DS_Store`, `__pycache__`, `*.pyc`, `.git`), creates `plugin.json` and `build-manifest.json`, rejects symlinks, and does not delete existing directories.

### Eval corpus

```bash
python3 scripts/check_evals.py evals
```

It checks the integrity of routing and behavioral cases. A harness-native or independent evaluator must execute the actual cases separately.

## Full pre-release verification

```bash
python3 scripts/validate_marketplace.py .
npx skills add . --list
claude plugin validate .
claude plugin validate ./plugin --strict
claude --plugin-dir ./plugin
```

Also run trigger evals, behavior evals, upgrade verification from the previous version, and security review. If a tool is unavailable, mark the result as `NOT RUN`.

## Versions

- `SKILL.md → metadata.version` applies to one skill.
- `.claude-plugin/plugin.json → version` applies to the plugin bundle.
- marketplace entry version applies to the installable catalog offering.

Versions must not be assumed to be identical automatically. Changing installable content requires a new distribution release.

## Safety

- Treat external skills as supply-chain input.
- Inspect scripts and provenance before execution.
- Do not store secrets in skill packages, manifests, fixtures, or logs.
- Build in staging, then verify, and only then promote.
- Run a pilot before broad rollout.
- Keep the previous known-good release until the rollback window is complete.
- Publication, global installation, and removal require a separate explicit decision.

## Package contents

```text
skill-marketplace-manager/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── prompts/
├── references/
│   ├── best-practices.md
│   ├── integration-contracts.md
│   ├── manifest-patterns.md
│   └── migration-contract.md
├── scripts/
└── evals/
```

`references/best-practices.md` is the canonical runtime reference. The central `skill-best-practices` can index and update sources, but the installed skill does not depend on neighboring directories.

## Limitations

- Harness formats change; official documentation must be rechecked before release.
- The portable validator checks only cross-platform invariants.
- Real installability is confirmed only by loading a representative skill in the target harness.
- The skill does not make decisions on the user's behalf about public/private visibility, licensing, owners, or release channel.

## Quick examples

```text
Run a read-only audit of ./skills-repo and find skill.sh/Claude Code collisions.
```

```text
Design a marketplace with metaskills and development, one canonical source,
and an aggregate plugin for local testing. Provide the manifests for review.
```

```text
Create a phased migration plan for ./legacy-skills, including rollback and acceptance gates.
Do not apply changes.
```

```text
Build a candidate plugin in a new staging directory and check for drift.
Do not install or publish anything.
```

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Design, inventory, scaffold, curate, build, document, validate, migrate, release, and audit repositories that distribute Agent Skills through skill.sh-compatible catalogs and plugin harnesses such as Claude Code.
- **Version:** `1.4.2`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `marketplace`, `distribution`.

## When To Use

Marketplace topology, category design, marketplace.json or plugin.json generation, portable skills/ layouts, aggregate plugin builds, skill documentation and onboarding sets, catalog governance, version policy, compatibility checks, staged migrations, publishing plans, or repository-wide skill distribution.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/skill-marketplace-manager Inspect a read-only repository with 40 skills: find duplicate names, category depth issues, and manifest drift.
```

**Expected result:** route `the skill's primary route` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### route-inventory

- **Example request:** “Inspect a read-only repository with 40 skills: find duplicate names, category depth issues, and manifest drift.”
- **Expected route:** `the skill's primary route`.

### route-architecture

- **Example request:** “Propose a catalog structure for skill.sh and Claude Code with selective category installation.”
- **Expected route:** `the skill's primary route`.

### route-scaffold

- **Example request:** “Create a local scaffold for a new marketplace with metaskills and development categories, but do not publish it.”
- **Expected route:** `the skill's primary route`.

### route-curation

- **Example request:** “Add these three verified skills to the catalog, assign one category to each, and check for collisions.”
- **Expected route:** `the skill's primary route`.

### route-build

- **Example request:** “Build a self-contained aggregate plugin in a new staging catalog and generate hashes.”
- **Expected route:** `the skill's primary route`.

### route-documentation

- **Example request:** “Document the canonical skills and create onboarding from installation to the first verified outcome.”
- **Expected route:** `the skill's primary route`.

### route-validation

- **Example request:** “Verify whether the skills are discoverable through the skills CLI and the Claude plugin, but do not fix anything.”
- **Expected route:** `the skill's primary route`.

### route-migration-plan

- **Example request:** “Prepare a detailed plan to migrate outputs/* into the marketplace with rollback. Do not migrate anything yet.”
- **Expected route:** `the skill's primary route`.


## Expected Results

- the result matches the stated contract and clearly separates facts from assumptions;
- modified artifacts are listed, and completed checks are named without invented PASS results;
- constraints, residual risks, rollback status, and the next step are stated explicitly.

## Execution Flow

1. **Classify the request.** Execute the corresponding contract step from `SKILL.md`.
2. **Establish the operating mode.** Execute the corresponding contract step from `SKILL.md`.
3. **Run the common workflow.** Execute the corresponding contract step from `SKILL.md`.
4. **Enforce architectural invariants.** Execute the corresponding contract step from `SKILL.md`.
5. **Use deterministic helpers.** Execute the corresponding contract step from `SKILL.md`.
6. **Dispatch private documentation work.** Execute the corresponding contract step from `SKILL.md`.
7. **Apply route-specific rules.** Execute the corresponding contract step from `SKILL.md`.
8. **Coordinate with adjacent skills.** Execute the corresponding contract step from `SKILL.md`.
9. **Produce a completion report.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

Authoring one skill.

The skill must not expand the authority it received, hide skipped checks, perform irreversible or external actions without explicit permission, or claim host state solely from the presence of files.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](DONOR.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`private-skills/`](private-skills/) — internal skills available only to the owner.
- [`prompts/`](prompts/) — routing and specialist prompts.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/build_plugin_bundle.py`](scripts/build_plugin_bundle.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/validate_marketplace.py`](scripts/validate_marketplace.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
