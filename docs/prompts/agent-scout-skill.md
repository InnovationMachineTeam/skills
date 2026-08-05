# Master Prompt For The `agent-scout` Skill

Apply after [agent-skill-base.md](agent-skill-base.md). Create a skill that
finds and prioritizes justified opportunities for agents and agent-oriented
skills, but creates and activates nothing.

## Capability boundary

The skill must answer: "what is the minimal mechanism worth creating or reusing
for this recurring outcome?" It does not design the candidate, write production
prompts, or install assets.

## Source routes

Support the minimally necessary routes:

- session/task insights;
- repository/workflow mining;
- incident/support/task history;
- portfolio gap analysis;
- supplied article/document/corpus;
- explicit idea assessment.

Source scope is always explicit. Do not treat private session history as
available without a provided export or host authorization. Remove secrets/PII
from evidence.

## Decision taxonomy

For each opportunity, return exactly one decision:

- `USE_CODE_OR_WORKFLOW`;
- `USE_EXISTING_AGENT`;
- `EXTEND_EXISTING_AGENT`;
- `CREATE_NEW_AGENT`;
- `CREATE_AGENT_SKILL`;
- `KEEP_HUMAN`;
- `KEEP_AD_HOC`;
- `RESEARCH`;
- `REJECT`.

Do not blur the decision between creating an agent and a skill: an agent
performs a runtime mission, while an agent-oriented skill governs its
design/evaluation/lifecycle.

## Worth model

Evaluate:

- frequency and recurring pain;
- value and measurable outcome;
- variability/uncertainty that requires agent reasoning;
- decomposability and need for tools/state;
- existing coverage and extension cost;
- side-effect risk and human judgment;
- data/access availability;
- evaluation feasibility;
- ownership, maintenance, and retirement cost;
- the simpler alternative.

Do not issue a numeric score without evidence. Use a score only for ranking
after the hard gates: safety, authority, no owner, or no evaluation path may
block the recommendation.

## Required artifacts

```yaml
opportunity_id: stable-id
evidence: []
problem: observable recurring problem
users: []
candidate_outcome: measurable outcome
alternatives: []
existing_coverage: []
decision: RESEARCH
rationale: concise evidence-backed reason
risk_tier: R1
context_needed: []
evaluation_path: []
owner_candidate: null
next_handoff: agent-context
confidence: low
```

## Evaluation

Create positive/negative routing cases and verify that the skill:

- does not propose an agent for a deterministic script;
- finds existing coverage before `CREATE_NEW_AGENT`;
- distinguishes a runtime agent from an agent-oriented skill;
- does not treat a single occurrence as a recurring workflow;
- preserves uncertainty and recommends research when gaps remain;
- does not extract private/sensitive evidence without authority;
- allows the successful terminal outcome of "create nothing".

## Handoff

For each justified agent opportunity, specify which canonical documents and
decision records will be required, but do not create the `docs/` tree. Pass
this as input to
[agent-documentation-contract.md](agent-documentation-contract.md).

Hand off the approved opportunity to `agent-context` when evidence is
insufficient, or to `agent-architect` when the intent is ready. The handoff
contains objective, sources, constraints, alternatives, risk, preserved
systems, and unresolved questions.
