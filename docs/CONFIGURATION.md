# Configuration

The repository has no runtime `.env` contract and does not embed credentials.
Configuration is committed as reviewable JSON/YAML/Markdown and host manifests.

## Canonical configuration

| Path | Purpose | Edit policy |
|---|---|---|
| `catalog/entries.json` | installable skill inventory and tags | canonical |
| `catalog/dependencies.json` | required/recommended skill graph | canonical |
| `catalog/release.json` | publisher, categories, aggregate release | canonical |
| `docs/AGENT-ASSET-REGISTRY.json` | typed agent/skill/team inventory | canonical, transactional |
| `docs/AGENT-SKILLS-MAP.json` | versioned capability bindings | canonical, transactional |
| `.claude-plugin/marketplace.json` | Claude marketplace view | generated |
| `.agents/plugins/marketplace.json` | Codex marketplace view | generated |
| `.cursor-plugin/marketplace.json` | Cursor marketplace view | generated |
| `plugin/`, `plugins/` | aggregate and individual packages | generated |

## Agent-project configuration

Project-scoped agents live below `.agents/definitions/`. An exact definition
declares identity, version, mission, permissions, model policy, capability
budget, document contract, lifecycle, and evaluation evidence. Owner-private
skills and commands live inside the owning agent directory and are excluded
from marketplace packaging.

## Model, tool, and policy pinning

Released runs pin exact agent, workflow, prompt, skill, model, tool, and policy
versions. Durable roles define required model properties; current provider/model
recommendations are produced by `agent-model-selector` and re-evaluated before
change.

## Secrets and external services

Credentials, API keys, signing material, and production endpoints are never
committed to skill packages or documentation. Host authentication, policy
enforcement, credential brokering, graph/vector databases, and other external
services require a separate approved setup and operating contract.

## Generated-artifact rule

Never edit `plugin/`, `plugins/`, or marketplace manifests directly. Change
canonical sources, stage a rebuild, validate, review the diff, and then replace
the committed generated artifacts.
