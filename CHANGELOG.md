# Changelog

## 1.4.0 — 2026-07-31

- Added a typed agent asset registry, versioned capability map, transaction
  schema, deterministic Markdown views, and access-control validation.
- Added generated project-agent adapters for Codex, Claude Code, and Cursor
  with a tested owner-private walking skeleton.
- Added team-lifecycle and Agentic OS master prompts under `docs/prompts/`.
- Updated foundational metaskills for private capability placement,
  owner/accountability, agent-system evaluation, and orchestration.

## 1.2.0 — 2026-07-30

- Added the explicitly invoked `metaskillpack` composite with 19 canonical modes, nine aliases, and pinned read-only snapshots of all 12 metaskills.
- Added deterministic command routing, donor version and tree-digest checks, staged snapshot rebuilding, and no-op or blocked upgrade behavior.
- Added routing and behavior eval fixtures covering donor isolation, progressive loading, workflow selection, missing donors, same-version drift, and recursion guards.
- Added `metaskillpack` as an individually installable Claude Code, Codex, Cursor, and Agent Skills entry and upgraded the aggregate catalog to `1.2.0`.

## 1.1.0 — 2026-07-30

- Added native Codex repo marketplace metadata at `.agents/plugins/marketplace.json`.
- Added native Cursor multi-plugin metadata at `.cursor-plugin/marketplace.json`.
- Added 12 generated self-contained packages under `plugins/`, each with Claude Code, Codex, and Cursor manifests.
- Upgraded the aggregate plugin to the same three-host package layout.
- Added deterministic cross-host build, drift, metadata, path, policy, and bundle-integrity checks.
- Documented private Cursor limitations and public-publication gates.

## 1.0.0 — 2026-07-30

- Created the private `im-skills` marketplace for `InnovationMachineTeam/skills`.
- Added 12 individually installable `metaskills` entries.
- Added the generated `im-skills-all` aggregate plugin.
- Added deterministic manifest generation, bundle building, portability validation, and CI drift checks.
- Added repository governance, security, contribution, release, and private-to-public policies.
- Migrated `skill-best-practices` locators to portable forms and added `skill-marketplace-manager` to its managed portfolio; bumped that skill to `1.0.1`.
