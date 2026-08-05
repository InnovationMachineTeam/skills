# Practice Conflicts and Resolutions

Most differences are not factual contradictions, but different points on the
risk/complexity/interactivity spectrum. The decisions below are recorded so that
Agent OS does not inherit conflicting rules.

## Workflow or agent

**Difference:** deterministic workflows are predictable; autonomous agents are
flexible.

**Resolution:** code owns lifecycle, budgets, policies, and irreversible gates;
the agent solves ambiguous local tasks. Start with a workflow/single agent and
increase complexity based on eval evidence.

## One agent or many

**OpenAI/Anthropic:** keep it as simple as possible with a single agent first.

**Implementations:** GSD/BMAD/gstack actively specialize roles.

**Resolution:** specialization is justified by context isolation, distinct
permissions, tool confusion, independent verification, or parallel speedup.
Thematic separation alone is not sufficient.

## Rigid phases or fluid actions

**GSD/BMAD/Spec Kit:** sequential artifacts and gates.

**OpenSpec/ADLC:** iterative actions; ADLC modes operate in parallel.

**Resolution:** dependencies and assurance gates are mandatory; phase blocking
is not. An artifact graph permits return and iteration. Lite/standard/
high-assurance policies choose the level of strictness.

## Requirements or bets

**Classic SDLC:** requirements describe expected behavior.

**ADLC:** bets record the unknown and the resolution signal.

**Resolution:** bets apply before the problem/solution is confirmed;
requirements apply to the selected generation target and mandatory constraints.
A bet trace connects learning to the subsequent spec.

## Thin orchestrator or active manager

**GSD:** the orchestrator does not touch source files.

**Manager pattern:** the manager synthesizes and may do part of the work.

**Resolution:** the orchestrator MUST not duplicate dispatched tasks. It MAY
perform small integration operations if ownership is explicit and this does not
pollute context. Default: thin.

## Agents as tools or handoffs

**Difference:** the manager keeps user-facing ownership; a handoff transfers it
to the specialist.

**Resolution:** use agents-as-tools for bounded subtasks and a single final
answer; use handoff for full ownership of the next phase. Route history and max
transitions are mandatory.

## Team or parallel subagents

**Difference:** a team provides peer communication; subagents return to a lead.

**Resolution:** if participants do not need to coordinate directly, fan-out/
fan-in is simpler. Use a team only for genuine shared problem-solving/task
board work.

## Worktree as isolation

**Marketing perception:** a separate worktree looks like a safe environment.

**Platform details:** `.git`, plugins, approvals, or credentials may still be
shared.

**Resolution:** a worktree provides change/collision isolation. A security
boundary is sandboxing plus identity plus filesystem/network policy. Shared
resources must be documented.

## Memory or stateless agents

**Memory benefit:** continuity and learning.

**Risk:** poisoning, staleness, privacy, and hidden dependency.

**Resolution:** raw sessions do not become memory. Candidate -> verify ->
approve; provenance, scope, TTL, owner, and revocation are mandatory. Canonical
docs/state take priority over memory.

## Link to a standard or copy it

**Link:** stays current, but harms portability/reproducibility.

**Copy:** self-contained, but becomes stale.

**Resolution:** an active workflow reads the canonical reference; an immutable
run/spec records a version/digest or snapshot. A dependency graph marks stale
copies.

## Markdown state or database

**Markdown:** transparent to humans, git-friendly.

**DB:** transactions, concurrency, and queries.

**Resolution:** use a canonical structured store for runtime state and a
Markdown projection for review. In a small single-writer workflow, Markdown is
acceptable with schema/atomic-write/lock checks.

## Automatic gates or human review

**ADLC:** loops over gates, continuous signals.

**High-assurance:** blocking approvals.

**Resolution:** automated continuous validation everywhere; a human gate only
for accountability, irreversible/high-impact action, and genuine judgment. It
must not repeat the automated checklist.

## LLM verifier or deterministic test

**LLM:** sees meaning and coherence.

**Test:** reproducible and verifies observable behavior.

**Resolution:** deterministic evidence takes priority; the LLM links claims,
finds gaps, and evaluates judgment cases. A critical pass must not rely only on
the LLM.

## Fail-open or fail-closed

**OpenSpec lite:** verification warnings do not block archiving.

**Security/GSD:** uncertainty often requires human_needed/block.

**Resolution:** policy is set by risk class. Low reversible risk: accept and
flag. High/critical risk: fail-closed or accountable approval. Status is never
hidden.

## Full context or progressive loading

**Full context:** lower risk of omission.

**Progressive disclosure:** less context rot/cost.

**Resolution:** a compact context spine plus index is mandatory; details are
retrieved by relevance. Critical constraints are duplicated in the task
envelope, while the canonical source remains linked.

## "Boil the ocean" or minimalism

**gstack:** AI lowers marginal cost, so it is worth doing the complete thing.

**Anthropic/GSD Pi/OpenSpec:** complexity and ceremony only when needed.

**Resolution:** completeness applies to the agreed outcome and important edge
cases, not to unlimited scope. Budget, non-goals, and diminishing returns bound
the work.

## Numeric platform limits

Nesting depth, number of teammates, context size, and inherited permissions
vary and change.

**Resolution:** do not embed vendor limits in universal architecture. Maintain a
runtime capability matrix and choose stricter internal limits.

## Final policy for resolving new conflicts

1. Determine whether it is a fact, a trade-off, or a platform limitation.
2. Compare scope, risk tier, and source dates.
3. Prefer the primary/current official source for facts.
4. For trade-offs, use eval evidence and a reversible default.
5. For high-impact ambiguity, require a human decision and an ADR.
6. Record the exception, owner, and review date.
