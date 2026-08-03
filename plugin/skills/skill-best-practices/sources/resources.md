# Resource inventory

Last checked: 2026-08-03. `sources/registry.json` is canonical for automation; this file is the readable list.

Initial comparison point: `baseline-snapshot.json`. Its fingerprints represent the summarized findings recorded during the initial review, not immutable hashes of canonical pages. Refresh each canonical source before making a new “unchanged” claim.

## Open Agent Skills standard

| ID | Resource | Summary |
|---|---|---|
| SRC-AS-001 | [Specification](https://agentskills.io/specification) | Portable directory, SKILL.md, frontmatter, progressive-disclosure and validation contract. |
| SRC-AS-002 | [Best practices](https://agentskills.io/skill-creation/best-practices) | Concision, resource architecture, degrees of freedom and real-use iteration. |
| SRC-AS-003 | [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) | Description-driven discovery and positive/negative routing evaluation. |
| SRC-AS-004 | [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) | Clean-context output evaluation, assertions, human review and cost signals. |
| SRC-AS-005 | [Using scripts](https://agentskills.io/skill-creation/using-scripts) | Deterministic helpers, dependencies, actionable errors and exit codes. |
| SRC-AS-006 | [Adding skills support](https://agentskills.io/client-implementation/adding-skills-support) | Client discovery, catalog, activation, context lifecycle and progressive loading. |

Detailed summary: [open-standard.md](open-standard.md).

## Anthropic

| ID | Resource | Summary |
|---|---|---|
| SRC-ANT-001 | [Authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Claude-oriented authoring, concision, resource structure and iteration. |
| SRC-ANT-002 | [Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) | Security review, coexistence, registry, versioning, rollout and rollback. |
| SRC-ANT-003 | [Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide) | API runtime, containers, versions, upload limits and long-running continuation. |
| SRC-ANT-004 | [Engineering article](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Architectural rationale for discoverable, composable procedural context. |
| SRC-ANT-005 | [Claude 5 context engineering](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) | Model-specific guidance on judgment, progressive disclosure, lightweight instructions and rich references. |

Detailed summary: [anthropic.md](anthropic.md).

## OpenAI

| ID | Resource | Summary |
|---|---|---|
| SRC-OAI-001 | [Build skills](https://learn.chatgpt.com/docs/build-skills) | ChatGPT/Codex structure, explicit and implicit invocation, catalog budget and host metadata. |
| SRC-OAI-002 | [Build plugin skills](https://developers.openai.com/plugins/build/skills) | Author workflows as skills and distribute them with plugins. |
| SRC-OAI-003 | [Skills and MCP](https://developers.openai.com/plugins/concepts/skills) | Separate workflow instructions from live connector capabilities. |
| SRC-OAI-004 | [Optimize Metadata](https://developers.openai.com/plugins/guides/optimize-metadata) | Front-load distinctive metadata and test it in the actual catalog. |

Detailed summary: [openai.md](openai.md).

## Public exemplars

| ID | Resource | Summary |
|---|---|---|
| SRC-EX-001 | [garrytan/gstack](https://github.com/garrytan/gstack) | Operational phase protocols, gates, evidence loops and multi-host distribution. |
| SRC-EX-002 | [garrytan/gbrain](https://github.com/garrytan/gbrain) | Meta-skills, skillify productionization, resolver audits, versioning and atomic workflows. |

Detailed summary: [exemplars.md](exemplars.md).

## Local platform and derived baseline

| ID | Resource | Summary |
|---|---|---|
| SRC-LOCAL-001 | Bundled Codex `skill-creator` | Environment-dependent runtime contract; resolve in the active Codex installation before refresh. |
| SRC-DER-001 | Prior synthesized report | Historical derived baseline; not bundled and currently unavailable. |

Detailed summary: [local-and-derived.md](local-and-derived.md).
