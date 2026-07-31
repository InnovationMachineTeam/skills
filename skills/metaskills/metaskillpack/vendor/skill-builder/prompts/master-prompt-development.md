# Scenario: master-prompt-development

Use when the primary artifact is a durable master, system, or developer prompt rather than a skill bundle.

1. Invoke `optimize-prompts` in Create, Audit, Improve, Resolve, Adapt, or Evaluate mode.
2. Preserve instruction authority, runtime constraints, permissions, untrusted-data boundaries, recovery, and output contracts.
3. Run mechanical lint plus behavioral, adversarial, and failure cases proportional to risk.
4. If the prompt should become reusable capability with triggers and bundled resources, run the worth gate and hand it to `skill-architect`.
5. Invoke `skill-evaluator` for the resulting skill bundle's routing, behavior, adversarial, authority, and regression gates.
6. Run `skill-doctor` only when diagnosing a confirmed defect in an existing or newly created prompt-backed skill.

Do not convert every prompt into a skill. Keep one-off task prompts ad hoc and project-specific rules in the appropriate project instruction layer.
