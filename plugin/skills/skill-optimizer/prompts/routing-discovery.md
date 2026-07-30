# Routing and Discovery Optimization Prompt

Apply after [base.md](base.md). Optimize skill selection without masking execution defects.

## Diagnose

- Test frontmatter metadata independently from the body.
- Separate missed triggers, false triggers, ambiguous requests, and collisions.
- Confirm whether the host uses only `name` and `description` or additional metadata.
- Compare direct language, paraphrases, artifact names, neighboring tasks, and compound requests.

## Optimize

- State capability and concrete trigger contexts in the description.
- Add exclusions only where measured collisions justify them.
- Prefer natural discriminating terms to keyword lists.
- Keep the name short, stable, and tool-namespaced only when useful.
- Regenerate UI metadata if the contract changes.

## Guardrails

Do not broaden triggers to maximize recall at the expense of harmful false positives. Do not edit the body when selection is the only confirmed defect. Use held-out routing cases and report weighted false-positive and false-negative costs.

