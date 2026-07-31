# Agentkit Readiness Gate

Status: **STABLE — RELEASED IN MARKETPLACE 3.3.0**

The stable `agentkit@1.0.0` bundle is at
`skills/agent-skills/agentkit/` and is registered as one public, selectively
installable entry in the private marketplace. The reusable design prompt
remains at `docs/prompts/agentkit-composite-skill.md`.

Creation requires all of the following:

1. all ten donors released independently;
2. two consecutive stable portfolio releases after the last donor enters;
3. no blocking routing, authority, documentation, recovery or lifecycle
   regressions in those releases;
4. versioned donor interfaces and reproducible tree hashes;
5. at least three real end-to-end workflows that benefit from one explicit
   entry point;
6. a frozen donor manifest, upgrade comparison, rollback and pack-level holdout;
7. explicit invocation that does not compete with direct specialist triggers.

Release `3.2.0` is the initial donor release. Releases `3.2.1` and `3.2.2`
completed two post-donor stability cycles with unchanged donor hashes and all
blocking layers passing. The machine-readable evidence is in
`docs/agents/evals/individual-agent-stability-cycles.json`.

Completed evidence: **2/2 stable cycles and 3/3 real workflows**. Cycle 2 is tied
to a later timestamp, unchanged donor hashes, new E2E artifacts and release
`3.2.2`; it is not a repeated copy of cycle 1. Upgrade, rollback and external
pack holdout contracts are hash-frozen. Release `3.3.0` promoted the exact
candidate into a separately validated stable package.

## Stable package

`agentkit@1.0.0` is discoverable only through explicit agentkit invocations. It
contains locked read-only donor snapshots, has its own catalog identity and
generated plugin, and appears in the Claude Code, Codex and Cursor marketplace
manifests. Vendored donor entrypoints are named `DONOR.md`, so they are not
independently discovered as nested skills.

The explicit `agentkit e2e` command scaffolds E2E cases, runs selected commands
through the pack router, records raw evidence, classifies ownership and
proposes improvements. A donor-owned finding requires exact user approval
before the pack may write an improvement prompt or dispatch a staged
`repair-and-improve` or `optimize-existing` process. Canonical and vendored
donors remain read-only, and donor promotion remains a separate lifecycle decision.

Synthetic router tests do not count toward real workflow observations.

Candidate evaluation `agentkit-candidate-0.2.0` and exact stable-package
evaluation `agentkit-1.0.0-release` pass all blocking layers.
Three user-authorized semantic workflows exercised full lifecycle,
repair/recovery and optimize/regression routes and retained artifact hashes.
They used the current task executor rather than an external model, so no
cross-model generalization claim is made. Repository publication is complete;
host installation and activation were intentionally not performed and require
separate lifecycle authority plus host read-back.

## Usage documentation

The stable command surface and complete one-agent workflow are documented in
the [Onboarding Guide](ONBOARDING.md#start-with-agentkit). Cross-domain examples
show when `agentkit` is sufficient and when work must route to an agent team or
Agentic OS. The readiness evidence in this file remains a release record; it is
not the primary day-to-day usage guide.
