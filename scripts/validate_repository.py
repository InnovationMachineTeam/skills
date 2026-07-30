#!/usr/bin/env python3
"""Run deterministic repository-level marketplace checks."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from validate_marketplace import validate_marketplace


LOCAL_PATH = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\\\)")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures: list[str] = []
    findings, inventory = validate_marketplace(root)
    failures.extend(f"{item.code}: {item.path}: {item.message}" for item in findings if item.level == "FAIL")
    skills = inventory["skills"]
    if len(skills) != 12:
        failures.append(f"expected 12 skills, found {len(skills)}")

    manifest = json.loads((root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    plugins = manifest.get("plugins", [])
    if len(plugins) != len(skills):
        failures.append(f"expected {len(skills)} marketplace entries, found {len(plugins)}")
    if {item["name"] for item in plugins} != {item["name"] for item in skills}:
        failures.append("marketplace entries do not match canonical skills")

    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == "build":
            continue
        if path.is_symlink():
            failures.append(f"symlink is not allowed: {relative}")
        if path.name in {".DS_Store"} or path.name == "__pycache__" or path.suffix == ".pyc":
            failures.append(f"non-runtime artifact: {relative}")
        if path.is_file() and "evals" not in relative.parts and path.suffix in {".json", ".yaml", ".yml"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            if LOCAL_PATH.search(text):
                failures.append(f"absolute local path in machine-readable file: {relative}")

    check = subprocess.run(
        [sys.executable, str(root / "scripts" / "generate_marketplace.py"), str(root), "--check"],
        text=True,
        capture_output=True,
        check=False,
    )
    if check.returncode:
        failures.append(check.stderr.strip() or check.stdout.strip() or "marketplace generation check failed")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS repository: {len(skills)} skills, {len(plugins)} individual marketplace entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
