# Master Prompt For Agent Capability Placement

Run after the task/capability graph and before creating an agent skill or command.
The goal is to choose the minimal form and avoid bloating the public skill catalog.

## Input

You will receive the capability contract, intended consumers, owner agent, triggers,
resources, tools, state, risk, eval needs, target hosts, public/private roots,
registry/map, and mutation authority. If the owner or consumers are materially unclear,
ask one to three focused questions.

## Decision

Choose exactly one:

- `INLINE` — a short stable rule without resources/tests/lifecycle;
- `PRIVATE_COMMAND` — one agent, a narrow named action or template;
- `PRIVATE_SKILL` — one agent, a reusable multi-step capability with resources,
  scripts, or evals;
- `PUBLIC_SKILL` — two independent consumers or an independent owner/contract/
  release lifecycle;
- `TOOL_SCRIPT` — deterministic execution is the dominant constraint;
- `WORKFLOW` — durable stages/state/coordination are the dominant constraint;
- `USE_EXISTING` or `REJECT`.

Explain why the next simpler form is insufficient. Similar wording,
prompt length, or a desire to "split things into folders" does not by itself justify
a skill.

## Placement And Visibility

```text
.agents/skills/<skill>/                         # public project skill
.agents/definitions/<agent>/skills/<skill>/    # private agent skill
.agents/definitions/<agent>/commands/<name>.md # private agent command
```

Marketplace public skills may live in `skills/<category>/<skill>/`.
The private root is never added to global discovery. Private describes the scope
of use; repository permissions and runtime policy separately handle
confidentiality.

## Output

Return the decision, rationale, owner/consumers, primary archetype when applicable,
canonical path, registry/map effect, agent-version effect, required evals,
loader rule, and the next prompt:

- private command → `agent-private-command.md`;
- private/public skill → primary archetype prompt +
  `agent-private-skill.md` when private;
- promotion/demotion → `agent-skill-visibility-migration.md`.
