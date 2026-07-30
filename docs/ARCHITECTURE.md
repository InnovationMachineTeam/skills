# Architecture

## Distribution views

```text
skills/metaskills/*
        │
        ├── generate_marketplace.py ──> .claude-plugin/marketplace.json
        │                                one entry per skill
        │
        └── build_plugin_bundle.py ───> plugin/
                                         aggregate local plugin
```

The canonical tree is compatible with skill.sh's one-category discovery model. Claude Code receives individual shared-root entries for selective installation. The aggregate plugin is a generated self-contained copy for local and integration testing.

## Naming

- Marketplace: `im-skills`.
- Individual entry: exact skill name.
- Aggregate plugin: `im-skills-all`.
- Category: `metaskills`.

Install example: `skill-architect@im-skills`.

Category is not part of the skill identity and does not prevent collisions. Every skill name must be globally unique across the aggregate plugin.

## Version authority

Individual entry versions are generated from `metadata.version`. The aggregate plugin has an independent release version because it is a distinct installable/test artifact. CI checks generated drift, and releases include an upgrade test from the previous known-good version.

## Portability

Each installed skill must contain all required scripts, references, prompts, assets, evals, and host metadata. Parent references, absolute local runtime paths, symlinks, `.DS_Store`, bytecode, and VCS internals are excluded or rejected.
