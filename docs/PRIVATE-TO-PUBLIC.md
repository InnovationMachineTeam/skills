# Private-to-public checklist

The repository begins private. Do not change visibility until every item below is approved.

## Legal and provenance

- choose and add an explicit public license;
- review every imported reference, prompt, script, fixture, and asset for redistribution rights;
- preserve required attribution and upstream licenses;
- remove confidential company material and customer data.

## Security and privacy

- scan repository history as well as the current tree for secrets;
- remove personal absolute paths, private endpoints, internal repository names, and sensitive traces;
- review scripts and tool permissions;
- publish a supported security-reporting channel;
- verify that generated bundles contain no excluded files.

## Product and compatibility

- document supported harness versions;
- test from a clean account without InnovationMachineTeam access;
- test every individual entry and the aggregate plugin;
- document channel-collision behavior with skill.sh;
- freeze public install names or publish a compatibility policy.

## Governance

- approve license and visibility through InnovationMachineTeam;
- confirm maintainers and response expectations;
- enable branch protection and required checks;
- define deprecation, quarantine, and support policies;
- create public release notes and migration guidance.

Only the repository owner changes visibility after a signed review by `@stanislavus86`.
