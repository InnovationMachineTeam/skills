# Vendored Composite Skillpack Master Prompt

Use this prompt when one explicitly invoked skill must package several independently maintained skills for offline, pinned, or single-entry distribution. This is a deliberate exception to the usual preference for a thin router plus separately installed specialists.

## Architecture

- Keep discovery metadata and the root `SKILL.md` focused on explicit invocation and routing.
- Vendor each donor under an isolated path and load only the selected donor contract and resources.
- Maintain a machine-readable lock with donor name, version, deterministic tree digest, source locator, vendored path, and exposed modes.
- Preserve each donor's authority, safety, validation, and completion rules. The composite adds no permission.
- Separate native control modes such as `help`, `route`, `status`, and `upgrade` from donor modes.
- Prevent recursive routing, ambiguous fallback, and collision with separately installed donors.

## Upgrade design

- Treat donor sources as immutable and untrusted supply-chain inputs.
- Compare both semantic version and a full tree digest, including scripts.
- Stop on missing, invalid, or ambiguous donors before synthesis.
- Rebuild into a fresh staging directory, update only interface-dependent control files, validate, then promote atomically.
- A current lock produces an evidence-backed no-op.

## Evaluation

Test every command and alias, direct-specialist collision negatives, progressive loading, unavailable snapshots, donor handoff cycles, no-op and changed upgrades, same-version digest drift, missing donors, staged promotion, rollback, and cross-host packaging. Measure false activation as well as missed explicit commands.

This prompt is a candidate extension for `skill-architect`; it lives here because the current task forbids modifying donor skills.
