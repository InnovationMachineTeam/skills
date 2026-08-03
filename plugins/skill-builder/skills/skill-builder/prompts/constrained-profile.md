# Constrained orchestration profile

For each phase:

1. Restate the objective, exact inputs, allowed effects, forbidden effects and
   required output as a checklist.
2. Verify every entry condition before dispatch.
3. Dispatch exactly one owning specialist and one selected route.
4. Validate the returned artifact and each exit assertion explicitly.
5. Update state only from inspected evidence.
6. If a check fails, retry one safe transient action at most once; otherwise
   stop with the failed assertion, preserved state and required decision.

Do not combine phases, infer approval, overwrite baseline evidence or advance
from a specialist completion message alone.
