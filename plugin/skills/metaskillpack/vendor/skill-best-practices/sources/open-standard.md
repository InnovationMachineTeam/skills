# Open Agent Skills standard — source summaries

## SRC-AS-001 — Specification

Defines the portable minimum: a skill directory with `SKILL.md`; required `name` and `description`; optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`; optional `scripts/`, `references/`, and `assets/`. Establishes name/description limits, directory-name matching, relative references, progressive disclosure, a recommended sub-500-line instruction file, and strict validation. Watch for schema changes, optional-field status, limits, and validator behavior.

## SRC-AS-002 — Best practices

Emphasizes that context is shared, so core instructions should stay concise and detailed material should load on demand. Recommends matching instruction specificity to task fragility, using concrete workflows and examples, and iterating from actual use rather than adding generic advice. Watch for revised size guidance and resource-layout recommendations.

## SRC-AS-003 — Optimizing descriptions

Treats `description` as the primary activation interface. A good description names the capability and realistic trigger context without becoming broad enough to steal unrelated tasks. Recommends positive and difficult negative cases and iterative measurement rather than intuition-only editing. Watch for updated optimization methods and dataset guidance.

## SRC-AS-004 — Evaluating skills

Separates skill output quality from mere activation. Evaluation should use realistic tasks in clean context, objective assertions where possible, human review for subjective qualities, and resource evidence such as tokens and duration. Test agents should not receive hidden expected answers. Watch for new grader formats and platform-neutral harness guidance.

## SRC-AS-005 — Using scripts

Recommends bundled scripts for repeatable deterministic work and direct package runners for existing tools when runtime policy allows. Agent-facing scripts should document dependencies, validate inputs, produce actionable errors, and use meaningful exit codes. Watch for security and dependency-isolation changes.

## SRC-AS-006 — Adding skills support

Explains three-tier client loading: catalog metadata, activated instructions, then on-demand resources. Clients must choose bounded discovery and a content-access mechanism appropriate to local, cloud, or sandboxed operation. Watch for standard discovery locations, precedence, diagnostics, and context-lifecycle changes.
