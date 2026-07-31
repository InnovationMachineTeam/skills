#!/usr/bin/env python3
"""Synchronized CLAUDE.md and AGENTS.md instruction-pair gates."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_repository import validate_instruction_pairs


class InstructionPairTests(unittest.TestCase):
    def test_repository_pairs_are_complete_and_identical(self) -> None:
        self.assertEqual([], validate_instruction_pairs(ROOT))

    def test_missing_peer_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "CLAUDE.md").write_text("instructions\n", encoding="utf-8")
            self.assertEqual(
                [".: instruction pair is missing AGENTS.md"],
                validate_instruction_pairs(root),
            )

    def test_divergent_peer_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "CLAUDE.md").write_text("one\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("two\n", encoding="utf-8")
            self.assertEqual(
                [".: CLAUDE.md and AGENTS.md must be byte-identical"],
                validate_instruction_pairs(root),
            )


if __name__ == "__main__":
    unittest.main()
