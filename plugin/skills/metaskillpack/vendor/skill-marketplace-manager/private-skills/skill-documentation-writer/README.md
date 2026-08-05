# skill-documentation-writer

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Creates, updates, and audits evidence-backed skill documentation and marketplace onboarding artifacts when dispatched by skill-marketplace-manager with exact canonical sources, audiences, output roots, and mutation authority.
- **Version:** `1.0.2`.
- **Visibility:** package-private: invoked only by its parent `skill-marketplace-manager` and not published separately.

## When To Use

Use the skill when the request matches its purpose and responsibility boundaries in `SKILL.md`.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

This package-private skill is not invoked directly. The illustrative request is passed through its parent `/skill-marketplace-manager`:

```text
/skill-marketplace-manager skill-marketplace-manager dispatches exact canonical paths and asks for README documentation covering use cases and expected results.
```

**Expected result:** route `skill-documentation` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.
Direct `/skill-documentation-writer` is not a supported public command; parent `skill-marketplace-manager` must pass a bounded dispatch contract and verify the result.

## Usage Variants

### owner-skill-docs

- **Example request:** “skill-marketplace-manager dispatches exact canonical paths and asks for README documentation covering use cases and expected results.”
- **Expected route:** `skill-documentation`.

### owner-onboarding

- **Example request:** “skill-marketplace-manager dispatches the private marketplace manifest, target Codex users, and an approved path for an install-to-first-success onboarding guide.”
- **Expected route:** `marketplace-onboarding`.

### owner-audit

- **Example request:** “skill-marketplace-manager requests a read-only audit of stale versions, broken links, unsupported commands, and missing expected outcomes in skill documentation.”
- **Expected route:** `documentation-audit`.


## Expected Results

### evidence-backed-readme

For request “Document one skill from SKILL.md, routing evals, behavior evals and its scripts.”, the result must:

- preserves handcrafted content;
- includes realistic usage scenarios;
- pairs every scenario with observable expected results;
- links runtime rules to SKILL.md;
- labels examples separately from executions.

### onboarding-first-success

For request “Create onboarding for a private marketplace used by new Codex users.”, the result must:

- states access and authentication assumptions;
- covers discovery and package selection;
- provides a low-risk first-success task;
- defines verification and recovery;
- covers updates rollback support and limitations.

### conflicting-sources

For request “The generated plugin says version 2.0.0 while canonical SKILL.md says 1.4.0.”, the result must:

- treats canonical source as authoritative;
- reports projection drift;
- routes packaging repair to the parent.

### missing-dispatch-authority

For request “Create all onboarding files; no owner, output root, audience, or write authority is provided.”, the result must:

- returns BLOCKED_DOCUMENTATION_HANDOFF;
- lists missing dispatch fields;
- does not write files.


## Execution Flow

1. **Verify the parent dispatch.** Execute the corresponding contract step from `SKILL.md`.
2. **Select one primary mode.** Execute the corresponding contract step from `SKILL.md`.
3. **Build an evidence inventory.** Execute the corresponding contract step from `SKILL.md`.
4. **Write skill documentation.** Execute the corresponding contract step from `SKILL.md`.
5. **Write marketplace onboarding.** Execute the corresponding contract step from `SKILL.md`.
6. **Update without erasing authorship.** Execute the corresponding contract step from `SKILL.md`.
7. **Verify the artifacts.** Execute the corresponding contract step from `SKILL.md`.
8. **Return the handoff.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Use skill-documentation-writer directly to rewrite every README in my repository.” → `skill-marketplace-manager`.
- “Write end-user documentation for my accounting web application.” → `product-documentation`.
- “Redesign the trigger and workflow of this SQL analysis skill.” → `skill-architect`.

Critical anti-results:

- invents installation success;
- rewrites skill behavior;
- duplicates the full runtime prompt;
- uses real credentials;
- claims organization-wide access from author access;
- marks unavailable host checks PASS;
- silently documents version 2.0.0;
- edits the generated package directly;
- scans broad roots;
- assumes publication authority.

## Dependencies

There are no external catalog dependencies. Parent `skill-marketplace-manager` passes only a bounded dispatch envelope to this private skill and verifies its result.

## Package Resources

- [`SKILL.md`](DONOR.md) — executable contract, routing, and safety rules.
- [`assets/`](assets/) — templates and reusable artifacts.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
