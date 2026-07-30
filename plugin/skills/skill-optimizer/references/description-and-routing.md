# Description and Routing Optimization

## Contents

- Description contract
- Test matrix
- Diagnosis
- Optimization rules

## Description contract

Treat frontmatter metadata as routing code. The description should state:

- what capability the skill adds;
- concrete situations, artifacts, or user language that should trigger it;
- supported operations when ambiguity is likely;
- exclusions when neighboring skills collide.

Keep essential trigger information in the description because the body loads only after selection. Use specific nouns and verbs naturally. Do not keyword-stuff or repeat every paraphrase.

## Test matrix

Include:

- direct positives;
- paraphrased positives without the skill name;
- adjacent negatives;
- ambiguous cases requiring clarification;
- collisions with installed skills;
- compound requests;
- non-English phrasing when relevant.

Measure false-positive and false-negative cost separately. A rare high-consequence false positive may matter more than several benign misses.

## Diagnosis

- Missed direct and paraphrased positives suggest missing capability or trigger language.
- Adjacent false positives suggest generic verbs or absent exclusions.
- Correct trigger but poor execution indicates a body or workflow problem, not a description problem.
- Different results across clients may indicate host discovery differences rather than metadata quality.

## Optimization rules

- Change the smallest phrase able to address a measured routing gap.
- Keep a held-out routing set to detect overfitting.
- Do not broaden the description to include ordinary tasks the skill does not specialize in.
- Regenerate UI metadata when the skill's contract changes.
- Test the description independently from the body.

