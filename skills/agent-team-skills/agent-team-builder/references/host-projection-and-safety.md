# Host projection and safety

Keep canonical agent definitions host-neutral. Generate Claude, Codex, Cursor or
other host adapters from those definitions and record generator/version headers
where the host format permits it. Host-specific constraints may narrow behavior
but may not silently broaden permissions or rewrite the mission.

Collision policy:

- absent path: create in staging;
- compatible generated path: regenerate and drift-check;
- stale generated path: replace only through the approved manifest;
- handwritten or unknown path: stop for review;
- concurrent revision change: abort and rebuild the manifest.

Never emit secrets. Reference credential providers or environment contracts.
Validate permissions, private boundaries and data classes before any smoke test.
