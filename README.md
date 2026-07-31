# IM Skills

Private Agent Skills marketplace maintained by **InnovationMachineTeam** for **InnovationMachine**.

- Marketplace: `im-skills`
- Repository: `InnovationMachineTeam/skills`
- Categories: `agent-os-skills`, `agent-team-skills`, `agent-skills`, `metaskills`, `prompt-skills`
- Entries: one installable cross-host plugin per skill
- Supported hosts: Claude Code, Codex, Cursor, and Agent Skills clients
- Aggregate local plugin: `im-skills-all` (`3.2.2`)
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

## Install with Codex

Add the private repository as a repo marketplace, then install one entry:

```bash
codex plugin marketplace add InnovationMachineTeam/skills
codex plugin add skill-architect@im-skills
```

Use `codex plugin marketplace list` and `codex plugin list --json` to verify the resolved marketplace and installed package. Repository access must already work for the current Git identity.

## Use with Cursor

During the private phase, use the Agent Skills channel for installation:

```bash
npx skills add InnovationMachineTeam/skills \
  --skill skill-architect \
  --agent cursor
```

The repository also contains Cursor-native `.cursor-plugin/plugin.json` files and a root `.cursor-plugin/marketplace.json`. They are kept ready for local testing and later Cursor Marketplace submission. Cursor's publication flow requires a public Git repository, so native marketplace publication remains intentionally disabled while this repository is private.

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
  --agent codex \
  --agent cursor
```

Do not activate the same skill through both marketplace and Skills CLI in the same host scope. Choose one channel per skill and scope.

## Install skills with companions

Claude Code supports native same-marketplace plugin dependencies and installs
them with the requested plugin. Codex and Cursor do not use that manifest
contract. The repository therefore keeps one portable source of truth in
`catalog/dependencies.json`, projects it into Claude manifests, generates
warnings for every affected package, and provides a dependency-aware fallback
installer.

Preview a complete dependency-first plan without changing installed state:

```bash
python3 scripts/manage_skill_dependencies.py plan skill-builder --host codex
```

Install the required companion plugins and the requested plugin together:

```bash
python3 scripts/manage_skill_dependencies.py install skill-builder --host codex --execute
```

Check the currently enabled Codex plugins and print a visible warning when a
required companion is missing or too old:

```bash
python3 scripts/manage_skill_dependencies.py check skill-builder --host codex
```

`--include-recommended` opts into recommended companions. Without `--execute`,
the install command is a dry run. The helper never embeds duplicate copies of a
companion skill into individual plugins.

## Test the complete toolkit locally

The committed `plugin/` directory is a generated aggregate package with Claude Code, Codex, and Cursor manifests:

```bash
claude --plugin-dir ./plugin
```

The aggregate plugin is intended for local integration testing and full-toolkit development. Individual marketplace entries remain the supported selective-install path. For Codex, use the repo marketplace rather than loading the aggregate directly; for Cursor, use the individual package or Agent Skills flow.

## Catalog

| Entry | Category | Purpose | Version |
|---|---|---|---|
| `agent-architect` | `agent-skills` | Design one bounded agent or subagent definition | 1.0.0 |
| `agent-best-practices` | `agent-skills` | Query and govern evidence-linked agent practices | 1.0.0 |
| `agent-builder` | `agent-skills` | Orchestrate one-agent lifecycle workflows | 1.0.0 |
| `agent-context` | `agent-skills` | Build provenance-bearing agent design context | 1.0.0 |
| `agent-doctor` | `agent-skills` | Diagnose and minimally repair one agent | 1.0.0 |
| `agent-evaluator` | `agent-skills` | Independently evaluate one frozen agent | 1.0.0 |
| `agent-knowledge-manager` | `agent-skills` | Curate and retrieve provenance-bearing project knowledge | 1.0.0 |
| `agent-manager` | `agent-skills` | Govern one agent lifecycle | 1.0.0 |
| `agent-model-selector` | `agent-skills` | Evaluate and recommend evidence-backed model policies | 1.0.0 |
| `agent-observer` | `agent-os-skills` | Validate traces, SLOs, alerts, and bounded diagnostics | 1.0.0 |
| `agent-os-architect` | `agent-os-skills` | Design the minimum justified Agentic OS | 1.0.0 |
| `agent-os-bootstrapper` | `agent-os-skills` | Stage an approved Agentic OS walking skeleton | 1.0.0 |
| `agent-os-evaluator` | `agent-os-skills` | Independently evaluate frozen Agentic OS candidates | 1.0.0 |
| `agent-policy-manager` | `agent-os-skills` | Govern pinned authorization and approval decisions | 1.0.0 |
| `agent-registry-manager` | `agent-os-skills` | Reconcile typed desired and observed asset state | 1.0.0 |
| `agent-runtime-manager` | `agent-os-skills` | Govern durable platform task and run lifecycle | 1.0.0 |
| `agent-optimizer` | `agent-skills` | Improve one healthy agent against a frozen metric | 1.0.0 |
| `agent-refactor` | `agent-skills` | Refactor agent boundaries and migrations | 1.0.0 |
| `agent-scout` | `agent-skills` | Discover and prioritize justified agent opportunities | 1.0.0 |
| `agent-skill-mapper` | `agent-skills` | Map governed capabilities to registered agents | 1.0.0 |
| `agent-team-architect` | `agent-team-skills` | Design justified agent teams and versioned specifications | 1.1.0 |
| `agent-team-builder` | `agent-team-skills` | Stage approved agent-team specifications safely | 1.0.0 |
| `agent-team-manager` | `agent-team-skills` | Govern agent-team lifecycle workflows and run state | 1.2.0 |
| `agent-team-orchestrator` | `agent-team-skills` | Execute approved team task graphs with bounded runtime state | 1.0.0 |
| `agent-workspace-manager` | `agent-team-skills` | Govern isolated worktrees and integration handoffs | 1.0.0 |
| `metaskillpack` | `metaskills` | Run the complete metaskill toolkit from one explicit command | 1.4.0 |
| `prompt-optimize` | `prompt-skills` | Design and improve durable controlling prompts | 3.0.0 |
| `skill-architect` | `metaskills` | Classify and create skill architectures | 1.2.0 |
| `skill-best-practices` | `metaskills` | Maintain an evidence-linked practices corpus | 1.2.0 |
| `skill-builder` | `metaskills` | Orchestrate end-to-end skill workflows | 1.4.0 |
| `skill-doctor` | `metaskills` | Diagnose and repair unhealthy skills | 1.0.0 |
| `skill-evaluator` | `metaskills` | Design and run skill evaluations | 1.1.0 |
| `skill-harvester` | `metaskills` | Extract reusable skill components and evidence | 1.1.0 |
| `skill-manager` | `metaskills` | Govern installed skill lifecycle | 1.2.0 |
| `skill-marketplace-manager` | `metaskills` | Design and operate skill marketplaces | 1.3.0 |
| `skill-optimizer` | `metaskills` | Improve healthy skills with measured evidence | 1.0.0 |
| `skill-refactor` | `metaskills` | Merge, split, extract, and reshape capabilities | 1.2.0 |
| `skill-scout` | `metaskills` | Discover and prioritize skill opportunities | 1.1.0 |

The source of truth for versions is each skill's `SKILL.md → metadata.version`. Marketplace entry versions are generated from those values.

## Repository structure

```text
.
├── .claude-plugin/marketplace.json   # Claude Code marketplace
├── .agents/plugins/marketplace.json  # Codex repo marketplace
├── .cursor-plugin/marketplace.json   # Cursor multi-plugin marketplace
├── catalog/
│   ├── entries.json                  # tags and declared entry inventory
│   ├── dependencies.json             # canonical companion-skill graph
│   └── release.json                  # governance and aggregate release config
├── skills/                           # canonical source of truth
│   ├── agent-os-skills/              # Agentic OS plane capabilities
│   ├── agent-team-skills/            # team design and execution
│   ├── agent-skills/                 # reusable single-agent capabilities
│   ├── metaskills/                   # skill engineering and orchestration
│   └── prompt-skills/                # prompt engineering capabilities
├── candidates/agentkit/              # non-discoverable 0.2 promotion candidate
├── plugins/<skill>/                  # generated per-skill cross-host packages
├── plugin/                           # generated aggregate cross-host package
├── scripts/                          # deterministic generation and validation
├── docs/
│   ├── AGENT-ASSET-REGISTRY.json     # canonical typed asset inventory
│   ├── AGENT-SKILLS-MAP.json         # versioned capability bindings
│   ├── HOST-CONFORMANCE.md            # Codex/Claude/Cursor adapter contract
│   ├── AGENT-METASKILLS-ANALYSIS.md # applying metaskill patterns to agents
│   ├── AGENT-TEAM-AND-AGENT-OS-PLAN.md # approved phased implementation plan
│   └── prompts/                     # reusable agent-oriented skill prompts
├── tests/fixtures/agent-assets/      # public/private walking skeleton
└── .github/workflows/validate.yml
```

Never edit `plugin/`, `plugins/`, or platform marketplace manifests manually. Change canonical skills or catalog configuration, regenerate, validate, and review the resulting diff.

`candidates/` is a review and evaluation surface, not an installation root.
Candidate bundles must not appear in `catalog/entries.json`, generated plugins,
marketplaces or host discovery until their documented promotion gate passes.

The agent-oriented portfolio analysis and reusable creation prompts are
documented in [docs/AGENT-METASKILLS-ANALYSIS.md](docs/AGENT-METASKILLS-ANALYSIS.md)
and [docs/prompts/README.md](docs/prompts/README.md). These are design inputs, not
active agent definitions or automatically installed skills.

The approved registry, team, model-selection, knowledge, and Agent OS roadmap is
in [docs/AGENT-TEAM-AND-AGENT-OS-PLAN.md](docs/AGENT-TEAM-AND-AGENT-OS-PLAN.md).
The implemented foundation is described in
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and
[docs/HOST-CONFORMANCE.md](docs/HOST-CONFORMANCE.md).

## Development workflow

1. Edit the canonical package under `skills/<category>/<name>/`.
2. Bump that skill's `metadata.version` according to SemVer.
3. Validate and render companion dependency references:

   ```bash
   python3 scripts/manage_skill_dependencies.py validate
   python3 scripts/manage_skill_dependencies.py render
   ```

4. Rebuild individual cross-host plugin packages into a new staging directory:

   ```bash
   python3 scripts/build_individual_plugins.py . build/plugins
   ```

5. Regenerate all three marketplace manifests:

   ```bash
   python3 scripts/generate_marketplace.py .
   ```

6. Rebuild the aggregate plugin into a new staging directory:

   ```bash
   python3 scripts/build_aggregate.py . build/im-skills-all
   ```

7. Replace committed generated directories only after staged candidates pass validation.
8. Run:

   ```bash
   python3 scripts/validate_repository.py .
   python3 scripts/validate_marketplace.py .
   python3 scripts/manage_agent_assets.py validate .
   python3 scripts/generate_agent_adapters.py tests/fixtures/agent-assets --check
   python3 -B -m unittest discover -s tests -p 'test_*.py' -v
   npx skills add . --list
   claude plugin validate .
   claude plugin validate ./plugin --strict
   codex plugin marketplace add .
   codex plugin list --available --json
   ```

9. Run the Codex plugin validator against `plugin/` and every directory under `plugins/`. Validate Cursor paths and manifests with the repository validator, then locally test a representative plugin before public submission.
10. Obtain review from `@stanislavus86` before release.

## Version policy

- Individual skill and marketplace entry: the skill's `metadata.version`.
- Aggregate plugin: independent SemVer in `catalog/release.json`.
- Marketplace metadata: repository catalog release version, currently `3.2.2`.

Bump an individual skill version whenever its installed contents or contract change. Bump the aggregate plugin when any bundled skill or aggregate install contract changes. A release is blocked if generated manifests or bundle hashes drift from canonical sources.

## Governance and security

- GitHub repository owner and technical publisher: **InnovationMachineTeam**.
- Product/company steward: **InnovationMachine**.
- Lead maintainer and required reviewer: **@stanislavus86**.
- Security contact: `stanislav.usoltsev@gmail.com`.

See [GOVERNANCE.md](GOVERNANCE.md), [SECURITY.md](SECURITY.md), and [CONTRIBUTING.md](CONTRIBUTING.md).

## Private-to-public roadmap

The first release remains private. Public release requires a licensing decision, removal of confidential material and private locators, provenance review, security review, fresh-install testing without organization credentials, and an explicit visibility change. See [docs/PRIVATE-TO-PUBLIC.md](docs/PRIVATE-TO-PUBLIC.md).
