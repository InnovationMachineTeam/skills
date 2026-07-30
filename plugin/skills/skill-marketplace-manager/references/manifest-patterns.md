# Manifest patterns

Use this reference before generating or editing marketplace and plugin manifests.

## Decision table

| Need | Pattern |
|---|---|
| Install one self-contained plugin | Plugin root with `.claude-plugin/plugin.json` |
| Offer selected categories from one repository | Root `.claude-plugin/marketplace.json`, shared-root entries, explicit `skills` paths, `strict: false` |
| Test all skills locally | Generated aggregate `plugin/` with category paths in `plugin.json` |
| Support skill.sh | Canonical `skills/<skill>` or `skills/<category>/<skill>` tree |

## Aggregate plugin

```json
{
  "name": "skill-toolkit",
  "displayName": "Skill Toolkit",
  "version": "1.0.0",
  "description": "Portable skill engineering toolkit",
  "skills": ["./skills/metaskills"]
}
```

Keep component paths relative to the plugin root. Put only `plugin.json` inside `.claude-plugin/`.

## Shared-root marketplace

```json
{
  "name": "skill-toolkit-marketplace",
  "owner": { "name": "Maintainers" },
  "plugins": [
    {
      "name": "metaskills",
      "source": "./",
      "strict": false,
      "version": "1.0.0",
      "category": "metaskills",
      "tags": ["skills", "governance"],
      "skills": "./skills/metaskills"
    }
  ]
}
```

For a root `source`, component paths form the complete entry definition. Do not rely on an unrelated root `plugin.json` to add components.

## Version policy

- Treat skill, plugin, and marketplace versions as separate release surfaces.
- Prefer one authoritative location for a plugin distribution version.
- If a version is duplicated, enforce equality in CI.
- Require a distribution version bump when installed content changes.
- Test upgrade from the previous release, not only clean installation.

## Validation commands

```bash
claude plugin validate .
claude plugin validate ./plugin --strict
npx skills add . --list
claude --plugin-dir ./plugin
```

Record absent tooling as `NOT RUN`.
