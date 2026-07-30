# Portability and Packaging Optimization Prompt

Apply after [base.md](base.md). Make claimed host and installation compatibility explicit and verifiable.

## Diagnose

- Inventory frontmatter, host metadata, invocation syntax, paths, operating systems, runtimes, tools, dependencies, permissions, hooks, and unsupported extensions.
- Reproduce failures on each claimed host or reduce the claim when testing is unavailable.

## Optimize

- Choose portable core, host-optimized, or dual profile.
- Isolate host extensions in supported locations and keep common behavior in `SKILL.md`.
- Normalize paths and dependency declarations without inventing metadata.
- Remove generated junk, empty resources, stale files, and accidental secrets.

## Guardrails

Do not claim portability from valid YAML alone. Preserve host-specific performance when creating a portable core, or document the deliberate tradeoff. Validate install, discovery, invocation, resources, and execution separately.

