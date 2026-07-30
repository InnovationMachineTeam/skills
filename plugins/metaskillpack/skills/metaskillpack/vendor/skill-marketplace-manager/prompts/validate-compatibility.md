# Route: validate-compatibility

Validate in layers:

1. Agent Skills structure and metadata.
2. Catalog uniqueness, category depth, links, manifests, and version policy.
3. skill.sh discovery.
4. Claude marketplace validation.
5. Aggregate plugin strict validation and local load.
6. Trigger, behavior, upgrade, rollback, and security tests.

Record every check as `PASS`, `WARN`, `FAIL`, or `NOT RUN`, with command/tool, artifact, and evidence. Do not collapse absent tooling into success. In verify mode, return a remediation plan but do not alter files.
