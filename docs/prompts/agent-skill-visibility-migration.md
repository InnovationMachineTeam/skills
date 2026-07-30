# Мастер-промпт migration private/public skill

Запускай через `skill-refactor`, когда current visibility не соответствует
реальным consumers и lifecycle.

## Promotion gate

`PROMOTE_PUBLIC` разрешён только когда approved independent consumer существует,
contract обобщён за пределы исходного agent, а independent
owner/evals/release cadence/lifecycle оправдывают public surface. Второй
consumer запускает assessment, но не даёт автоматического promotion. Удали owner-agent assumptions, stage public
candidate, назначь public identity/version, обнови registry/map/adapters,
проверь coexistence и consumers, затем retire private source через manager.

## Demotion gate

`DEMOTE_PRIVATE` разрешён только после inventory, доказавшего одного remaining
owner agent. Stage private candidate, задай owner и allowed consumers, обнови
agent version/registry/map/adapters, проверь global non-discovery и denial других
agents, затем retire public source.

## План и evidence

Верни exact source/destination hashes, consumers, contract diff, permissions,
file operations, registry/map diff, agent version effect, compatibility window,
host adapter changes, eval matrix, approvals, rollback и stop conditions.

Не реализуй migration простым move. Не утверждай, что private path обеспечивает
confidentiality. Lifecycle mutations выполняет `skill-manager` после independent
evaluation exact candidate.
