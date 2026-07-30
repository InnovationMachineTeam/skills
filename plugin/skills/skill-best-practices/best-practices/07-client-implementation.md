# Client implementation and context lifecycle

Practice-ID: BP-CLIENT-001
Scope: client
Status: current
Sources: SRC-AS-001, SRC-AS-006, SRC-OAI-001, SRC-ANT-003
Last-rebuilt: 2026-07-30

## Discovery

Support explicit bounded roots or registries. Resolve symlinks, hidden/generated/vendor directories, size and count limits, identity, precedence, duplicate names, trust, and diagnostics. Folder presence does not prove active discovery.

## Catalog

Expose compact name, description, identity/location, and availability. Filter skills whose required capabilities are unavailable. Make collisions and truncation visible. OpenAI currently applies a bounded initial catalog budget; other clients may differ.

## Activation and context

Use a constrained activation mechanism, validate identity again, load the exact current SKILL.md, and record version/hash. Protect active instructions from accidental compaction loss, deduplicate repeated activation, and replace content when the version changes rather than appending stale copies.

Load resources on demand with bounded paths. Keep trusted policy distinct from skill and task data. Host permissions and consent must govern tools and external actions.

## Producer and consumer behavior

Publishers should be strict. Consumers may be diagnostically tolerant, but must not silently normalize identity, authority, or meaning. Record parse errors, unsupported fields, missing dependencies, shadowing, and source scope.
