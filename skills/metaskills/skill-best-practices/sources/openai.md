# OpenAI — source summaries

## SRC-OAI-001 — Build skills

Defines the current ChatGPT/Codex authoring surface on top of the open standard. Supports explicit mention and implicit description matching, optional `agents/openai.yaml`, and plugin distribution. Codex budgets the initial skill catalog and may shorten or omit descriptions in large catalogs, so key differentiators and trigger terms should be front-loaded. Host-specific budget values and invocation UI are dynamic facts.

## SRC-OAI-002 — Build plugin skills

Positions skills as reusable workflows and plugins as the distribution package for skills plus connectors and optional UI. The reusable workflow should stay separable from packaging and live integrations. Testing must cover both skill behavior and the plugin surface where distributed.

## SRC-OAI-003 — Skills and MCP

Separates procedural instruction from capability: skills explain how and when to perform work; MCP servers expose authenticated tools and live data. Permissions, connection policy, and tool enforcement belong to the host and connector layer rather than relying only on prose in SKILL.md.

## SRC-OAI-004 — Optimize Metadata

Metadata must quickly communicate the distinct use case in the context where users and models choose among neighboring capabilities. Front-load discriminating terms, avoid vague or duplicative labels, and validate metadata in the real catalog rather than reviewing it in isolation.
