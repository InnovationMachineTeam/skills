# Inventory and Identity

## Contents

- Scope
- Identity
- Precedence
- Snapshots

## Scope

Require explicit roots. Resolve paths and symlinks. Refuse `/`, a full home directory, or an unspecified workspace as a recursive target. Exclude caches, VCS internals, dependencies, and generated folders unless intentionally managed.

## Identity

Record declared name, folder name, path, description, source, version when available, content hash, owner, host, and install channel. A path is not a stable identity by itself; a shared name is not proof that two bundles are equivalent.

## Precedence

Root order may suggest precedence but does not prove actual client resolution. Label shadowing as predicted until host discovery is observed. Distinguish duplicate content, divergent forks, intentional overrides, and accidental collisions.

## Snapshots

Make inventories deterministic: normalized resolved paths, stable ordering, content hashes, and no secret values. Compare snapshots before and after lifecycle operations. Preserve the original snapshot with the change record.

