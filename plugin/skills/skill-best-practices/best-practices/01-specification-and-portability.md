# Specification and portability

Practice-ID: BP-SPEC-001
Scope: portable
Status: current
Sources: SRC-AS-001, SRC-AS-006, SRC-OAI-001, SRC-ANT-003, SRC-LOCAL-001
Last-rebuilt: 2026-07-30

## Portable minimum

- Use a directory whose name matches frontmatter `name`.
- Include a root `SKILL.md` with YAML frontmatter and Markdown instructions.
- Keep `name` within 64 lowercase alphanumeric/hyphen characters, without leading, trailing, or consecutive hyphens.
- Keep `description` non-empty and within 1024 characters; state what the skill does and when it applies.
- Use `scripts/`, `references/`, and `assets/` only when they serve distinct reusable roles.
- Use relative paths and avoid dependence on the invocation working directory.

The open standard also permits `license`, `compatibility`, `metadata`, and experimental `allowed-tools`. Treat support as client-dependent. For the strictest cross-host source, keep `name` and `description` portable and place UI, dependencies, policy, versions, and governance in target adapters or registries.

## Progressive disclosure

Design for catalog metadata → activated SKILL.md → on-demand resources. Keep the main instructions under roughly 500 lines and 5,000 tokens unless evidence justifies more. Link critical resources directly from SKILL.md and avoid deep reference chains.

## Source and runtime separation

Keep development evals, reports, snapshots, and workspaces separable from a minimal published runtime bundle when the target host prefers a lean package. Strict producers should validate; importers may diagnose or normalize non-critical deviations without silently changing source identity.

## Portability proof

Declare runtime, OS, packages, network, tools, and host assumptions. Test every claimed host rather than inferring portability from syntax alone. Track target-specific hashes and do not rely on collision or shadowing semantics.
