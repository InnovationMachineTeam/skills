# Metadata and Discovery Diagnostic Prompt

Apply after [base.md](base.md).

Check folder/name identity, frontmatter delimiters and keys, description length and trigger language, client discovery paths, UI metadata, default invocation, installed-skill collisions, and stale caches.

Reproduce discovery separately from execution. Include direct positives, paraphrased positives, adjacent negatives, ambiguous requests, and collisions. Determine whether the skill is absent, invalid, undiscoverable, or merely poorly routed.

Repair only the failing metadata or installation path. Do not rewrite the body when selection is the confirmed defect. Rerun the same discovery cases before reporting recovery.

