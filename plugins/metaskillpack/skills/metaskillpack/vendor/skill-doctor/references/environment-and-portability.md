# Environment and Portability Diagnostics

## Contents

- Environment inventory
- Failure classes
- Portability
- Dependency handling

## Environment inventory

Record host/client, OS, architecture, shell, working directory, runtime versions, environment variables by name only, tools, credentials status, permissions, network, sandbox, locale, and filesystem behavior. Never print secret values.

## Failure classes

- missing capability or dependency;
- authentication or authorization;
- network, timeout, or rate limit;
- invalid input or schema drift;
- host policy or sandbox denial;
- OS/path/encoding difference;
- transient service failure;
- ambiguous external result.

Retry only confirmed transient failures within a bound. Do not repair permissions by broadening access without approval.

## Portability

Distinguish portable core, host-optimized behavior, and unsupported claims. Validate discovery, metadata, paths, invocation, resources, tools, and execution separately on each claimed host.

## Dependency handling

Confirm the failing version and compatibility before proposing an upgrade. Prefer declared, pinned, or bundled dependencies where supported. Treat third-party scripts and packages as supply-chain inputs requiring provenance and security review.
