# Testing

## Test layers

| Layer | Purpose |
|---|---|
| Static skill validation | frontmatter, names, versions, paths, references |
| Repository validation | canonical/generated drift, manifests, registries, instruction pairs |
| Unit tests | builders, adapters, dependencies, lifecycle scripts, agentkit contracts |
| Behavior and routing evals | trigger precision, non-triggering, expected artifacts |
| E2E workflow evidence | complete user outcome across real specialist routes |
| Host validation | Claude Code, Codex, Cursor, and portable discovery |
| Upgrade/rollback | version comparison, staged replacement, preserved prior state |

## Full local suite

```bash
python3 scripts/validate_documentation.py .
python3 scripts/validate_repository.py .
python3 scripts/validate_marketplace.py .
python3 scripts/manage_agent_assets.py validate .
python3 scripts/generate_agent_adapters.py tests/fixtures/agent-assets --check
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

Host tools should be run only when installed:

```bash
npx skills add . --list
claude plugin validate .
claude plugin validate ./plugin --strict
codex plugin marketplace add .
codex plugin list --available --json
```

## Documentation verification

Check Markdown links, referenced files, commands, catalogue versions, and
generated boundaries. Scan changed documentation for credential-like values.
`CLAUDE.md` and `AGENTS.md` must both exist and be byte-identical at each level
where either is present.

## Writing new tests

Add deterministic tests under `tests/test_*.py`. Negative cases should prove
that unsafe, stale, unauthorized, incomplete, or misrouted input fails closed.
Separate deterministic router fixtures from semantic workflow observations and
preserve raw evidence for release claims.

## Acceptance

Do not average away blocker failures. Security, permission, registry integrity,
private-skill visibility, rollback, and required outcome failures block release
even when aggregate scores are high.
