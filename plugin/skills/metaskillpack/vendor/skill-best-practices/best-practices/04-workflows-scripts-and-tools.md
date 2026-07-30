# Workflows, scripts, and tools

Practice-ID: BP-WORKFLOW-001
Scope: portable
Status: current
Sources: SRC-AS-002, SRC-AS-005, SRC-OAI-003, SRC-EX-001, SRC-LOCAL-001
Last-rebuilt: 2026-07-30

## Workflow contract

Define preconditions, required and optional inputs, invariants, phases, decisions, forbidden inferences, clarification/stop/decline conditions, side effects, postconditions, validation, recovery, and definition of done. Bound validation and retry loops.

A durable default is:

```text
discover → plan → preflight → execute → validate → repair → verify → report
```

For mutations use preview, exact consent when required, atomic or reversible change, read-back, manifest, and rollback. Report partial success rather than forcing binary completion.

## Scripts

Use a script for mechanical, repeatedly rewritten, fragile, costly, reproducible, or machine-verifiable work. Agent-facing scripts should be non-interactive, expose useful help, validate inputs before side effects, use structured stdout and diagnostic stderr, meaningful exit codes, deterministic ordering, safe paths, bounded sizes, and explicit dependencies. Actually execute every added or changed script on positive and failure cases.

Avoid shell interpolation of user text, cwd assumptions, symlink escapes, broad globs, uncontrolled temporary files, and silent dependency installation.

## Tools and MCP

Use skills for workflow and judgment; use tools or MCP for authenticated live data and controlled actions. Keep capability, permission, invocation policy, and procedural instruction distinct. Tool availability never grants action authority.
