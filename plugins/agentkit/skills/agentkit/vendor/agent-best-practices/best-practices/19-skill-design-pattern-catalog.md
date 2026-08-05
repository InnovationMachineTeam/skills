# Skill Design Pattern Catalog

## Skill as a capability package

A skill is a versioned package of instructions, references, scripts, and evals
that provides a bounded capability to an agent. It does not have to be an
agent: an agent owns the goal and runtime decisions, a skill defines a
repeatable method or specialization, a tool executes an operation, and a
workflow coordinates steps.

A good skill has a narrow semantic boundary, a precise trigger description,
progressive disclosure, a verifiable outcome, and explicit permissions/side
effects.

## Structural patterns

### Atomic skill

One capability, one class of intent, one primary workflow. This is the default:
it is easier for trigger evals, versioning, reuse, and least privilege. Split a
skill if its modes require different owners, permissions, contexts, or release
cadence.

### Method skill

Encapsulates a method: threat modeling, migration review, requirements linting.
`SKILL.md` stores the decision process and navigation; detailed rubrics/templates
live in references. The method must define input, output, stop conditions, and
evidence.

### Adapter skill

Translates a canonical process to a platform or toolchain: Claude Code, Codex,
Cursor, GitHub. Core semantics remain shared; the adapter contains only
commands, manifest rules, and platform limits. This prevents duplication of the
entire logic.

### Script-backed skill

Deterministic, repeatable, or sensitive operations are handled by a script,
while the model prepares parameters, interprets the result, and handles
exceptions. Scripts use explicit arguments, dry-run, typed output, stable exit
codes, idempotency, and tests. A script must not hide changes to external
state.

### Reference-backed skill

The main file briefly routes to thematic references. Each reference has a clear
trigger for reading; highly volatile data includes source, checked date, and
refresh procedure. A copied document without provenance becomes a hidden fork.

### Generator-validator pair

One part creates an artifact, the other independently checks schema, semantics,
and task outcome. The validator can be a script, an eval suite, or a separate
read-only skill. The author's self-check is useful, but does not replace an
independent gate.

### Context-builder

The skill assembles a minimal evidence pack before the main work: questions,
sources, code/doc excerpts, assumptions, and gaps. An inbox is a temporary
staging area, not canonical memory; the final synthesis should remove
duplicates, mark conflicts, and preserve provenance.

### Evaluator skill

Describes dataset, positive/negative triggers, rubrics, graders, thresholds,
variance policy, and regression comparison. It must not modify the evaluated
skill during a single evaluation run.

### Guard / decorator

Adds preflight, approval, security scan, or a postcondition to another skill.
Composition order MUST be explicit. A guard in a prompt is not enforcement: the
real blocking control belongs at the tool/runtime boundary.

## Composition patterns

### Composite / skillpack

A single entry point routes to several donor skills or built-in modes. The
following are required:

- non-overlapping mode contracts and explicit command form;
- default/fallback behavior for ambiguity;
- a donor manifest with exact versions and compatibility range;
- provenance of every borrowed prompt/script/reference;
- a ban on silently editing donors;
- integration and routing evals on top of each donor's evals;
- an upgrade workflow with diff, migration notes, eval gate, and rollback.

A skillpack is justified by a shared user journey, not by a desire to hide many
unrelated skills under one name.

### Router skill

Classifies intent and launches one suitable capability. The description answers
"when to use it" rather than listing internals. Test overlapping intents,
near-miss negative triggers, confidence, and the questions needed for missing
context.

### Strategy / mode

A shared domain has several algorithms: `create`, `optimize`, `doctor`,
`evaluate`. The mode contract records additional arguments and side effects. If
modes evolve independently, keep them as separate donor skills and use
router/composite only as a facade.

### Pipeline skill

Steps form a stable artifact flow: context -> design -> build -> evaluate ->
package. Each stage has a schema and can be resumed. If the order is dynamic,
orchestration should live in a workflow/agent, and the skill should provide
separate capabilities.

### Extension point

The core skill publishes a versioned hook contract, and extensions add domain or
platform behavior without modifying the core. Hook-declared side effects, order,
timeout, failure semantics, and compatibility are mandatory. Do not execute
discovered extensions automatically just because of a filename.

## Description and activation patterns

### Trigger contract

The description contains capability + situation/intent + key constraints. It
must not promise a broader outcome than the skill supports. A useful format:

```text
Use when <user intent/context>. Handles <bounded capability> and produces
<artifact/outcome>. Do not use for <nearest confusing alternatives>.
```

### Progressive disclosure

1. The registry loads name/description.
2. On selection, the entire `SKILL.md` is read.
3. References/scripts/assets are opened only by explicit routing instruction.

The main file is a control document, not an encyclopedia. But critical safety
rules and action order must not be hidden deep inside references.

### Decision table

When branching depends on 2-4 attributes, use a table instead of long prose.
For each route, define input, required context, action, output, and fallback. A
large dynamic graph should be moved into workflow-as-code.

## Skill lifecycle patterns

### Source-of-truth manifest

The manifest records name, semantic version, owner, publisher, status, license,
dependencies, compatibility, permissions, data handling, entrypoint, eval refs,
provenance, and replacement. YAML frontmatter should not be the only location
if the marketplace requires a separate canonical manifest; the fields are kept
in sync by a validator.

### Donor lock and upgrade

A composite skill stores donor, resolved version, source commit/content hash,
included components, and transformation notes. Upgrade:

1. resolves current and available versions;
2. exits unchanged if hashes match;
3. shows semantic and file diff;
4. checks compatibility/migrations;
5. rebuilds a candidate, not the active version;
6. runs donor + integration + regression evals;
7. publishes and canary-promotes only after the gate;
8. preserves a rollback target.

### Deprecation bridge

A deprecated skill remains discoverable for a limited time, warns about a
replacement, includes a migration guide, and stops accepting new dependents.
Retirement removes routes/credentials, but preserves the immutable release and
audit metadata so old runs remain reproducible.

### Harvest-curate-publish

External material first goes into quarantine/inbox, then passes license,
security, provenance, relevance, and duplication review. The extracted pattern
is rewritten to fit the local contract and evals; an external skill is not
published as trusted merely because it can be downloaded.

## Minimal evals

| Layer | What to verify |
|---|---|
| Discovery | the skill is found by target phrasings |
| Negative triggers | it does not activate on adjacent or dangerous intents |
| Routing | it chooses the correct mode and asks the necessary questions |
| Procedure | it follows the required order, gates, and stop conditions |
| Artifact | schema, correctness, completeness, and usability |
| Tool/script | exit codes, errors, dry-run, idempotency, portability |
| Safety | permissions, prompt injection, secrets, destructive actions |
| Composition | donor compatibility, context transfer, no hidden mutation |
| Regression | a new release does not degrade agreed baselines |

## Skill anti-patterns

- **Mega-skill** - unrelated capabilities, shared context, and broad rights.
- **Trigger soup** - the description lists every possible word and competes with
  the entire marketplace.
- **Prompt-only enforcement** - the prohibition exists only as a textual
  request.
- **Hidden side effect** - install, network write, or publish without preflight.
- **Reference maze** - nested links without routing or required order.
- **Copied knowledge snapshot** - no source, date, or refresh policy.
- **Scripts as opaque binaries** - unclear inputs, outputs, and changes.
- **Auto-upgrade in place** - active behavior changes before diff and evals.
- **Version without semantics** - there is a number, but no compatibility or
  migrations.
- **Evals written to implementation** - tests confirm steps rather than
  outcome.
- **Composite that edits donors** - the package cannot be reproduced or
  upgraded.
- **Skill as implicit agent** - the skill starts setting new goals and
  delegating beyond the user's intent.

## Decision: skill, agent, tool, or workflow

| Need | Primary mechanism |
|---|---|
| Repeatable instruction/method | Skill |
| Deterministic action | Tool/script |
| Adaptive achievement of a bounded goal | Agent |
| Stable sequence and durable state | Workflow |
| Single entry point to related capabilities | Router/composite skill |
| Policy and action blocking | Policy service + enforcement point |

Composition is often correct: a workflow calls an agent, the agent activates a
skill, the skill prepares a safe tool call, and the runtime applies policy.
