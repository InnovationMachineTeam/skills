# Agentkit command contract

## Syntax

```text
agentkit <command> [target] [task]
```

Aliases are deliberately narrow: `test` maps to `e2e`; `create` maps to
`architect`; `research` maps to `context`; `improve` maps to `optimize`.
Aliases never override an explicit canonical command.

## Native commands

- `help`: list commands, inputs, donors and approval boundaries.
- `route <task>`: recommend a command and explain the discriminator; do not run it.
- `status`: compare lockfile, vendor and optional canonical donor roots read-only.
- `upgrade`: preview drift and build a complete staged candidate only after scope is authorized.
- `e2e [command|workflow|all] [task]`: scaffold, execute and review an isolated E2E run.

## Specialist commands

Every specialist command resolves to exactly one lock entry. Forward only the
user task, exact target, granted authority, preservation constraints, output
contract and verification requirements. Do not merge donor bodies or load
unselected donors.

`run` is the only multi-stage route. It must present workflow choices and wait
for selection before execution.

## Failure behavior

- Missing command plus clear explicit intent: ask one discriminating question.
- Unknown command: print help and make no mutation.
- Missing or changed donor: block that command and show status evidence.
- Recursive `agentkit` dispatch from a donor: stop and report a routing cycle.
- Donor asks for broader authority: preserve the original authority and stop.
