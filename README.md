# IM Skills

Private Agent Skills marketplace maintained by **InnovationMachineTeam** for **InnovationMachine**.

- Marketplace: `im-skills`
- Repository: `InnovationMachineTeam/skills`
- Category: `metaskills`
- Entries: one installable entry per skill
- Aggregate local plugin: `im-skills-all`
- Current visibility: private
- Lead maintainer and required reviewer: [@stanislavus86](https://github.com/stanislavus86)

## Install with Claude Code

Private repository access must already work for the current GitHub identity.

Interactive commands:

```text
/plugin marketplace add InnovationMachineTeam/skills
/plugin install skill-architect@im-skills
```

CLI equivalents:

```bash
claude plugin marketplace add InnovationMachineTeam/skills
claude plugin install skill-architect@im-skills
```

Replace `skill-architect` with any entry from the catalog below. Each entry installs exactly one skill.

## Install with Skills CLI / skill.sh

List repository skills:

```bash
npx skills add InnovationMachineTeam/skills --list
```

Install one skill for selected agents:

```bash
npx skills add InnovationMachineTeam/skills \
  --skill skill-architect \
  --agent claude-code \
  --agent codex
```

Do not activate the same skill through both marketplace and Skills CLI in the same host scope. Choose one channel per skill and scope.

## Test the complete toolkit locally

The committed `plugin/` directory is generated from canonical `skills/`:

```bash
claude --plugin-dir ./plugin
```

The aggregate plugin is intended for local integration testing and full-toolkit development. Individual marketplace entries remain the supported selective-install path.

## Catalog

| Entry | Purpose | Version |
|---|---|---|
| `optimize-master-prompts` | Design and improve durable controlling prompts | 1.0.0 |
| `skill-architect` | Classify and create skill architectures | 1.0.0 |
| `skill-best-practices` | Maintain an evidence-linked practices corpus | 1.0.1 |
| `skill-builder` | Orchestrate end-to-end skill workflows | 1.0.0 |
| `skill-doctor` | Diagnose and repair unhealthy skills | 1.0.0 |
| `skill-evaluator` | Design and run skill evaluations | 1.0.0 |
| `skill-harvester` | Extract reusable skill components and evidence | 1.0.0 |
| `skill-manager` | Govern installed skill lifecycle | 1.0.0 |
| `skill-marketplace-manager` | Design and operate skill marketplaces | 1.0.0 |
| `skill-optimizer` | Improve healthy skills with measured evidence | 1.0.0 |
| `skill-refactor` | Merge, split, extract, and reshape capabilities | 1.0.0 |
| `skill-scout` | Discover and prioritize skill opportunities | 1.0.0 |

The source of truth for versions is each skill's `SKILL.md → metadata.version`. Marketplace entry versions are generated from those values.

## Repository structure

```text
.
├── .claude-plugin/marketplace.json   # generated individual entries
├── catalog/
│   ├── entries.json                  # tags and declared entry inventory
│   └── release.json                  # governance and aggregate release config
├── skills/metaskills/                # canonical source of truth
├── plugin/                           # generated aggregate Claude Code plugin
├── scripts/                          # deterministic generation and validation
├── docs/
└── .github/workflows/validate.yml
```

Never edit `plugin/` or `.claude-plugin/marketplace.json` manually. Change canonical skills or catalog configuration, regenerate, validate, and review the resulting diff.

## Development workflow

1. Edit the canonical package under `skills/metaskills/<name>/`.
2. Bump that skill's `metadata.version` according to SemVer.
3. Regenerate individual marketplace entries:

   ```bash
   python3 scripts/generate_marketplace.py .
   ```

4. Rebuild the aggregate plugin into a new staging directory:

   ```bash
   python3 scripts/build_aggregate.py . build/im-skills-all
   ```

5. Replace the committed `plugin/` only after the staged candidate passes validation.
6. Run:

   ```bash
   python3 scripts/validate_repository.py .
   python3 scripts/validate_marketplace.py .
   npx skills add . --list
   claude plugin validate .
   claude plugin validate ./plugin --strict
   ```

7. Obtain review from `@stanislavus86` before release.

## Version policy

- Individual skill and marketplace entry: the skill's `metadata.version`.
- Aggregate plugin: independent SemVer in `catalog/release.json`.
- Marketplace metadata: repository catalog format version, currently `1.0.0`.

Bump an individual skill version whenever its installed contents or contract change. Bump the aggregate plugin when any bundled skill or aggregate install contract changes. A release is blocked if generated manifests or bundle hashes drift from canonical sources.

## Governance and security

- GitHub repository owner and technical publisher: **InnovationMachineTeam**.
- Product/company steward: **InnovationMachine**.
- Lead maintainer and required reviewer: **@stanislavus86**.
- Security contact: `stanislav.usoltsev@gmail.com`.

See [GOVERNANCE.md](GOVERNANCE.md), [SECURITY.md](SECURITY.md), and [CONTRIBUTING.md](CONTRIBUTING.md).

## Private-to-public roadmap

The first release remains private. Public release requires a licensing decision, removal of confidential material and private locators, provenance review, security review, fresh-install testing without organization credentials, and an explicit visibility change. See [docs/PRIVATE-TO-PUBLIC.md](docs/PRIVATE-TO-PUBLIC.md).
