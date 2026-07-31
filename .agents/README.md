# Agent and Codex Metadata Root

This repository currently uses `.agents/plugins/marketplace.json` as the
generated Codex repo-marketplace manifest. Project-local agent systems may also
use `.agents/definitions/`, but definitions are created only from an approved
agent or team specification and remain separate from public marketplace skills.

Do not edit the generated marketplace manifest directly. Private agent skills
and commands must stay below their owner definition, declare one allowed
consumer, and remain excluded from marketplace packaging.
