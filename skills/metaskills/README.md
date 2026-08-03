# Skill-Engineering Metaskills

Use these skills to discover, research, create, evaluate, diagnose, optimize,
refactor, govern, package, and release skills.

- prefer a direct `skill-*` specialist for one known phase;
- use `skill-builder` when the correct multi-stage workflow must be inferred;
- use explicit `metaskillpack` for the version-locked composite command surface;
- keep donor skills read-only inside composite packs;
- stage and evaluate replacements before promotion;
- use `skill-marketplace-manager` for distribution rather than mixing packaging
  into skill creation.

## Full command examples

These are illustrative commands; adapt target paths, visibility, and acceptance
criteria to the current repository.

```text
/skill-builder Create a private skill that audits API migration plans, includes positive and negative routing cases, and returns a verification-ready skill package
```

Expected result: a governed multi-stage skill workflow with an explicit
architecture, implementation artifacts, evaluations, and lifecycle handoff.

```text
/skill-doctor Diagnose why skills/development/api-migration-auditor triggers on implementation requests and apply the smallest safe fix
```

Expected result: a severity-ranked diagnosis, minimal authorized repair, and
regression evidence without unrelated redesign.

```text
/skill-marketplace-manager Move api-migration-auditor into the development category, rebuild all marketplace projections in staging, validate portability, and prepare a rollback record without publishing
```

Expected result: synchronized canonical metadata and verified staged packages;
publication and installation remain separate transitions.

Agent creation belongs to `agent-skills/`; team work belongs to
`agent-team-skills/`; Agentic OS belongs to `agent-os-skills/`.
