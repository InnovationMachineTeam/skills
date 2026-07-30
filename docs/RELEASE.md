# Release process

## Individual skill release

1. Update canonical skill and evals.
2. Bump `metadata.version` using SemVer.
3. Rebuild `plugins/` and regenerate Claude Code, Codex, and Cursor marketplace manifests.
4. Rebuild the aggregate plugin and update its version if bundled content or host support changed.
5. Run static, discovery, behavior, security, native-manifest, clean-install, and upgrade checks.
6. Obtain required review.
7. Merge to protected `main`.
8. Create an immutable tag and release notes.
9. Verify installation from the repository rather than the local checkout in every release host.

## Initial private release

The release is accepted when all 12 individual entries are discoverable in all three generated marketplaces, representative skills load in Claude Code and Codex, Skills CLI lists all 12 for Cursor and portable clients, generated artifacts have no drift, and rollback is documented.

Native Cursor Marketplace publication is not part of the private release. Cursor's documented submission workflow requires a public Git repository and platform review; use Skills CLI for the private phase and retain `.cursor-plugin` artifacts as publication-ready inputs.

## Rollback

- Pin or restore the previous known-good repository revision.
- Remove the candidate from the affected scope.
- Reinstall the previous skill entry or aggregate plugin.
- Verify discovery and one critical behavior case.
- Record the incident and block the faulty version.

Do not delete the migration archive until at least two successful release cycles or 14 days, whichever is longer.
