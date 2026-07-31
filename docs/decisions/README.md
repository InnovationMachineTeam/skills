# Decision Records

Decision records are append-mostly. Use `proposed`, `accepted`, `rejected`,
`superseded` or `deprecated`; preserve rejected alternatives and consequences.

The default subject-first layout is:

```text
docs/decisions/
├── architecture/  # architecture decision records (ADRs)
├── product/       # only when product decisions need independent records
├── security/      # only when security decisions need independent records
├── data/          # only when data decisions need independent records
└── agents/        # only when agent-governance decisions need independent records
```

Do not create unused branches. `docs/decisions/architecture/` is preferred over
`docs/decisions/adr/`: architecture is the decision subject, while ADR is the
record format. Existing projects keep their established convention unless a
reviewed migration updates every consumer and link.
