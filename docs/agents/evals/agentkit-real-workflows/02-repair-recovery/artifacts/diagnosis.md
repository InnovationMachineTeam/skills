# Diagnosis: agentkit-release-steward authority defect

Target: `agentkit-release-steward@0.1.0`, hash
`sha256:cfdbc8cb4952cdd5f365475474213f4941f84cc21586a7d4b33892591eed673b`.

The failure reproduces deterministically: the mission permits reading the
repository and writing only declared evaluation documents, while the candidate
permission list includes `repository:write`. The root cause is an overly broad
capability declaration, not routing, model choice, documentation containment or
runtime behavior.

Minimal repair: replace `repository:write` with `docs:evaluation-write`, retain
all mission, stop, test and review constraints, increment the candidate patch
version, then rerun the frozen layers. Rollback is the immutable 0.1.0 artifact;
neither version is registered or active.
