# agent-best-practices

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Maintains and applies an evidence-linked corpus of best practices for individual agents, subagents, agent teams, orchestration, documentation, evaluation and Agentic OS.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `research`, `governance`.

## When To Use

Querying agent design guidance, auditing an agent or agent-oriented skill against practices, checking source freshness, reconciling changed guidance, rebuilding the corpus, or preparing a bounded portfolio-change prompt. Do not treat platform examples as universal rules, perform open-ended research without scope, edit active agents, or activate changes.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-best-practices What documentation contract should a software-architecture agent have?
```

**Expected result:** route `query` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### query

- **Example request:** “What documentation contract should a software-architecture agent have?”
- **Expected route:** `query`.

### audit

- **Example request:** “Audit this agent definition against current lifecycle and delegation practices.”
- **Expected route:** `apply`.

### refresh

- **Example request:** “Check whether the official agent sources changed and prepare a corpus rebuild candidate.”
- **Expected route:** `refresh`.


## Expected Results

### scope-platform-fact

For request “A Cursor guide recommends a setting; make it mandatory for every host.”, the result must:

- keeps platform scope;
- requires evidence before universal rule.

### conflicting-sources

For request “Two official sources conflict about delegation limits.”, the result must:

- records scope and revisions;
- blocks silent reconciliation.

### docs-taxonomy

For request “Create every possible docs folder for a tiny advisory agent.”, the result must:

- requires owned consumers;
- creates directories on demand.


## Execution Flow

1. **Select one route.** Execute the corresponding contract step from `SKILL.md`.
2. **Preserve evidence integrity.** Execute the corresponding contract step from `SKILL.md`.
3. **Apply documentation practices.** Execute the corresponding contract step from `SKILL.md`.
4. **Validate and complete.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Create and activate a production coding agent now.” → `agent-builder`.
- “Evaluate the routing description of this PDF skill.” → `skill-evaluator`.

Critical anti-results:

- promotes platform fact to universal MUST;
- silently chooses one;
- creates empty taxonomy.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](DONOR.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/validate_corpus.py`](scripts/validate_corpus.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
