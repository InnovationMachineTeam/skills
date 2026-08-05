# Mode and depth contract

This contract operationalizes the mode selection, evidence discipline, and
depth rules derived from the supplied master prompt.

## Normalized intake

Record the classification before drafting:

```yaml
prompt_task:
  selected_mode: improve | reconstruct | generalize | specialize | merge | decompose | audit | optimize
  source_prompt_available: true | false
  reference_outputs_available: true | false
  research_required: true | false
  depth: Compact | Standard | Production
  confidence: high | medium | low
  critical_missing_information: []
  assumptions: []
```

Accept these optional context fields when supplied:

```yaml
context:
  domain: ""
  target_user: ""
  target_agent_or_model: ""
  execution_environment: ""
  expected_use: []
  expected_outputs: []
  languages: []
  constraints:
    deadline: unknown
    budget: unknown
    context_limit: unknown
    tools: []
    prohibited_tools: []
    jurisdictions: []
    confidentiality: public | internal | confidential | restricted
    risk_level: low | medium | high | critical
  improvement_goals: []
  invariants: []
  known_problems: []
```

Omit unknown optional fields from the final prompt or represent them with
placeholders. Never invent their values.

## Mode decision matrix

| Evidence or requested change | Primary mode | Core specialist operation | Required addition |
|---|---|---|---|
| Source prompt must become more reliable | `improve` | Improve | audit, revision, change evidence |
| Source absent; outputs show desired behavior | `reconstruct` | Create | evidence map and epistemic limits |
| Specific values must become reusable parameters | `generalize` | Adapt/Create | applicability and configuration rules |
| General prompt must fit one domain or host | `specialize` | Adapt | domain risks, tools, sources, revised evals |
| Several prompts must become one | `merge` | Resolve/Improve | precedence, deduplication, provenance |
| One prompt owns separable roles or contexts | `decompose` | Resolve/Create | controller, child boundaries, handoffs |
| User requests findings without rewrite | `audit` | Audit | severity-ranked evidence only |
| Context or execution cost must fall | `optimize` | Improve/Evaluate | invariant-preservation comparison |

If a request combines modes, select the mode that governs the hardest output
contract and record the others as secondary operations. Example: reconstructing
from outputs and then generalizing is primarily `reconstruct` until functional
equivalence is established.

## Reconstruction discipline

When the original prompt is absent:

```yaml
reconstruction:
  exact_original_recovered: false
  functional_equivalence_targeted: true
  confidence: high | medium | low
  evidence: []
  assumptions: []
```

Analyze at least one reference output. Separate its domain content from its
reusable structure. Infer likely inputs, sequence, decision rules, constraints,
quality gates, failures, and output schema. Add missing safety and evaluation
contracts as new recommendations, not as claims about hidden instructions.

Confidence is `high` only when several representative outputs consistently
support the same behavior. One output can support a useful reconstruction but
rarely exact or high-confidence attribution.

## Generalization and specialization

For `generalize`:

- replace private values with named parameters;
- distinguish required and optional capabilities;
- support relevant domains without claiming universality;
- preserve critical constraints and define applicability limits;
- provide safe unknown-data behavior.

For `specialize`:

- preserve the reusable control logic;
- remove sections with no behavioral value;
- add only applicable domain rules, current sources, tools, risks, output
  details, and evaluation cases;
- revalidate authority and host assumptions.

## Merge and decomposition

For `merge`, preserve provenance for material rules. Resolve conflicts using
platform safety, current explicit user objective, law and binding policy,
invariants, target outcome, runtime constraints, and preferences in that order.
At equal authority, prefer the more specific scoped instruction.

For `decompose`, split only when there are independent roles, outputs, contexts,
tools, risk levels, or lifecycle needs. Specify controller routing, child input
and output contracts, shared invariants, handoffs, failure propagation, and a
recursion guard. A child must not reproduce the controller.

## Depth profiles

### Compact

Use for low-risk, simple, or one-off work. Include role, task, inputs,
algorithm, output format, and quality criteria. Add other sections only when an
observed risk requires them.

### Standard

Use for repeatable work, role agents, skills, documents, or research. Add
authority boundaries, missing-data and error behavior, Human gates, evals, and
handoff.

### Production

Use for agent harnesses, orchestrators, critical processes, public components,
or high-risk work. Add machine-readable contracts, security, observability,
versioning, tests, automation boundaries, documentation, governance,
maintenance, rollback, and independent evaluation.

Depth is a consequence of risk and lifecycle, not prompt length. Prefer the
smallest profile that covers every material constraint.

## Source basis

Derived from the user-supplied `Master Prompt for Improving and Reconstructing
Prompts.pdf`. The skill operationalizes its behavior; it does not preserve the
PDF as a runtime dependency or reproduce it verbatim.
