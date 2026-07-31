# Release 3.2.2 — agent donor stabilization cycle 2

Release `3.2.2` is the second distinct post-donor stability observation. All
ten individual-agent donor versions and tree hashes remain identical to the
`3.2.0` baseline and `3.2.1` cycle.

New evidence in this cycle:

- three real, artifact-bound agentkit workflows completed through locked donors;
- deterministic router fixtures cannot be relabeled as real observations;
- upgrade, rollback and pack holdout contracts are hash-frozen;
- a first-release rollback plan returns to direct donor invocation without host mutation.

No donor, registry activation, installation or runtime state changed. This
release makes the maturity gate ready for a separate `agentkit@1.0.0`
promotion; it does not itself publish agentkit.
