# Agent-Asset Root Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

- `plugins/marketplace.json` is generated from the canonical catalogue.
- Project agent definitions may be materialized only from an approved exact
  specification and write plan.
- Keep agent definitions, owner-private skills/commands, and generated host
  adapters distinct.
- Register every asset and binding through versioned optimistic transactions.
- Private discovery scope is not a secrecy boundary; enforce confidentiality
  with repository ACL, runtime identity, sandbox, policy, and credentials.
- Do not infer installation, activation, publication, or production authority.
