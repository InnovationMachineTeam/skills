# Public repository status and hardening checklist

The repository is public. It was spun out of the agent and skill engineering
practices developed at Innovation Machine and is maintained by
InnovationMachineTeam as an independently consumable project.

Public visibility does not imply an open-source license. The repository keeps
the license declared in `catalog/release.json` until the owner approves a
separate licensing transition.

## Ongoing legal and provenance checks

- review every imported reference, prompt, script, fixture and asset for redistribution rights;
- preserve required attribution and upstream licenses;
- keep confidential company material and customer data out of the repository;
- reassess the license through an explicit owner decision rather than inferring it from public visibility.

## Security and privacy

- scan repository history and the current tree for secrets;
- exclude personal absolute paths, private endpoints, internal repository names and sensitive traces;
- review scripts and tool permissions;
- maintain a supported security-reporting channel;
- verify that generated bundles contain no excluded files.

## Product and compatibility

- document supported harness versions;
- test from a clean account without InnovationMachineTeam organization access;
- test every individual entry and the aggregate plugin;
- document channel-collision behavior with skill.sh;
- keep public install names stable or publish a compatibility policy;
- treat host marketplace submission and approval as separate from repository visibility.

## Governance

- confirm maintainers and response expectations;
- maintain branch protection and required checks;
- preserve deprecation, quarantine and support policies;
- create release notes and migration guidance for material public-contract changes.

Repository visibility is controlled by the owner. Host-native marketplace
publication, licensing and activation remain separate authorized transitions.
