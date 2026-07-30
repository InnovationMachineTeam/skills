# Route: release-distribution

Resolve repository, visibility, plugin/entry name, version, channel, pilot cohort, and rollback release before any external action.

Prepare the candidate, validate all release gates, test clean install and upgrade, generate release notes, and report unresolved blockers. External publish, organization rollout, global install, tag creation, and retirement require explicit authority.

After release, verify discoverability from the consumer path and retain the previous known-good artifact through the rollback window.
