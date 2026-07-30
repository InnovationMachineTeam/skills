# Inventory and Discovery Management Prompt

Apply after [base.md](base.md).

Resolve public roots and agent-private roots separately and scan only explicit
paths to a bounded depth. Record declared names, descriptions, paths, hashes,
metadata, source, version, dependencies, structural validity, visibility,
scope, discoverability, owner agent, and allowed consumers. Exclude caches and
generated directories. Path-derived visibility is predicted until registry and
host discovery agree.

Identify duplicate names and identical versus divergent copies. Treat root order as predicted precedence unless the host confirms it. Do not label a skill active, disabled, or shadowed from file presence alone.

Do not add private roots to global discovery. Verify registry/hash parity and
report a private entry without an owner, a public entry in a private root, or an
unauthorized binding as a blocking conflict.

Return a deterministic inventory with unknown fields explicit. Make no changes.
