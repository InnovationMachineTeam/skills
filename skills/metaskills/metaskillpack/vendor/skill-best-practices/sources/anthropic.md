# Anthropic — source summaries

## SRC-ANT-001 — Skill authoring best practices

Reinforces concise, structured, real-use-tested skills. Distinguishes metadata loaded at startup, SKILL.md loaded on activation, and resources loaded on demand. Adds Claude runtime considerations such as dependency availability in code execution and collaborative iteration using one agent to draft and another execution context to expose gaps.

## SRC-ANT-002 — Skills for enterprise

Treats third-party skills like production software. Requires review of all instructions, scripts, tools, MCP references, filesystem scope, network calls, credentials, redirects, and exfiltration paths. Recommends 3–5 representative trigger/non-trigger/ambiguous queries for approval, isolation and coexistence testing, separation of author and reviewer, registry ownership, pinned production versions, checksums, rollback, role-based catalogs, and periodic re-evaluation.

## SRC-ANT-003 — Using Agent Skills with the API

Describes the Claude API's current host contract: skills execute through a code-execution container, managed and custom skills share a common invocation shape, versions can be pinned, generated files have a separate lifecycle, and long operations may pause and resume. Runtime limits such as skills per request, upload size, headers, retention, and version formats are dynamic platform facts and must be refreshed rather than copied into portable rules.

## SRC-ANT-004 — Engineering article

Provides architectural rationale: general agents need procedural and organizational knowledge packaged into discoverable folders; progressive loading makes expertise composable and scalable; portability reduces repeated prompt engineering. It is conceptual evidence, not the current API or schema contract.

## SRC-ANT-005 — Claude 5 context-engineering guidance

Reports that advanced Claude 5 models benefit from fewer overlapping blanket constraints, contextual judgment, progressive disclosure, simple tool descriptions, lightweight project instructions, and high-fidelity references such as code, tests, artifacts and rubrics. This is model-generation-specific engineering guidance rather than a portable skill standard. Apply it through capability evidence: retain explicit steps, schemas and checks for simpler or unvalidated models, while keeping safety and authority invariants identical across profiles.
