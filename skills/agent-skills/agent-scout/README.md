# agent-scout

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Identifies and prioritizes justified opportunities for one agent or subagent from tasks, sessions, code, documents, incidents and recurring work, then checks whether code, a model call, workflow, existing agent, team or Agentic OS already fits.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `discovery`, `planning`.

## When To Use

Deciding whether to create or extend an agent, finding duplicate or missing agent capabilities, or producing an evidence-backed agent opportunity manifest. Read only by default. Do not design, build, install or activate agents, treat frequency or persona names as proof, or recommend a new agent without coverage, maintenance, authority and evaluation analysis.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-scout Review these recurring tasks and tell me which ones justify an agent.
```

**Expected result:** route `portfolio` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### discover

- **Example request:** “Review these recurring tasks and tell me which ones justify an agent.”
- **Expected route:** `portfolio`.

### duplicate

- **Example request:** “Check whether this proposed reviewer duplicates an installed agent.”
- **Expected route:** `coverage`.

### session

- **Example request:** “Find potential agent opportunities in these session notes without creating them.”
- **Expected route:** `discover`.


## Expected Results

### deterministic

For request “Create an agent to sort a fixed JSON array.”, the result must:

- selects code or script;
- rejects unnecessary autonomy.

### unknown

For request “Public search failed because network is unavailable; label coverage none.”, the result must:

- labels coverage unknown;
- records search failure.

### docs

For request “The proposed architect agent needs ADRs; create every docs folder now.”, the result must:

- records documentation needs only;
- defers structure to architect.


## Execution Flow

1. **Inventory and compare.** Execute the corresponding contract step from `SKILL.md`.
2. **Apply the worth gate.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Find reusable skill opportunities in this article.” → `skill-scout`.
- “Design the exact definition for this approved agent.” → `agent-architect`.

Critical anti-results:

- rewards agent novelty;
- claims none;
- creates directories.

## Dependencies

- **Recommended: `agent-best-practices` >= `1.0.0`.** Provides selection, lifecycle and maintenance criteria.
- **Recommended: `agent-context` >= `1.0.0`.** Recommended when the opportunity decision needs additional evidence.

A missing required dependency blocks only the route that depends on it. Recommended dependencies improve evidence quality but must not be imitated by the skill itself.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
