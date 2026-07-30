# Artifact/Template Skill Master Prompt

Apply after [base.md](base.md). Design a skill whose primary value is producing or transforming a formatted artifact.

## Artifact contract

- Define the final file type, required structure, visual or semantic acceptance criteria, and editable versus rendered outputs.
- Store reusable templates, boilerplate, fonts, images, themes, or sample files in `assets/`.
- Treat assets as output ingredients, not instructions to load into context unless inspection is necessary.
- Preserve user content, formatting, formulas, metadata, and accessibility properties that are in scope.
- Separate content decisions from layout and rendering decisions.

## Workflow

Use an inspect → transform → render or execute → verify loop. Prefer editing an existing artifact over recreating it when preservation matters. Use dedicated format libraries or tools. Avoid manual binary manipulation unless the format requires it and deterministic support exists.

## Verification

Verify both structure and user-visible result. Depending on format, inspect schemas, links, formulas, page bounds, clipping, contrast, fonts, image resolution, speaker notes, accessibility, or executable behavior. Do not declare success from file creation alone.

## Evaluation

Test empty and dense content, long text, missing assets, unsupported fonts, format round-trips, preservation of unrelated elements, rendering at target dimensions, and clean failure without corrupting originals.
