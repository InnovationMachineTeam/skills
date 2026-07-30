# Composition and Merge

Prefer `COMPOSE` when component skills remain useful alone, carry different permissions, evolve independently, or can fail independently. The composer should route and coordinate rather than duplicate implementation.

Use `MERGE` only when maintaining separate discovery contracts creates more ambiguity than value and a single lifecycle is justified. Analyze permission union, context bloat, trigger collisions, resource conflicts, state ownership, rollback, and consumer migration.

Never merge solely because names, topics, authors, or files overlap.
