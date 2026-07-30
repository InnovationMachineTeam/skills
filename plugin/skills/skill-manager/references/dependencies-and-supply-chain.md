# Dependencies and Supply Chain

## Contents

- Provenance
- Inspection
- Credentials
- Updates

## Provenance

Record origin, revision, author or organization, license, integrity hash, update channel, and review status. Treat third-party skills as software supply-chain inputs.

## Inspection

Inspect scripts, binaries, packages, install hooks, network access, tool dependencies, permissions, embedded prompts, assets, symlinks, and generated files before activation. Never execute managed content merely to inventory it.

## Credentials

Do not inventory secret values. Record only required credential types and status through supported interfaces. Avoid expanding permissions during installation or repair.

## Updates

Pin or record revisions where possible. Diff before update, test staged candidates, verify migration and rollback, and avoid unreviewed automatic updates for consequential skills.

