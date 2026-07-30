# Staged Upgrade Protocol

## Contents

- Invariants
- Discovery and comparison
- Candidate rebuild
- Validation and promotion
- Missing donors
- Rollback

## Invariants

- Source donors are immutable inputs.
- Vendored snapshots are immutable during ordinary modes.
- A version string is necessary but not sufficient: compare deterministic tree digests so changed scripts and resources cannot hide behind an unchanged version.
- Never build in place. Use a new staging directory outside the active pack.
- Never promote a candidate that omits a required donor, weakens authority, loses a route, or fails blocking evals.

## Discovery and comparison

Run `scripts/check_donors.py`. Search only the default sibling root and explicitly supplied donor roots. A root may be a canonical category directory, repository root, plugin `skills/` directory, or a bounded marketplace cache subtree.

Classify each donor as:

- `current`: locked version and digest match;
- `changed`: version or digest differs;
- `missing`: no unambiguous candidate exists;
- `invalid`: `SKILL.md`, `name`, or `metadata.version` is missing or inconsistent.

Treat duplicate candidates with different content as invalid ambiguity rather than picking the newest-looking path.

## Candidate rebuild

Create a complete candidate:

```bash
python3 scripts/build_snapshot.py --skillpack . --output /authorized/staging/metaskillpack-candidate --donor-root /path/to/metaskills
```

The script copies the pack control plane, replaces only `vendor/`, and regenerates `donors.json`. It refuses an existing output directory and refuses missing, invalid, or ambiguous donors.

Then compare changed donor interfaces:

- frontmatter description and trigger boundary;
- modes, scenarios, routes, and aliases;
- required inputs, outputs, authority, and stop conditions;
- prompts, references, scripts, evals, and host metadata;
- handoffs to neighboring skills.

Update the root router, command reference, routing script, master prompts, and eval fixtures only where those interfaces changed. Do not import donor implementation detail into the root router.

## Validation and promotion

Run, in order:

1. official skill validation on the candidate;
2. `scripts/check_evals.py`;
3. `scripts/check_donors.py` against the same donor roots;
4. every changed donor script test available in its snapshot;
5. routing and behavior forward tests for changed modes;
6. package and marketplace validators when publishing.

Review a file inventory and diff against the active pack. Promote atomically or through versioned packaging. Record the old pack version and preserve a recoverable last-known-good artifact.

## Missing donors

Stop before invoking the upgrade master prompt. Report:

- missing or invalid donor name;
- expected locked version;
- searched roots;
- whether the current vendored snapshot remains usable;
- accepted remedies: supply another `--donor-root`, install or restore the donor, or explicitly revise the pack's donor contract in a separate architecture change.

Do not download an unpinned replacement, use a public namesake, silently remove the mode, or relabel the old snapshot as current.

## Rollback

Rollback restores the previous complete pack version, including `SKILL.md`, `donors.json`, scripts, prompts, evals, and all vendored snapshots. Re-run structural and routing checks after rollback. Donor sources require no rollback because upgrade never writes to them.
