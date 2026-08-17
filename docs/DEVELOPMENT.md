# Development

## Canonical edit workflow

1. Work from an up-to-date branch.
2. Edit a canonical skill under `skills/<category>/<name>/` or canonical catalog
   and registry data.
3. Update `metadata.version` when an installed skill contract or content changes.
4. Keep `CLAUDE.md` and `AGENTS.md` identical at every level you touch.
5. Reconcile public skill versions and content hashes with the agent asset
   registry, render its generated view, then validate dependencies and assets.
6. Build individual and aggregate packages into new staging directories.
7. Validate staged artifacts before replacing committed generated output.
8. Run the complete repository test suite and review the diff.

## Commands

```bash
python3 scripts/manage_skill_dependencies.py validate
python3 scripts/manage_skill_dependencies.py render --check
python3 scripts/manage_agent_assets.py sync-public . --accountable-owner InnovationMachineTeam --write
python3 scripts/manage_agent_assets.py render . --write
python3 scripts/manage_agent_assets.py validate .
python3 scripts/validate_repository.py .
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

Build into paths that do not already exist:

```bash
python3 scripts/build_individual_plugins.py . build/plugins-next
python3 scripts/generate_marketplace.py .
python3 scripts/build_aggregate.py . build/im-skills-all-next
```

## Documentation changes

Verify commands, paths, versions, and state claims against canonical files.
Update the documentation map when adding a new document domain. Add agent-system
findings to `docs/INSIGHTS-AGENT-SYSTEM-DESIGN.md` when they apply across use
cases rather than only to one implementation.

## Pull requests and releases

Use a focused branch and reviewable commits. Generated changes must be
reproducible from canonical input. Obtain the required review from
`@stanislavus86`. Installation, activation, publishing, deployment, and
repository visibility changes are separate authorized operations.
