# Policy contract

A decision binds subject, asset, action, exact target, environment, data class,
risk tier, policy version, run/action IDs, nonce, issue/expiry, conditions,
approvals and obligations. The enforcement point consumes the decision once and
records outcome; it cannot broaden the action.

`ALLOW` requires a satisfied matching rule. `REQUIRE_APPROVAL` requires named
approval roles and remains non-executable until verified. Missing, conflicting,
stale or ambiguous inputs yield `DENY`.
