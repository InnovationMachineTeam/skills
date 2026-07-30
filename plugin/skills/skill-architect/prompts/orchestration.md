# Orchestration/Composition Skill Master Prompt

Apply after [base.md](base.md). Design a skill that coordinates multiple agents, skills, tools, or stages toward one outcome.

## Decomposition

- Delegate only bounded, independently useful work.
- Define ownership, allowed files or systems, inputs, forbidden changes, output format, and completion evidence for every subtask.
- Keep authority resolution, final integration, and safety-critical policy interpretation with the orchestrator.
- Avoid parallel work that writes the same files or mutates the same external target.
- Prefer fan-out for independent discovery and fan-in for synthesis and verification.

## State and failure

- Track task status, dependencies, budgets, checkpoints, and partial results explicitly.
- Assume shared-workspace changes may appear while workers run; prohibit reverting unrelated work.
- Define timeout, retry, cancellation, stale-result, and unavailable-worker behavior.
- Continue independent work after one branch fails when safe; report degraded coverage.
- Verify integrated output rather than trusting child completion messages.

## Context discipline

Pass the minimum task-local context needed. Do not leak expected answers into evaluation subtasks. Summarize large child outputs and preserve links to raw evidence. Prevent recursive delegation loops with a clear depth or ownership boundary.

## Evaluation

Test single-worker fallback, parallel success, one branch failure, conflicting edits, duplicate work, stale results, interrupted aggregation, budget exhaustion, malicious child output, and false completion before integration verification.
