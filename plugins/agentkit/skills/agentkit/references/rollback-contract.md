# Agentkit rollback contract

1. Keep the last known-good pack version, donor lock and evaluation result until the replacement passes observation.
2. Never roll back by editing canonical or vendored donors.
3. For the first stable pack, the fallback is direct invocation of the locked donor skills; no composite remains active.
4. For later versions, restore the previous complete pack and its exact donor lock as one unit.
5. Before rollback, stop new `agentkit` routing, preserve active run state, inventory consumers and verify the target hash.
6. After rollback, verify direct donor resolution, command-to-donor parity, authority boundaries and the failing case.
7. Installation, disablement and replacement require target-host lifecycle authority; generating a rollback plan does not grant it.

Use `scripts/build_rollback_plan.py` to create a read-only, hash-bound plan. The
script never uninstalls, replaces or activates a skill.
