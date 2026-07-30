# Inventory and Discovery Management Prompt

Apply after [base.md](base.md).

Resolve only explicit roots and scan to a bounded depth. Record declared names, descriptions, paths, hashes, metadata, source, version, dependencies, and structural validity. Exclude caches and generated directories.

Identify duplicate names and identical versus divergent copies. Treat root order as predicted precedence unless the host confirms it. Do not label a skill active, disabled, or shadowed from file presence alone.

Return a deterministic inventory with unknown fields explicit. Make no changes.

