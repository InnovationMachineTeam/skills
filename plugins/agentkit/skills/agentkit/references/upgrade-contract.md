# Agentkit upgrade contract

1. Compare `donors.json` with exact canonical donor paths read-only.
2. Exit without rewriting when versions and hashes are current.
3. Treat missing, invalid or unexpected donors as blocking drift.
4. For any change, inventory interfaces, documentation contracts, modes,
   authority, dependencies and eval assets before copying.
5. Build a complete candidate in a new staging directory; never patch the
   active pack in place.
6. Re-run donor validators, agentkit routing/behavior/scripts, E2E regression
   and protected pack holdout.
7. Require a migration decision for breaking donor interface changes.
8. Promote only with exact lifecycle authority and retain the previous pack as
   rollback.

The upgrade process may read canonical donors. It must not edit, fetch,
substitute, install, publish or delete them by assumption.
