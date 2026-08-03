# Governance

## Roles

| Role | Identity | Responsibility |
|---|---|---|
| Repository owner | `InnovationMachineTeam` | Access, settings, visibility, branch protection, emergency actions |
| Technical publisher | `InnovationMachineTeam` | Tags, releases, marketplace publication, rollback |
| Company steward | `InnovationMachine` | Product direction, brand, public-release approval |
| Lead maintainer and required reviewer | `@stanislavus86` | Architecture, code review, release evidence, security triage |
| Security contact | `stanislav.usoltsev@gmail.com` | Private vulnerability reports and incident coordination |

The GitHub organization is the publisher because it owns the repository and credentials. InnovationMachine remains the company and product identity. Personal credentials must not be the sole publication mechanism.

## Public contacts

| Channel | Languages |
|---|---|
| [LinkedIn — Stanislav Us](https://www.linkedin.com/in/stanislavus/) | English, Russian |
| [X — @stanislavus86](https://x.com/stanislavus86) | English, Russian |
| [Telegram — @stanislavus86](https://t.me/stanislavus86) | English, Russian |
| [Telegram — Innovation Machine](https://t.me/InnovationMachine) | Russian |

Use these channels for public project and company communication. Report vulnerabilities privately through the security contact listed in [SECURITY.md](SECURITY.md).

## Decision policy

- Changes to one skill require its validator/evals and review by `@stanislavus86`.
- Marketplace topology, install identifiers, visibility, licensing, or release-policy changes require repository-owner approval.
- Generated files must be reproducible from canonical sources.
- Publication and archive retirement are separate approvals.
- Emergency quarantine may be performed by the repository owner, followed by a documented review.

## Branch protection recommendation

After the first push, protect `main` with:

- pull requests required;
- `validate` workflow required;
- one approving review from `@stanislavus86`;
- stale approvals dismissed after new commits;
- force pushes and branch deletion disabled;
- administrator bypass reserved for security recovery.

## Source of truth

`skills/metaskills/` is canonical. `.claude-plugin/marketplace.json` and `plugin/` are generated distribution views. Conflicts are resolved in favor of the canonical skill tree and catalog configuration.
