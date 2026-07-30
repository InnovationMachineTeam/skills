# Release process

## Individual skill release

1. Update canonical skill and evals.
2. Bump `metadata.version` using SemVer.
3. Regenerate `.claude-plugin/marketplace.json`.
4. Rebuild aggregate plugin and update its version if bundled content changed.
5. Run static, discovery, behavior, security, clean-install, and upgrade checks.
6. Obtain required review.
7. Merge to protected `main`.
8. Create an immutable tag and release notes.
9. Verify installation from the repository rather than the local checkout.

## Initial private release

Recommended tag: `v1.0.0`. The release is accepted when all 12 individual entries are discoverable, representative skills load in Claude Code, Skills CLI lists all 12, and rollback to the archived pre-marketplace source is documented.

## Rollback

- Pin or restore the previous known-good repository revision.
- Remove the candidate from the affected scope.
- Reinstall the previous skill entry or aggregate plugin.
- Verify discovery and one critical behavior case.
- Record the incident and block the faulty version.

Do not delete the migration archive until at least two successful release cycles or 14 days, whichever is longer.
