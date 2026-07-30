# Script and tool evaluation

## Static preflight

Inspect help, inputs, dependencies, platform assumptions, file and network access, credential use, temporary paths, exit codes, stdout/stderr, deterministic ordering, concurrency, cleanup, and recovery. Search for shell interpolation, broad deletion, unsafe globs, cwd dependence, symlink following, silent install, and hidden external writes.

## Dynamic matrix

Test as applicable:

- minimal and representative positive inputs;
- empty, maximum, boundary, malformed, duplicate, and unsupported inputs;
- missing dependency, permission, network, timeout, and partial-failure paths;
- spaces, Unicode, special characters, traversal, symlinks, and path collisions;
- deterministic reruns, idempotency, concurrency, locks, interruption, cleanup, and rollback;
- stdout/stderr separation, structured output, exit codes, and actual resulting artifacts.

Use explicit fixtures and bounded temporary destinations. Hash source fixtures before and after when immutability is required.

## Tool integrations

Separate mocked contract tests, sandbox/staging tests, and authorized live tests. Tool availability is not permission. Verify exact recipients, resources, scopes, read-back, partial success, rate-limit behavior, and retry bounds. Avoid real destructive actions when a faithful safe surrogate can test the contract.
