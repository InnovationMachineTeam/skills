# Release 3.6.0 — Private Skill Documentation Writer

Status: **validated repository candidate; no host activation or external publication performed**.

## Scope

- adds package-private `skill-documentation-writer@1.0.0` under `skill-marketplace-manager`;
- adds the parent `documentation` route for skill README files, marketplace onboarding guides and documentation audits;
- updates `skill-marketplace-manager` to `1.4.0` and `metaskillpack` to `1.5.0`;
- keeps the private specialist out of public catalog entries and host discovery metadata;
- teaches the metaskillpack snapshot builder to rename nested private `SKILL.md` contracts to `DONOR.md` and rewrite their links;
- rebuilds 43 individual packages and `im-skills-all@3.6.0`.

## Verification

- repository validation: PASS for 43 public skills, three marketplace projections and 43 individual plugins;
- portable staging validation: PASS for 43 public skills and five package-private subskills;
- documentation links: PASS for 118 canonical files;
- parent and private routing/behavior corpus: PASS, 28 cases;
- complete unit suite: PASS, 80/80 tests.

## Authority and lifecycle

The release changes repository source and generated packages only. It does not install, activate, publish, deploy or grant credentials. `skill-marketplace-manager` remains the only allowed consumer of the private documentation skill and retains catalog, version, packaging and release authority.

## Rollback

Revert this release commit to restore marketplace release `3.5.1`, `skill-marketplace-manager@1.3.1`, and `metaskillpack@1.4.1`. No external state needs compensation because no host or publication transition was executed.
