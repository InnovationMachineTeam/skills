# Constrained model profile

Use when model capabilities are unknown or not validated for the workflow.

For each phase:

1. Restate the phase objective, exact inputs, allowed writes and forbidden
   effects in a compact checklist.
2. Select one next action from the factory contract; do not branch into later
   phases.
3. Produce the declared artifact using its schema or template.
4. Check every required field, link, permission and exit condition explicitly.
5. If a check fails, correct once without widening scope. Then stop with the
   failed assertion, preserved state and required human decision.
6. Update state only after inspecting the artifact.

Use enumerated states and exact output contracts. Do not replace missing facts
with guesses or treat a completion message as evidence.
