# Visibility and access management

## Meaning

`public` means discoverable from an approved repository/project skill root.
`private` means discoverable and bindable only through an owning agent's
approved private root. Neither value is a confidentiality classification.

Recommended canonical paths:

```text
skills/<category>/<skill>/SKILL.md
.agents/skills/<skill>/SKILL.md
.agents/definitions/<agent-id>/skills/<skill>/SKILL.md
.agents/definitions/<agent-id>/commands/<command>.md
```

## Inventory rules

- Scan public roots and private roots separately.
- Do not recursively include private roots in global host discovery.
- Record `visibility`, `scope`, `discoverability`, `owner_agent_ref`, and
  `allowed_consumers` in inventory and registry.
- Treat path-derived visibility as a prediction until registry and host behavior
  agree.
- Report private registry metadata without exposing private content unless the
  exact root is authorized.

## Lifecycle rules

Activation of a private skill means attaching it to an approved owner/consumer,
not copying it into a global root. Verify positive owner use, unauthorized-agent
denial, global non-discovery, registry/hash parity, and rollback.

Promotion and demotion change capability topology and belong to
`skill-refactor`; manager applies the approved lifecycle plan, updates observed
state, and verifies discovery after migration.
