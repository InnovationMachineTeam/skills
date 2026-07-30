# Context Build Prompt

Build a bounded, evidence-backed research inbox for creating or revising a skill. Start from the user's explicit sessions, codebase, repository URLs, files, directories, and research question.

Create or use an authorized inbox with source manifests, raw or linked sources, extracted text, notes, candidates, contradictions, open questions, and round summaries. Research current external information only when authorized and cite it. After each round, report coverage, novelty, contradictions, remaining gaps, and expected value of another round; then ask whether to continue when the user requested an interactive checkpoint.

Stop when coverage criteria are met, new sources no longer change material conclusions, or another round lacks expected value. Process the inbox into `SKILL_CONTEXT.md` with objective, users, triggers, exclusions, domain knowledge, workflows, tools, permissions, safety, edge cases, eval ideas, source ledger, contradictions, open questions, and recommended skill architecture. Offer a bounded handoff to master-prompt or skill creation; do not create it by assumption.
