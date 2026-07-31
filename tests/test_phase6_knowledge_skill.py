#!/usr/bin/env python3
"""Forward and adversarial tests for the curated knowledge plane."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


GRAPH = module("phase6_graph", "skills/metaskills/agent-knowledge-manager/scripts/build_knowledge_graph.py")


def page(doc_id: str, status: str = "approved", related: str = "[]", sources: str = "[source://test]") -> str:
    return f"""---
id: {doc_id}
type: fact
status: {status}
owner: team
version: "1.0.0"
updated_at: 2026-07-31
review_at: 2026-10-31
sources: {sources}
related: {related}
tags: [test]
sensitivity: internal
agent_access: read
---

# Test fact

Verified body.
"""


class Phase6KnowledgeSkillTests(unittest.TestCase):
    def test_projection_preserves_provenance_and_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "knowledge"
            root.mkdir()
            (root / "fact.md").write_text(page("doc://knowledge/fact"), encoding="utf-8")
            first, failures = GRAPH.build(root, "2026-07-31T00:00:00Z")
            second, second_failures = GRAPH.build(root, "2026-07-31T00:00:00Z")
            self.assertEqual([], failures)
            self.assertEqual([], second_failures)
            self.assertEqual(first, second)
            self.assertEqual("approved", first["nodes"][0]["status"])
            self.assertTrue(first["nodes"][0]["content_sha256"].startswith("sha256:"))
            self.assertEqual("DERIVED_FROM", first["edges"][0]["type"])

    def test_missing_provenance_and_duplicate_id_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "knowledge"
            root.mkdir()
            no_sources = page("doc://knowledge/duplicate", sources="")
            (root / "one.md").write_text(no_sources, encoding="utf-8")
            (root / "two.md").write_text(page("doc://knowledge/duplicate"), encoding="utf-8")
            _graph, failures = GRAPH.build(root, "2026-07-31T00:00:00Z")
            self.assertTrue(any("sources" in item for item in failures), failures)
            self.assertTrue(any("unique" in item for item in failures), failures)

    def test_broken_internal_relation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "knowledge"
            root.mkdir()
            (root / "fact.md").write_text(page("doc://knowledge/fact", related="[doc://knowledge/missing]"), encoding="utf-8")
            _graph, failures = GRAPH.build(root, "2026-07-31T00:00:00Z")
            self.assertTrue(any("unresolved related" in item for item in failures), failures)

    def test_unapproved_status_remains_visible_not_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "knowledge"
            root.mkdir()
            (root / "candidate.md").write_text(page("doc://knowledge/candidate", status="candidate"), encoding="utf-8")
            graph, failures = GRAPH.build(root, "2026-07-31T00:00:00Z")
            self.assertEqual([], failures)
            self.assertEqual("candidate", graph["nodes"][0]["status"])


if __name__ == "__main__":
    unittest.main()
