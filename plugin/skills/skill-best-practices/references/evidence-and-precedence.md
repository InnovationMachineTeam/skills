# Evidence and precedence

## Authority tiers

1. **Portable normative:** current open Agent Skills specification.
2. **Platform normative:** current official host documentation for behavior on that host.
3. **Platform guidance:** official authoring, enterprise, API, plugin, and engineering recommendations.
4. **Official local contract:** bundled client skill-creator and validators for the current runtime.
5. **Exemplars:** public repositories such as gstack and gbrain.
6. **Derived synthesis:** prior reports and internal summaries.

Higher tier does not erase lower-tier evidence when scopes differ. A host can impose stricter constraints than the portable spec, but those constraints must remain labeled host-specific.

## Conflict rules

- Prefer the portable spec for what a portable package may contain.
- Prefer the target host for what that host accepts, loads, truncates, activates, or executes.
- Prefer enterprise guidance for organizational approval and security policy, not portable syntax.
- Treat engineering articles as architectural rationale unless they declare a current contract.
- Treat repositories as observed patterns and failure evidence, never as standards.
- Treat derived reports as indexes to primary evidence, not independent confirmation.

## Temporal rules

The newest source is not automatically authoritative. Verify canonical identity and scope. Pin procedures and deployed versions where stability matters; retrieve dynamic limits and platform behavior from current official sources at runtime.

## Citation rules

Every material practice must name at least one source ID. Conflicts must cite all material sides. If a source becomes unavailable, retain the last observed claim as historical evidence and mark current support unverified.
