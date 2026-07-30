# Script-Backed Automation Skill Master Prompt

Apply after [base.md](base.md). Design a skill whose primary value is deterministic, repeatable, or fragile automation.

## Script-first design

- Define a small stable command-line contract before writing instructions around it.
- Keep judgment, routing, and consent in `SKILL.md`; keep exact transformations in scripts.
- Prefer the runtime and libraries already available in the target workspace.
- Parameterize inputs and outputs instead of embedding task-specific paths or values.
- Avoid shell string interpolation when structured process execution is available.

## Reliability and safety

- Validate file existence, type, size, encoding, schema, and exact mutation target.
- Preserve originals unless replacement is explicitly requested.
- Use temporary files and atomic replacement for risky writes.
- Make operations idempotent or detect duplicate execution.
- Bound CPU, memory, network, recursion, and retry behavior.
- Never embed secrets or print them in diagnostics.
- Document dependencies and provide a clear missing-dependency failure.

## Interface

Use stdout for the requested result, stderr for diagnostics, and nonzero exit codes for errors. Provide `--help`; add `--dry-run` for consequential changes. Keep normal execution non-interactive so agents can automate it safely.

## Evaluation

Actually run every script. Test representative success, invalid input, boundary sizes, missing dependency, interrupted write, permission error, repeated execution, and output verification. Use fixtures that contain no production secrets or personal data.
