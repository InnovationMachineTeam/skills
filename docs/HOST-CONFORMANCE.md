# Agent capability host conformance

Checked: 2026-07-31. Re-verify before a host-specific release.

## Canonical contract

Canonical assets remain host-neutral. An adapter returns one of:

- `native`: host enforces the required scope directly;
- `generated`: a deterministic agent-specific projection enforces the scope;
- `unsupported`: no safe projection exists, so activation is blocked.

Private means scoped loading, not filesystem confidentiality. Marketplace and
global skill scanners must never receive private roots.

## Matrix

| Host | Public skills | Agent definitions | Strict private skill | Private command | Adapter decision |
|---|---|---|---|---|---|
| Codex | Native `.agents/skills` discovery | Native `.codex/agents/*.toml` | Exact path through agent-local `skills.config`; verify target version | Generated into agent instructions | native skill / generated command |
| Claude Code | Native `.claude/skills`; plugin skills | Native `.claude/agents/*.md` and plugin agents | `skills` only preloads and does not restrict later Skill access | Commands are global/project/plugin components | generated: deny Skill tool and embed private assets |
| Cursor | Agent Skills supported in editor/CLI | Custom subagents supported | Native isolation not assumed | Native isolation not assumed | generated agent projection until conformance fixture passes |

## Codex evidence and constraints

The current official Codex manual documents repository skill discovery only
from `.agents/skills` roots. Project custom agents live in `.codex/agents/` and
may override `skills.config`, whose entries contain an exact skill path and an
enabled flag. Therefore private skills stay outside scanned roots and are
attached only in the owning custom-agent configuration. A private command is
rendered into `developer_instructions` because Codex does not document an
agent-private command directory.

Sources:

- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://developers.openai.com/plugins/build/skills

## Claude Code evidence and constraints

Subagent frontmatter supports `skills`, but the field preloads content rather
than restricting accessible skills. A subagent can still invoke other project,
user and plugin skills through the Skill tool. Strict private mode therefore
omits or denies Skill and injects the exact private capability into the
generated agent body. Plugin agents do not support all local-agent controls, so
adapter validation is mandatory.

Sources:

- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/slash-commands
- https://code.claude.com/docs/en/plugins-reference

## Cursor evidence and constraints

Cursor supports Agent Skills and custom subagents, but the web documentation
available to this implementation does not establish a stable per-agent skill
allow-list contract. The baseline adapter embeds private capability text in the
generated `.cursor/agents/<agent>.md` projection and keeps private roots outside
global skill locations. Native attachment may replace this only after a pinned
version passes the same access fixtures.

Sources:

- https://cursor.com/docs/subagents
- https://cursor.com/changelog/2-4
- https://cursor.com/changelog/2-5

## Required conformance cases

1. Owning agent can use the private skill.
2. Another agent cannot discover or bind it.
3. Global skill selectors do not list it.
4. Missing owner, stale hash or unverified adapter blocks activation.
5. Public skill remains available to approved project consumers.
6. Marketplace packages contain no private assets.
