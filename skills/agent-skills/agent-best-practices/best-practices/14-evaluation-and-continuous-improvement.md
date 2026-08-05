# Evaluation and Continuous Improvement

## Evaluate the system, not eloquence

The primary metric is the share of tasks where the required outcome is proven
within acceptable risk, cost, and time. Also evaluate separately:

1. the individual agent;
2. tool use;
3. routing/delegation;
4. handoff;
5. workflow/team end-to-end;
6. policy and approvals;
7. recovery;
8. production impact.

## Eval pyramid

```text
production outcomes and incidents
end-to-end workflow scenarios
multi-agent coordination and recovery
single-agent task evals
tool/schema/policy unit tests
static validation
```

Lower levels are faster and more deterministic; upper levels are more realistic
but more expensive.

## Dataset

The corpus SHOULD include:

- representative happy paths;
- ambiguous requests;
- boundary/edge/error/recovery;
- adversarial and prompt injection;
- permission denials;
- stale/conflicting context;
- missing agent/tool;
- timeout/cancel/retry;
- parallel conflicts and duplicated work;
- long-running resume;
- platform-specific cases;
- real production failures.

Separate the train/development set and the held-out regression set. Do not tune
the prompt on held-out cases.

## Rubric

Example dimension set:

| Dimension | What is measured |
|---|---|
| Goal achievement | Whether the observable outcome was achieved |
| Correctness | Facts, calculations, code behavior |
| Completeness | Coverage of mandatory requirements |
| Grounding | Claims supported by sources/evidence |
| Scope discipline | No unnecessary actions |
| Tool correctness | Choice, arguments, order, side effects |
| Delegation quality | Correct tasks and context |
| Handoff quality | Completeness of status and continuation |
| Safety | Policy, privacy, approvals, injection resistance |
| Recovery | Errors, retries, cancel/resume |
| Efficiency | Cost/latency/tool calls at success |
| Operability | Trace, artifacts, diagnosability |

For each score, define behavioral anchors, not just 1-5.

## Graders

Use a combination of:

- deterministic assertions;
- schema validators;
- test execution;
- source/code comparison;
- policy simulator;
- LLM judge with rubric;
- pairwise comparison;
- human/domain expert review.

An LLM judge must not be the sole judge for security, money, compliance, and
irreversible side effects. Check judge calibration and inter-rater agreement.

## Orchestration verification

Test not only the final answer:

- the router selected the correct path;
- an unnecessary agent was not launched;
- the context pack is minimal and sufficient;
- child permissions did not expand;
- the DAG and waves are correct;
- no duplicate write ownership;
- the aggregator preserved dissent/evidence;
- the budget and max depth were respected;
- failure was not masked by overall success;
- cancel/retry/resume are idempotent.

## Team evals

Compare the team against a single-agent baseline:

- quality lift;
- latency and cost multiplier;
- coordination overhead;
- conflict/duplicate rate;
- critical-path speedup;
- diversity/independence of specialists;
- synthesis loss;
- operator intervention.

If the team does not provide a measurable gain, return to a simpler
architecture.

## Trigger/routing evals

A set of positive, negative, and near-miss prompts measures precision/recall.
Especially important:

- requests where the agent MUST trigger;
- similar requests where it must not trigger;
- conflict between several agents;
- insufficient context;
- explicit user override;
- multilingual/paraphrase cases.

## Security evals

- direct/indirect prompt injection;
- exfiltration via tool arguments/output;
- privilege escalation and confused deputy;
- malicious memory/doc/tool/agent card;
- approval replay or digest mismatch;
- unsafe handoff;
- network allowlist bypass;
- unsafe code execution;
- audit tampering;
- resource exhaustion;
- emergency revoke.

Link them to the OWASP Agentic Top 10 and the local threat model.

## Efficiency optimization

OpenAI recommends first establishing a quality baseline on a strong model, then
replacing it with a cheaper one where the eval target is preserved
([guide](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)).

Optimize in this order:

1. remove unnecessary calls/tools/agents;
2. improve routing and context retrieval;
3. reduce variable outputs;
4. cache stable context;
5. choose the model per DAG node;
6. parallelize only the critical path;
7. reduce retries through descriptive errors.

## Agent release gate

Before a new version:

- static/schema checks pass;
- unit/tool/policy tests pass;
- the held-out eval has not regressed beyond budget;
- critical safety cases pass;
- cost/latency remain within the envelope;
- docs/contract/changelog are updated;
- compatibility and migration are checked;
- canary cohort and rollback are defined;
- owner/approver sign the evidence bundle.

## Production learning loop

```text
trace/feedback/incident
  → classify failure
  → reproduce as eval
  → root cause: prompt/tool/context/model/policy/orchestration
  → minimal change
  → regression suite
  → canary
  → monitor
```

Do not change a prompt blindly based on a single example. First classify the
causal layer; often the problem is the tool contract, stale docs, or
permissions.

## Eval report

```markdown
# Agent evaluation report

## Versions and environment
## Dataset and exclusions
## Baseline
## Results by dimension and risk class
## Failure clusters
## Cost and latency
## Security findings
## Regressions
## Human review disagreements
## Decision and rollout
## Follow-up owners
```

Results without the prompt/model/tools/policy version and dataset digest are not
reproducible.
