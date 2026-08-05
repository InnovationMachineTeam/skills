# Release 3.8.0 — full command examples in skill README files

Status: repository source and generated packages validated; no external
publication, installation, activation, or production change was performed.

## Scope

- added a durable `## Full Command Example` section to all 48 canonical skill
  README files;
- public skills show a complete `/skill-name <task>` invocation;
- five package-private skills show invocation through their actual owning
  public skill and explicitly reject direct slash invocation;
- added full command examples and expected results to all six category README
  files and the canonical `skills/README.md` index;
- corrected generated private-skill ownership text so
  `skill-documentation-writer` is dispatched by `skill-marketplace-manager`;
- advanced patch versions for all changed public and private skills and advanced
  the repository marketplace and aggregate package to `3.8.0`;
- rebuilt `agentkit@1.0.2`, `metaskillpack@1.5.1`, registries, individual
  packages, aggregate package, and all three marketplace projections.

## Verification

- repository validation: PASS for 43 public skills, three marketplaces, and 43
  individual packages;
- documentation links: PASS;
- README generation: PASS for 48/48 canonical skills;
- command-example contract: PASS for all public and package-private skills;
- portable aggregate structure: PASS for 43 public and 5 package-private
  skills;
- agentkit donor lock: 10/10 current;
- metaskillpack donor lock: 12/12 current;
- unit suite: 81/81 PASS;
- `git diff --check`: PASS.

## Rollback

Before publication, restore the previous Git revision. For a released rollback,
restore marketplace `3.7.0`, agentkit `1.0.1`, metaskillpack `1.5.0`, and the
previous individual skill versions, then rebuild all projections through
staging. Do not edit installed caches or generated packages manually.
