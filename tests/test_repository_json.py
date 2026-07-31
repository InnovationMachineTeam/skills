#!/usr/bin/env python3
"""Ensure every committed repository JSON document is syntactically valid."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_TOP_LEVEL = {".git", "build"}


class RepositoryJsonTests(unittest.TestCase):
    def test_all_repository_json_parses(self) -> None:
        failures: list[str] = []
        for path in ROOT.rglob("*.json"):
            relative = path.relative_to(ROOT)
            if relative.parts and relative.parts[0] in EXCLUDED_TOP_LEVEL:
                continue
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(f"{relative.as_posix()}: {exc}")
        self.assertEqual([], failures)

    def test_schema_required_fields_have_declared_properties(self) -> None:
        failures: list[str] = []

        def walk(value: object, path: str, source: Path) -> None:
            if isinstance(value, dict):
                required = value.get("required")
                properties = value.get("properties")
                if isinstance(required, list) and isinstance(properties, dict):
                    missing = sorted(set(required) - set(properties))
                    if missing:
                        failures.append(f"{source}: {path} missing properties {missing}")
                for key, child in value.items():
                    walk(child, f"{path}/{key}", source)
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    walk(child, f"{path}/{index}", source)

        for path in (ROOT / "docs" / "schemas").glob("*.schema.json"):
            walk(json.loads(path.read_text(encoding="utf-8")), "#", path.relative_to(ROOT))
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
