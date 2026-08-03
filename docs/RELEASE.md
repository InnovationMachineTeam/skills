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

## Public repository release

The public repository was spun out of Innovation Machine's agent and skill
engineering practices. A release is accepted when every canonical catalog
entry is discoverable in all three generated marketplaces, representative
skills load in Claude Code and Codex, Skills CLI lists the same inventory for
Cursor and portable clients, generated artifacts have no drift, and rollback
is documented. Do not hard-code the inventory count; derive it from
`catalog/entries.json`.

Public repository visibility satisfies the source-visibility prerequisite for
Cursor submission but does not prove platform publication. Use Skills CLI for
direct repository installation and retain `.cursor-plugin` artifacts as inputs
to the separate Cursor review process.

## Rollback

- Pin or restore the previous known-good repository revision.
- Remove the candidate from the affected scope.
- Reinstall the previous skill entry or aggregate plugin.
- Verify discovery and one critical behavior case.
- Record the incident and block the faulty version.

Do not delete the migration archive until at least two successful release cycles or 14 days, whichever is longer.
