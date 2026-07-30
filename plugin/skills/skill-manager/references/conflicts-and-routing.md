# Conflicts and Routing

## Contents

- Conflict types
- Resolution
- Routing validation

## Conflict types

- same name and identical content;
- same name and divergent content;
- different names with overlapping descriptions;
- intentional higher-precedence override;
- stale installed copy versus source copy;
- skill/plugin or host-builtin collision;
- namespace and invocation ambiguity.

## Resolution

Do not automatically delete a loser. Determine actual precedence, ownership, consumers, and desired identity. Options include namespace, rename, disable, quarantine, consolidate, version pin, or explicit host configuration.

Renaming changes invocation and may break references. Consolidation changes behavior and belongs with `skill-architect`, `skill-refactor`, or `skill-optimizer` according to the boundary change. Broken or unsafe copies belong with doctor before activation.

## Routing validation

Test direct, paraphrased, adjacent negative, ambiguous, collision, and explicit-invocation cases. Verify actual host selection rather than relying on description inspection alone.
