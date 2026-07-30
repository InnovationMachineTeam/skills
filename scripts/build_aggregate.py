#!/usr/bin/env python3
"""Build the aggregate plugin using the authoritative release configuration."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    config = json.loads((root / "catalog" / "release.json").read_text(encoding="utf-8"))
    plugin = config["aggregate_plugin"]
    command = [
        sys.executable,
        str(root / "scripts" / "build_plugin_bundle.py"),
        str(root),
        str(args.output.resolve()),
        "--plugin-name",
        plugin["name"],
        "--display-name",
        plugin["display_name"],
        "--version",
        plugin["version"],
        "--description",
        plugin["description"],
        "--author-name",
        config["publisher"]["brand"],
        "--author-email",
        config["reviewer"]["email"],
        "--author-url",
        config["publisher"]["url"],
        "--repository-url",
        config["distribution"]["repository_url"],
        "--license",
        config["distribution"]["license"],
        "--codex-category",
        config["distribution"]["codex_category"],
        "--keyword",
        "agent-skills",
        "--keyword",
        config["category"],
    ]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(1)
