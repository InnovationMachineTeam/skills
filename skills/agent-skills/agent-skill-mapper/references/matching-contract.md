# Matching contract

Evaluate hard constraints before ranking soft fit.

## Hard gates

- The capability exists at the referenced version and is not retired or quarantined.
- Its visibility permits the agent to consume it.
- Required host features, tools and data access are available.
- Requested permissions are a subset of the agent's authorized permissions.
- Provenance and trust satisfy the project's policy.
- Side effects fit the agent's role and human checkpoints.

Failure of a hard gate is `REJECT` or `CONFLICT`, never a low score.

## Soft evidence

Assess mission/trigger overlap, task frequency, input/output compatibility,
evaluation quality, maintenance cost, context size, redundancy and portability.
Use explicit evidence references. Do not invent a universal numeric threshold;
record the project's weights and decision rule in the proposal.

## Capability budget

Count active bindings, adapters and always-loaded private instructions. Prefer a
small coherent set. Route occasional capabilities on demand and remove dominated
or duplicative bindings. Exceeding `max_capabilities` invalidates a proposal.

## Decisions

- `MATCH`: all hard gates pass and evidence supports direct binding.
- `CONDITIONAL`: viable only with a named adapter, evaluation or approval.
- `GAP`: no adequate governed capability exists.
- `CONFLICT`: two bindings or authorities cannot safely coexist.
- `REJECT`: the candidate is unsuitable or forbidden.
