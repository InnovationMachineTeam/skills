# Delivery and evaluation contract

Use this contract to decide whether a candidate prompt package is ready and to
produce proportionate evidence.

## Definition of Ready

Work may start when at least one exists: source prompt, task description, or
reference output. A higher-confidence result benefits from a target user,
runtime, constraints, good and bad examples, and quality criteria, but secondary
gaps do not block a safe assumption-led draft.

## Required package fields

Provide only applicable sections, but never omit a blocking finding:

```text
summary
source_and_evidence_analysis
source_audit
reference_output_analysis
candidate_architecture
complete_candidate_prompt
compact_variant
change_map
evaluation_package
usage_example
maintenance_recommendations
```

The candidate prompt itself normally contains:

```text
title
role_and_mission
primary_outcome
inputs
terms_and_entities
authority_and_boundaries
principles
workflow_and_decisions
research_and_tools
human_gates
failure_and_recovery
quality_control
definition_of_ready
definition_of_done
evaluations
output_contract
prohibitions
execution_command
```

Delete any section that adds no observable behavior. Do not repeat the same
rule in the output contract, quality gate, and Definition of Done.

## Evaluation case contract

Create at least these 12 cases unless one is demonstrably inapplicable:

1. complete normal input;
2. incomplete input that can use safe assumptions;
3. contradictory requirements;
4. out-of-scope task;
5. required tool unavailable;
6. high-risk request;
7. current research required;
8. overbroad request;
9. request for minimum configuration;
10. request for Production configuration;
11. request to reduce output length;
12. retry after an unsuccessful first result.

Represent each case as:

```yaml
id: ""
input: ""
expected_behavior: []
expected_output_properties: []
forbidden_behavior: []
pass_criteria: []
```

Add prompt-injection, external mutation, partial success, compaction/resume, and
false-completion cases when the candidate can encounter them.

## Prompt quality rubric

Score each dimension from 0 to 4 and cite evidence:

- clarity of objective;
- completeness and missing-data behavior of inputs;
- process and decision logic;
- authority and boundaries;
- output contract;
- reproducibility;
- failure and recovery behavior;
- Human-in-the-loop decisions;
- security and privacy;
- evaluation coverage;
- efficiency and context cost.

Define the pass threshold before running evaluation. Any uncontrolled external
or destructive authority, untrusted content promoted to instruction,
irreconcilable authority conflict, invented tool result, unbounded loop, or
false-completion path blocks release regardless of aggregate score.

Rubric self-scoring is diagnostic, not proof. Use deterministic assertions for
schemas and invariants, clean-context runs for behavior, and independent or
human review for holistic quality.

## Baseline comparison

When a source or last-known-good prompt exists, compare under the same model,
host, tools, fixtures, configuration, and number of runs. Record at least:

- task success and format adherence;
- unsupported assumptions and unnecessary questions;
- critical-rule adherence and unsafe-action rate;
- false-completion and tool-recovery behavior;
- output length, prompt length, latency, tokens, and cost when available;
- rubric results and variance.

Do not attribute every output difference to the prompt. Record model, runtime,
tool, fixture, or sampling changes as confounders. If comparable runs were not
performed, label the A/B result `NOT_EVALUATED`.

## Version and change record

Use Semantic Versioning for the prompt artifact:

- Major: primary objective, output contract, authority boundary, required
  capability, or main workflow changes incompatibly;
- Minor: compatible mode, check, optional format, or evaluation additions;
- Patch: wording, contradiction, example, or formatting corrections that do
  not intentionally change the public contract.

Record:

```yaml
prompt:
  id: ""
  name: ""
  version: "1.0.0"
  status: draft | experimental | stable | deprecated
  owner: ""
  updated_at: ""
  review_interval: ""
```

For every version record what changed, why, which observation or evaluation
motivated it, new risks, migration needs, and compatibility.

## Definition of Done

A candidate is ready only when:

- mode, depth, primary result, users, and owner are explicit;
- supplied facts, observations, inferences, assumptions, and recommendations
  remain distinguishable;
- invariants and variable parameters are identified;
- conflicts and duplication are resolved with provenance;
- entities, inputs, workflow, boundaries, Human gates, failures, and output
  contract are coherent;
- quality gates and applicable evals exist;
- self-review is complete and independent evaluation is used when risk warrants;
- no critical finding remains open;
- the version, worked example, maintenance trigger, residual risks, and unrun
  checks are recorded.

Do not mark a prompt `stable` without behavioral evidence from its intended
runtime.
