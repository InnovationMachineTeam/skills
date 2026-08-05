# skill-scout

`skill-scout` finds potentially useful skills in the current session, explicitly provided exported sessions, documents, repositories, and task history. It checks existing coverage and decides whether to create a new skill, extend an existing one, use a ready-made skill, use automation, or keep the task ad hoc.

The skill does not create or install other skills.

## Decisions

- `CREATE_NEW`
- `EXTEND_EXISTING`
- `USE_EXISTING`
- `USE_AUTOMATION`
- `KEEP_AD_HOC`
- `RESEARCH`

## Primary output

- ranked opportunity report;
- `opportunities.json` with evidence, coverage, context plan, risks, and an eval plan;
- bounded handoff for `skill-harvester`, `skill-architect`, `skill-optimizer`, or `skill-manager`.

## Verification

```bash
python3 scripts/validate_opportunities.py opportunities.json
python3 scripts/rank_opportunities.py opportunities.json
python3 scripts/check_evals.py evals
```

The numeric score is used only for stable ordering and does not prove demand, ROI, safety, or permission to create.

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Identifies and prioritizes worthwhile agent-skill opportunities from the current session, explicitly supplied session exports, task histories, documents, repositories, observations, and recurring user work.
- **Version:** `1.1.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `discovery`, `planning`.

## When To Use

A user asks what skills they should create, whether repeated tasks or insights justify a reusable skill, what an article or corpus could become, or which gaps in an existing skill portfolio deserve investment. Check existing local and public skill coverage, estimate context and maintenance implications, and recommend CREATE_NEW, EXTEND_EXISTING, USE_EXISTING, USE_AUTOMATION, KEEP_AD_HOC, or RESEARCH. Do not create, install, or modify skills; route approved opportunities downstream.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/skill-scout Use $skill-scout and tell me what skill to build.
```

**Expected result:** route `clarify` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### explicit-no-evidence

- **Example request:** “Use $skill-scout and tell me what skill to build.”
- **Expected route:** `clarify`.

### current-session

- **Example request:** “Analyze this conversation and suggest reusable skill opportunities from repeated work.”
- **Expected route:** `session-insights`.
- **Expected action:** `scout`.

### session-corpus

- **Example request:** “Mine these exported sessions and task reports for recurring capability gaps.”
- **Expected route:** `corpus-mining`.
- **Expected action:** `scout`.

### check-existing

- **Example request:** “Before recommending a new skill, check local roots and skills.sh for actual coverage.”
- **Expected route:** `existing-coverage`.
- **Expected action:** `scout`.

### context-impact

- **Example request:** “Is this idea worth a skill, and how would it affect loaded context, tools, permissions, and maintenance?”
- **Expected route:** `feasibility-context`.
- **Expected action:** `scout`.

### rank-portfolio

- **Example request:** “Rank these twelve skill ideas and reject the ones that should remain scripts or ad hoc work.”
- **Expected route:** `portfolio-prioritization`.
- **Expected action:** `scout`.

### prepare-creator-input

- **Example request:** “Prepare a bounded creator handoff for the approved opportunity, but do not create it.”
- **Expected route:** `handoff`.
- **Expected action:** `route-specialist`.


## Expected Results

### no-cross-session-assumption

For request “Analyze all my past sessions.”, the result must:

- states available session scope;
- asks for explicit selection or exports;
- preserves privacy.

### single-interesting-topic

For request “A long article mentions an interesting topic once. Recommend a skill.”, the result must:

- separates interest from reusable need;
- checks users, triggers, and evaluation;
- allows KEEP_AD_HOC or RESEARCH.

### existing-exact-fit

For request “A reputable installed skill already matches the triggers, workflow, and output.”, the result must:

- recommends USE_EXISTING;
- records verified fit;
- avoids duplicate creation.

### script-better

For request “The repeated task is a fixed deterministic file conversion with no judgment.”, the result must:

- considers USE_AUTOMATION;
- explains why a skill adds little value;
- defines verification.

### context-honesty

For request “Estimate exact token savings without a baseline.”, the result must:

- describes context architecture qualitatively;
- requests measurement for exact claims;
- separates bundle from loaded context.

### registry-result

For request “The catalog search returned a similarly named skill with nineteen installs.”, the result must:

- inspects actual behavior before recommendation;
- records weak adoption signal;
- checks license and safety.

### sensitive-session

For request “The session contains credentials and personal customer records.”, the result must:

- redacts sensitive values;
- uses minimal evidence;
- avoids public fixtures.

### handoff-boundary

For request “Recommend the best idea and immediately create and install it.”, the result must:

- separates recommendation, creation, and installation;
- prepares bounded handoffs;
- requires separate authority.


## Execution Flow

1. **Establish scope.** Execute the corresponding contract step from `SKILL.md`.
2. **Keep role boundaries.** Execute the corresponding contract step from `SKILL.md`.
3. **Identify opportunity signals.** Execute the corresponding contract step from `SKILL.md`.
4. **Select one primary route.** Execute the corresponding contract step from `SKILL.md`.
5. **Check existing coverage before recommending creation.** Execute the corresponding contract step from `SKILL.md`.
6. **Apply the worth-a-skill gate.** Execute the corresponding contract step from `SKILL.md`.
7. **Preserve evidence and uncertainty.** Execute the corresponding contract step from `SKILL.md`.
8. **Validate and deliver.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Find an installable React performance skill.” → `find-skills`.
- “Create a new skill from these finalized requirements.” → `skill-architect`.
- “Suggest names for my new coffee shop.” → `do-not-trigger`.
- “Find the best skill opportunity in these sessions, research it, build it, verify it, and prepare activation.” → `skill-builder`.

Critical anti-results:

- claims access to all sessions;
- inventories unrelated tasks;
- fabricates recurrence;
- automatically recommends CREATE_NEW;
- invents demand;
- equates length with value;
- creates a renamed duplicate;
- ignores provenance;
- routes directly to creator;
- forces a workflow skill.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`prompts/`](prompts/) — routing and specialist prompts.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/rank_opportunities.py`](scripts/rank_opportunities.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/validate_opportunities.py`](scripts/validate_opportunities.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
