# Contributing

## Change one skill

1. Work in `skills/metaskills/<skill>/`.
2. Preserve the skill's capability and authority boundary unless the change explicitly redesigns it.
3. Update or add routing, behavior, script, security, and regression evals as appropriate.
4. Bump `metadata.version` when installed content changes.
5. Regenerate all marketplace manifests, individual plugin packages, and the aggregate plugin.
6. Run repository and harness-native validators.
7. Include evidence and rollback notes in the pull request.

## Add a skill

- Use a globally unique lowercase kebab-case name.
- Keep the skill self-contained and at `skills/metaskills/<name>/SKILL.md`.
- Add its name and tags to `catalog/entries.json`.
- Add its catalog row to `README.md`.
- Regenerate distribution artifacts.
- Demonstrate Skills CLI discovery plus representative Claude Code, Codex, and Cursor loading in isolated scopes.

## Generated artifacts

Do not manually edit:

- `.claude-plugin/marketplace.json`;
- `.agents/plugins/marketplace.json`;
- `.cursor-plugin/marketplace.json`;
- `plugins/`;
- `plugin/`;
- `plugin/build-manifest.json`.

Generated diffs must be committed with the canonical change that produced them.

## Review checklist

- no secret, personal local path, symlink, or parent-directory runtime dependency;
- name, directory, and entry agree;
- versions are intentionally bumped;
- trigger neighbors and negative cases were checked;
- scripts are reviewed before execution;
- private-source rights and provenance are known;
- installation does not duplicate an active skill from another channel;
- rollback points to a known-good version.
