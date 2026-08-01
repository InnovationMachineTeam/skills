# Role-skill output contract

## Contents

- Classification and research
- Skill package
- Implementation proposal
- Evaluation and completion

## Classification and research

Return the mechanism decision, visibility, owner, consumers, primary outcome,
triggers, non-triggers, scope, side effects and risk. Explain why the next
simpler form is insufficient and why any proposed split or merge is necessary.

For every material source record:

```yaml
source:
  title: ""
  publisher: ""
  locator: ""
  type: "official-doc|standard|law|research|source-code|professional-guidance|exemplar"
  version_or_date: ""
  accessed_at: ""
  supported_decision: ""
  limitations: ""
```

Mark claims `supported`, `changed`, `new`, `conflict`, `deprecated`,
`unverified` or `exemplar-only` when reconciliation is needed.

## Skill package

The host-native candidate must include:

- a precise discovery description with positive and neighboring negative cases;
- mission, primary outcome, scope and non-responsibilities;
- input, output and handoff contracts;
- a reproducible method with decisions, checks and stop rules;
- Ready/Done and self-review;
- required knowledge with provenance and freshness rules;
- tools and permissions without hidden authority;
- security, privacy, prompt-injection and data-egress controls;
- errors, retries, partial success, rollback/compensation where applicable;
- observability, metrics and maintenance owner;
- version and compatibility policy;
- examples, tests, evals and baseline evidence.

For this repository, `SKILL.md` plus applicable `references/`, `scripts/`,
`assets/`, `agents/openai.yaml` and `evals/` is preferred. Do not force the PDF
prompt's illustrative `skill.yaml`, README, changelog or broad folder tree when
the repository's canonical contract does not use them.

## Implementation proposal

For each proposed script, tool, adapter, automation or hook record:

```yaml
component:
  id: ""
  type: "script|tool|adapter|automation|hook"
  purpose: ""
  trigger: ""
  inputs: []
  outputs: []
  side_effects: []
  permissions: []
  risk: ""
  required: true
  build_reuse_or_adapter: "undecided"
  acceptance: []
```

Do not propose code for judgment that should remain expert reasoning or for a
rare operation whose maintenance cost exceeds its value.

## Evaluation and completion

Cover direct and paraphrased routing, neighboring non-trigger, ambiguity,
standard output, incomplete/invalid input, conflicting sources, unavailable
tool, high risk/Human gate, injection, regression and update freshness as
applicable. Use observable properties, not one exact prose answer.

Completion requires structural validation, linked resources, no placeholders,
tested executables, representative behavioral evidence, explicit uncertainty
and an immutable candidate for independent evaluation. File creation alone is
not completion.
