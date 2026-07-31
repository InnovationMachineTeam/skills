# Bootstrap contract

The manifest pins architecture identity/hash and contains only approved
operations. It names synthetic identities/data, exact destination, adapters,
stores, migrations, health checks, fixtures, expected revisions, rollback and
cleanup. `production_activation` is always false for this skill.

The vertical trace must link request, policy/version, resolved assets, run,
lease/fencing token, tool/action, artifact/hash, verification and terminal
state. Failure fixtures leave no active lease or ambiguous side effect.
