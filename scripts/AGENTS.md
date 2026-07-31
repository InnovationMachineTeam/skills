# Script Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

- Scripts must be deterministic, non-interactive by default, and explicit about
  inputs, outputs, dry runs, mutations, and exit status.
- Resolve exact targets; never write broad or unresolved paths.
- Build generated artifacts only into a new staging directory.
- Keep canonical/generated comparison byte-accurate and fail closed on drift.
- Avoid network, host installation, credentials, activation, and destructive
  cleanup unless the command contract and user authority explicitly allow them.
- Use stable machine-readable output for validators and tests.
- Add positive and negative unit coverage for new lifecycle or safety behavior.
