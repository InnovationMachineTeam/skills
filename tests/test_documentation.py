#!/usr/bin/env python3
"""Canonical documentation link gates."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_documentation import validate


class DocumentationTests(unittest.TestCase):
    def test_repository_documentation_links_resolve(self) -> None:
        self.assertEqual([], validate(ROOT))

    def test_missing_local_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "docs").mkdir()
            (root / "docs" / "README.md").write_text(
                "[Missing](missing.md)\n", encoding="utf-8"
            )
            self.assertEqual(
                ["docs/README.md: missing local link target: missing.md"],
                validate(root),
            )

    def test_external_and_anchor_links_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text(
                "[Section](#section) [Web](https://example.com)\n",
                encoding="utf-8",
            )
            self.assertEqual([], validate(root))


if __name__ == "__main__":
    unittest.main()
