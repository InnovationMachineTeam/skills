#!/usr/bin/env python3
"""Normalize a metaskillpack command without executing a donor."""

from __future__ import annotations

import json
import shlex
import sys


MODES = {
    "create": ("skill-architect", None),
    "scout": ("skill-scout", None),
    "research": ("skill-harvester", "context-build"),
    "optimize": ("skill-optimizer", None),
    "doctor": ("skill-doctor", None),
    "manage": ("skill-manager", None),
    "harvest": ("skill-harvester", None),
    "refactor": ("skill-refactor", None),
    "evaluate": ("skill-evaluator", None),
    "run": ("skill-builder", None),
    "compare": ("skill-harvester", "pairwise-skill-comparison"),
    "intake": ("skill-harvester", "external-skill-intake"),
    "prompt": ("prompt-optimize", None),
    "practices": ("skill-best-practices", None),
    "marketplace": ("skill-marketplace-manager", None),
    "status": (None, "native"),
    "route": (None, "native"),
    "upgrade": (None, "native"),
    "help": (None, "native"),
}

ALIASES = {
    "discover": "scout",
    "context": "research",
    "fix": "doctor",
    "test": "evaluate",
    "orchestrate": "run",
    "skillify": "run",
    "lifecycle": "manage",
    "collect": "harvest",
    "adopt": "intake",
}

REQUIRES_TARGET = {
    "create",
    "research",
    "optimize",
    "doctor",
    "manage",
    "harvest",
    "refactor",
    "evaluate",
    "compare",
    "intake",
}


def main() -> int:
    tokens = sys.argv[1:]
    if tokens and tokens[0] in {"--json", "--"}:
        tokens = tokens[1:]
    if len(tokens) == 1 and any(character.isspace() for character in tokens[0]):
        tokens = shlex.split(tokens[0])
    if tokens and tokens[0] in {"$metaskillpack", "metaskillpack"}:
        tokens = tokens[1:]

    if not tokens:
        result = {
            "status": "clarify",
            "canonical_mode": "help",
            "message": "No mode supplied; show help and ask for the desired outcome.",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    supplied_mode = tokens[0].lower()
    canonical_mode = ALIASES.get(supplied_mode, supplied_mode)
    if canonical_mode not in MODES:
        result = {
            "status": "unknown",
            "supplied_mode": supplied_mode,
            "known_modes": sorted(MODES),
            "known_aliases": ALIASES,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    donor, route = MODES[canonical_mode]
    remaining = tokens[1:]
    status = "ready"
    message = None
    if canonical_mode in REQUIRES_TARGET and not remaining:
        status = "clarify"
        message = f"Mode {canonical_mode!r} requires a named skill, source, or task target."
    if canonical_mode == "compare" and len(remaining) < 2:
        status = "clarify"
        message = "Mode 'compare' requires two named skills or paths."

    result = {
        "status": status,
        "supplied_mode": supplied_mode,
        "canonical_mode": canonical_mode,
        "alias_used": supplied_mode != canonical_mode,
        "donor": donor,
        "donor_route": route,
        "arguments": remaining,
        "message": message,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == "ready" else 2


if __name__ == "__main__":
    sys.exit(main())
