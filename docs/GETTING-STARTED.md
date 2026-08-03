# Getting Started

## Prerequisites

- Git access to the public `InnovationMachineTeam/skills` repository;
- the target host: Claude Code, Codex, Cursor, or another Agent Skills client;
- Python 3 for repository dependency, build, and validation helpers;
- Node.js/npx only for Skills CLI checks or installation.

Host CLIs are optional unless that host is being installed or validated.

## Choose an entry

- `agent-master`: governed Agent Harness factory from process description through orchestrator, role agents, skills, implementation and validation;
- `agentkit`: explicit one-agent lifecycle toolkit;
- `agent-team-manager`: assess and govern team lifecycles;
- `agent-os-architect`: assess and design an Agentic OS;
- `metaskillpack`: explicit skill-engineering toolkit.

See [ONBOARDING.md](ONBOARDING.md) before choosing a team or Agentic OS.

## Install one skill

### Claude Code

```text
/plugin marketplace add InnovationMachineTeam/skills
/plugin install agentkit@im-skills
```

### Codex

```bash
codex plugin marketplace add InnovationMachineTeam/skills
codex plugin add agentkit@im-skills
codex plugin list --json
```

### Cursor

```bash
npx skills add InnovationMachineTeam/skills --skill agentkit --agent cursor
```

Replace `agentkit` with an entry from the root catalogue.

## Check dependencies

```bash
python3 scripts/manage_skill_dependencies.py plan agent-team-manager --host codex
python3 scripts/manage_skill_dependencies.py check agent-team-manager --host codex
```

Add `--execute` to the dependency-aware install command only after reviewing the
plan. Claude Code can install declared same-marketplace required dependencies;
Codex and Cursor use the explicit dependency-first path.

## First use

```text
Use agent-master to build a private Agent Harness for this process on supervised
autopilot. Create the minimum sufficient orchestrator, role agents, role skills,
tools, evals and documentation, but stop before installation or activation.

agentkit help
agentkit status
agentkit run Design one agent that maintains ADR review evidence for this repo.
```

Or start a team assessment without authorizing a build:

```text
Use agent-team-manager to assess whether this task needs one agent or a team.
Return alternatives, roles, required skills, documents, and approval gates. Do
not build or activate anything.
```

## Common setup issues

| Problem | Resolution |
|---|---|
| Public repository cannot be resolved | Verify network access and the repository locator before invoking the host |
| A route reports a missing companion | Run the dependency plan and install the declared companion |
| Duplicate behavior or triggers | Use one installation channel per skill and scope |
| Cursor native marketplace entry is unavailable | Use Skills CLI directly from the public repository; native publication requires separate Cursor review |
| An installed skill is not active | Verify host read-back; installation and activation are separate states |

## Next steps

- [Onboarding and use cases](ONBOARDING.md)
- [Configuration](CONFIGURATION.md)
- [Development](DEVELOPMENT.md)
- [Testing](TESTING.md)
