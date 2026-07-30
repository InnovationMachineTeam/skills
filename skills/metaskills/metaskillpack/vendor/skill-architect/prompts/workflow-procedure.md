# Workflow/Procedure Skill Master Prompt

Apply after [base.md](base.md). Design a skill whose primary value is a repeatable multi-step procedure with decisions and verification.

## Architecture

- Express the workflow as observable stages, entry conditions, decision points, outputs, and exit conditions.
- Use a plan only when steps depend on each other, work is long-running, or risk warrants it.
- Keep one active stage when the host supports state tracking.
- Define which steps may be skipped and the evidence required to skip them.
- Make checkpoints resumable without relying on hidden conversation state.
- Put detailed variants in references instead of branching the main body into every possibility.

## Degree of freedom

Use prose heuristics where multiple approaches are valid, parameterized patterns where a preferred approach exists, and scripts for fragile deterministic steps. Do not force a rigid sequence when context genuinely changes the best route.

## Safety and recovery

Identify read-only, reversible, material, external, and destructive stages. Specify preflight, consent, verification, rollback, partial-success reporting, retry bounds, and blocker conditions proportional to consequence.

## Evaluation

Test normal completion, optional branches, missing prerequisites, interruption and resume, transient and permanent failure, rejected confirmation, partial success, and attempts to claim completion without verifying the outcome.
