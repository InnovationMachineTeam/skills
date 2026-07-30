# Integration contracts

Use specialists by ownership, not by filename overlap.

| Specialist | Owns | Marketplace manager consumes |
|---|---|---|
| `skill-architect` | behavior and resources of one skill | validated skill package |
| `skill-evaluator` | trigger and behavioral evidence | release-gate report |
| `skill-doctor` | diagnosis and repair plan for one broken skill | corrected or blocked package |
| `skill-refactor` | merge, split, extract, combine decisions | target package topology |
| `skill-manager` | installed-state lifecycle and rollback | activation/deactivation result |
| `skill-builder` | cross-specialist workflow orchestration | project-level checkpoints |

## Handoff envelope

Every handoff should state:

- requested outcome;
- exact artifact paths;
- authoritative source;
- allowed mutation scope;
- required evidence;
- blocking conditions;
- return format.

Do not ask another specialist to publish, delete, or install unless that authority was explicit in the originating request.

## Conflict resolution

When ownership overlaps:

1. preserve the current canonical source;
2. assign behavioral changes to the individual-skill specialist;
3. assign packaging and catalog changes to this skill;
4. validate both the skill and distribution artifact;
5. record which version surface each change must bump.
