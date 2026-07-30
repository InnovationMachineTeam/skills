# Workflow and Reliability Optimization Prompt

Apply after [base.md](base.md). Improve execution consistency, recovery, and truthful completion.

## Diagnose

- Reproduce missing steps, bad ordering, excess questions, unsafe autonomy, retry loops, lost state, partial success, and false completion.
- Identify whether freedom is too high for a fragile step or too low for contextual judgment.

## Optimize

- Define observable entry conditions, stages, decision points, outputs, and exit conditions.
- Use conditional rules instead of conflicting absolutes.
- Ask only when missing information materially changes outcome or authority.
- Add bounded retries, failure classes, checkpoints, resume behavior, and verification proportional to risk.
- Use scripts for fragile deterministic steps.

## Guardrails

Do not turn a flexible workflow into a rigid checklist without evidence. Do not equate command success with outcome success. Test normal, optional, interrupted, failed, partial, and resumed paths.

