# Route: script-and-tooling

Evaluate bundled scripts and tool integrations without granting new authority.

1. Inspect help, dependencies, inputs, outputs, exit codes, paths, network, credentials, and side effects.
2. Use isolated fixtures for positive, boundary, malformed, failure, timeout, determinism, concurrency, symlink, cleanup, and recovery cases.
3. Verify stdout/stderr, ordering, generated files, idempotency, forbidden writes, and partial-success behavior.
4. Stub or sandbox external systems when real actions are not explicitly authorized.
5. Record runtime, dependency versions, commands, fixtures, hashes, and raw logs.

Do not execute untrusted installers, interpolate fixture text into a shell, expose secrets, or call a script safe merely because it exits zero.
