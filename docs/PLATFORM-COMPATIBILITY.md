# Codex and Cursor plugin compatibility

Last reviewed: 2026-07-30.

## Decisions

1. Keep `skills/metaskills/` as the only editable skill source.
2. Generate one self-contained package per skill under `plugins/`.
3. Put only the manifest inside each host-specific hidden directory; keep skills and other components at the plugin root.
4. Use a native repo marketplace for each host instead of relying on another host's compatibility parser.
5. Keep every marketplace entry individually installable and explicitly versioned.
6. Include publisher, repository, license, category, and discovery metadata wherever the host schema supports it.
7. Declare no hooks, MCP servers, commands, agents, variables, or apps until the corresponding files exist and receive a security review.
8. Reject absolute paths, `..` traversal, symlinks, secrets, generated cache files, and bundle drift.

## Codex contract

- Repo marketplace: `.agents/plugins/marketplace.json`.
- Plugin manifest: `.codex-plugin/plugin.json`.
- Marketplace `source.path` begins with `./`, stays inside the marketplace root, and points to `./plugins/<name>`.
- Every entry declares `policy.installation`, `policy.authentication`, and `category`.
- Each package uses `skills/` with immediate skill children.
- Rich interface metadata is included, but optional legal or visual URLs are omitted until real assets and approved policies exist.
- Local/repo sources are private authoring and team-distribution channels; public publication is a separate review process.

Official references:

- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [Codex CLI command reference](https://developers.openai.com/codex/cli/reference)

## Cursor contract

- Multi-plugin marketplace: `.cursor-plugin/marketplace.json` at repository root.
- Plugin manifest: `.cursor-plugin/plugin.json` inside each `plugins/<name>/` package.
- Marketplace sources are relative subdirectories such as `plugins/skill-architect`.
- Manifest paths are relative, contain no `..`, and point to real components.
- Each package includes a README, clear description, SemVer, author, repository, proprietary license identifier, keywords, and explicit `skills` path.
- Cursor automatically discovers each immediate skill subdirectory under `skills/`; the explicit path replaces fallback discovery and therefore must remain correct.
- Native Cursor Marketplace submission stays blocked while the repository is private because Cursor's documented submission flow requires a public Git repository and review.

Official references:

- [Cursor Plugins Reference](https://cursor.com/docs/reference/plugins)
- [Cursor Marketplace submission](https://cursor.com/marketplace/publish)

## Validation matrix

| Check | Claude Code | Codex | Cursor | Portable clients |
|---|---:|---:|---:|---:|
| Native marketplace entry point | yes | yes | yes | n/a |
| Native per-plugin manifest | yes | yes | yes | `SKILL.md` |
| One installable package per skill | yes | yes | ready for publication | yes |
| Deterministic rebuild and drift check | yes | yes | yes | yes |
| Path, symlink, secret, and metadata checks | yes | yes | yes | yes |
| Native validator in local release gate | Claude CLI | plugin-creator validator | structural + local Cursor test | Skills CLI |

## Private-to-public gate

Before public release:

1. Replace the proprietary license notice with an approved public license and update generated manifest values.
2. Recheck every skill and script for confidential material, provenance, and third-party rights.
3. Add approved logo assets and public support, privacy, and terms URLs only if they are accurate.
4. Run clean installs in Claude Code, Codex, Cursor, and at least one portable Agent Skills client.
5. Submit Cursor plugins only after the repository is public; treat Cursor review as a separate approval gate.
6. Use immutable tags for release evidence and preserve a tested rollback revision.
