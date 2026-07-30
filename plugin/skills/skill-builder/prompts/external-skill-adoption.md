# Scenario: external-skill-adoption

Use when the user wants to inspect, reuse, adapt, install, or upgrade from a public or third-party skill source.

1. Run `skill-harvester` `external-skill-intake` without installing or executing repository code.
2. Pin canonical source and revision; record license, attribution, dependencies, scripts, network, credentials, hooks, secrets exposure, and host assumptions.
3. Choose one disposition: reject, research, use as-is, adapt, repair, refactor, or install.
4. Route unsafe or broken candidates to `skill-doctor`; healthy adaptations to `skill-optimizer`; topology changes to `skill-refactor`; substantial host-porting to `skill-architect` when it becomes a new bundle.
5. Invoke `skill-evaluator` on the exact adopted or adapted revision. Require a fresh local suite, safe script/tool probes, routing/coexistence, behavior, security, portability, and E2E evidence; upstream claims and badges are only inputs.
6. Route failures to the appropriate mutating specialist and evaluate the new revision, not a patched in-flight run.
7. Use `skill-manager` for staged install/update, version pinning, conflicts, activation, verification, and rollback.

Never run unreviewed source scripts, hooks, installers, or dependency commands as part of read-only intake.
