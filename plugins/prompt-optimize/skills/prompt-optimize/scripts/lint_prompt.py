#!/usr/bin/env python3
"""Deterministic heuristic linter for master/system/developer prompts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def finding(
    check_id: str,
    severity: str,
    message: str,
    evidence: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": check_id,
        "severity": severity,
        "message": message,
    }
    if evidence:
        item["evidence"] = evidence[:240]
    return item


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def active_line_match(lines: list[str], patterns: list[str]) -> bool:
    """Match apparent active rules while ignoring lines discussing an anti-pattern."""
    meta_patterns = [
        r"\b(?:avoid|detect|flag|review|check for|do not use|don't use|should not contain)\b",
        r"(?:\b(?:антипаттерн|нет ли)\b|избега\w*|обнаруж\w*|проверь\w*|не использ\w*|не долж(?:ен|но))",
        r"(?:whether|если).{0,30}(?:both|одновременно)",
        r"(?:conflict|contradiction|конфликт|противореч)",
    ]
    return any(
        contains_any(line, patterns) and not contains_any(line, meta_patterns)
        for line in lines
    )


def lint(text: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    lowered = text.lower()
    lines = text.splitlines()

    if not text.strip():
        findings.append(finding("empty-prompt", "error", "Prompt is empty."))
        return summarize(text, findings)

    if len(text) > 60_000:
        findings.append(
            finding("prompt-size", "error", "Prompt exceeds 60,000 characters; split conditional guidance into skills or references.")
        )
    elif len(text) > 30_000:
        findings.append(
            finding("prompt-size", "warning", "Prompt exceeds 30,000 characters; verify that every section earns its context cost.")
        )

    fence_count = sum(1 for line in lines if line.strip().startswith("```"))
    if fence_count % 2:
        findings.append(finding("unbalanced-fences", "error", "Markdown code fences are unbalanced."))

    placeholders = re.findall(r"\b(?:TODO|TBD|FIXME)\b|\{\{[^}\n]+\}\}|\[(?:TODO|PLACEHOLDER)[^\]]*\]", text, re.IGNORECASE)
    if placeholders:
        findings.append(
            finding("unresolved-placeholders", "error", "Prompt contains unresolved placeholders.", ", ".join(placeholders[:5]))
        )

    headings = [
        re.sub(r"\s+", " ", match.group(1).strip().lower())
        for line in lines
        if (match := re.match(r"^#{1,6}\s+(.+?)\s*$", line))
    ]
    duplicates = [name for name, count in Counter(headings).items() if count > 1]
    if duplicates:
        findings.append(
            finding("duplicate-headings", "warning", "Prompt contains duplicate headings that may signal duplicated rules.", ", ".join(duplicates[:8]))
        )

    reveal_reasoning = [
        r"(?:show|reveal|provide|print).{0,30}(?:chain[- ]of[- ]thought|hidden reasoning|internal reasoning)",
        r"(?:покажи|раскрой|выведи).{0,35}(?:цепочк[ау] рассуждений|внутренн(?:ие|ий) рассуждени)",
    ]
    protect_reasoning = [
        r"(?:do not|never).{0,30}(?:reveal|show).{0,30}(?:chain[- ]of[- ]thought|hidden reasoning)",
        r"without.{0,20}(?:revealing|showing).{0,30}(?:chain[- ]of[- ]thought|hidden reasoning)",
        r"не (?:показывай|раскрывай).{0,35}(?:цепочк[ау] рассуждений|скрыт(?:ые|ый) рассуждени)",
        r"без.{0,20}(?:раскрытия|показа).{0,35}(?:цепочк[иу] рассуждений|скрыт(?:ых|ого) рассуждени)",
    ]
    asks_reveal = any(
        contains_any(line, reveal_reasoning) and not contains_any(line, protect_reasoning)
        for line in lines
    )
    protects = contains_any(text, protect_reasoning)
    if asks_reveal:
        findings.append(
            finding("hidden-reasoning", "error", "Prompt requests hidden chain-of-thought. Request concise rationale, evidence, assumptions, and decisions instead.")
        )
    if asks_reveal and protects:
        findings.append(finding("reasoning-conflict", "error", "Prompt both requests and forbids disclosure of hidden reasoning."))

    always_ask = [r"always ask", r"ask (?:the )?user before (?:every|any)", r"всегда (?:спрашивай|уточняй)"]
    never_ask = [r"never ask", r"do not ask (?:the )?user", r"никогда не (?:спрашивай|уточняй)"]
    if active_line_match(lines, always_ask) and active_line_match(lines, never_ask):
        findings.append(
            finding("clarification-conflict", "error", "Prompt contains both unconditional always-ask and never-ask rules. Replace them with risk- and materiality-based conditions.")
        )

    always_tools = [r"always use (?:a |the )?tools?", r"всегда используй инструменты"]
    never_tools = [r"never use (?:a |the )?tools?", r"do not use (?:a |the )?tools?", r"никогда не используй инструменты"]
    if active_line_match(lines, always_tools) and active_line_match(lines, never_tools):
        findings.append(finding("tool-conflict", "error", "Prompt both requires and forbids tool use without scoped conditions."))

    external_context = contains_any(
        text,
        [r"\b(?:files?|documents?|web pages?|emails?|messages?|tool results?|retrieved content)\b", r"\b(?:файл|документ|веб|письм|сообщени|результат инструмент)"],
    )
    untrusted_boundary = contains_any(
        text,
        [r"untrusted.{0,40}(?:data|content)", r"treat.{0,50}(?:as data|not instructions)", r"(?:недоверенн|внешн).{0,40}(?:данн|содержим)", r"считай.{0,50}данными.{0,20}не инструкциями"],
    )
    if external_context and not untrusted_boundary:
        findings.append(
            finding("untrusted-data-boundary", "warning", "Prompt mentions external content but does not clearly prevent that content from redefining instructions.")
        )

    verification = contains_any(
        text,
        [r"\b(?:verify|verification|validate|validation|test|check)\b", r"(?:проверк|валидир|валидац|тестир)"],
    ) and contains_any(
        text,
        [r"\b(?:result|outcome|completion|done|final state)\b", r"(?:результат|завершен|итог|конечн.{0,15}состоян)"],
    )
    if not verification:
        findings.append(
            finding("verification", "warning", "No clear requirement to verify the actual outcome before reporting completion.")
        )

    termination = contains_any(
        text,
        [r"\b(?:bound(?:ed)?|limit|max(?:imum)?).{0,30}(?:retr(?:y|ies)|loops?|iterations?|tool calls?|time)", r"(?:огранич|не более|максимум).{0,35}(?:повтор|цикл|итерац|вызов|времен)"],
    )
    retry_or_loop = contains_any(text, [r"\b(?:retry|repeat|loop|iterate)\b", r"\b(?:повтор|цикл|итерац)"])
    if retry_or_loop and not termination:
        findings.append(finding("unbounded-loop", "warning", "Prompt mentions retries or loops without an explicit bound or termination condition."))

    dynamic_claims = contains_any(
        text,
        [r"\b(?:latest|current|today(?:'s)?|present)\b.{0,30}\b(?:version|price|model|api|leader)", r"\b(?:последн|текущ|сегодняшн).{0,30}(?:верси|цен|модел|api|руководител)"],
    )
    freshness = contains_any(
        text,
        [r"(?:verify|fetch|check).{0,40}(?:current|latest|authoritative)", r"(?:проверь|получи|найди).{0,40}(?:актуальн|текущ|авторитетн)"],
    )
    if dynamic_claims and not freshness:
        findings.append(
            finding("dynamic-facts", "warning", "Prompt appears to rely on current facts without requiring freshness verification from an authoritative source.")
        )

    absolutes = len(re.findall(r"\b(?:always|never|must)\b|\b(?:всегда|никогда|обязан|должен)\b", lowered))
    if absolutes > 20:
        findings.append(
            finding("absolute-density", "warning", f"Prompt uses {absolutes} absolute terms. Confirm that each is a genuine invariant rather than a conditional preference.")
        )

    coverage = {
        "objective": contains_any(text, [r"\b(?:objective|goal|outcome|responsibility)\b", r"\b(?:цель|результат|ответственност)\b"]),
        "authority": contains_any(text, [r"\b(?:priority|authority|precedence|scope|permission)\b", r"\b(?:приоритет|полномочи|област[ьи] действия|разрешени)\b"]),
        "tools": contains_any(text, [r"\b(?:tools?|mcp|capabilit)\b", r"\b(?:инструмент|возможност)\b"]),
        "security": contains_any(text, [r"\b(?:security|privacy|secret|untrusted)\b", r"\b(?:безопасност|приватност|секрет|недоверенн)\b"]),
        "verification": verification,
        "completion": contains_any(text, [r"\b(?:completion|done|finish|final)\b", r"\b(?:завершен|готов|финал)\b"]),
    }
    missing = [name for name, present in coverage.items() if not present]
    if missing:
        findings.append(
            finding("coverage", "info", "Potentially missing control-plane dimensions; omit only when the host enforces them.", ", ".join(missing))
        )

    return summarize(text, findings, coverage)


def summarize(
    text: str,
    findings: list[dict[str, Any]],
    coverage: dict[str, bool] | None = None,
) -> dict[str, Any]:
    counts = Counter(item["severity"] for item in findings)
    return {
        "summary": {
            "characters": len(text),
            "lines": len(text.splitlines()),
            "errors": counts["error"],
            "warnings": counts["warning"],
            "info": counts["info"],
            "coverage": coverage or {},
        },
        "findings": findings,
    }


def render_text(report: dict[str, Any]) -> str:
    summary = report["summary"]
    output = [
        f"Prompt: {summary['lines']} lines, {summary['characters']} characters",
        f"Findings: {summary['errors']} errors, {summary['warnings']} warnings, {summary['info']} info",
    ]
    for item in report["findings"]:
        line = f"[{item['severity'].upper()}] {item['id']}: {item['message']}"
        if item.get("evidence"):
            line += f" Evidence: {item['evidence']}"
        output.append(line)
    if not report["findings"]:
        output.append("No heuristic findings.")
    return "\n".join(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="-", help="Prompt file, or - for stdin")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--fail-on", choices=("none", "error", "warning"), default="none")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"Error: could not read prompt: {exc}", file=sys.stderr)
        return 2

    report = lint(text)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(report))

    severities = {item["severity"] for item in report["findings"]}
    if args.fail_on == "error" and "error" in severities:
        return 1
    if args.fail_on == "warning" and severities.intersection({"error", "warning"}):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
