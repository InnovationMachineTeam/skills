#!/usr/bin/env python3
"""Build a complete metaskillpack candidate from read-only source donors."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from donor_utils import frontmatter_identity, included_files, load_lock, resolve_donor


def copy_tree(source: Path, destination: Path, excluded_top_level: set[str] | None = None) -> None:
    excluded_top_level = excluded_top_level or set()
    destination.mkdir(parents=True, exist_ok=False)
    for path in included_files(source):
        relative = path.relative_to(source)
        if relative.parts and relative.parts[0] in excluded_top_level:
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skillpack", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--donor-root", action="append", type=Path, default=[])
    args = parser.parse_args()

    skillpack = args.skillpack.resolve()
    output = args.output.resolve()
    roots = [path.resolve() for path in args.donor_root]
    if output.exists():
        print(f"ERROR output already exists: {output}", file=sys.stderr)
        return 1
    if output == skillpack or skillpack in output.parents:
        print("ERROR output must be outside the active skillpack", file=sys.stderr)
        return 1

    try:
        lock = load_lock(skillpack)
        resolved = [resolve_donor(skillpack, donor, roots) for donor in lock["donors"]]
        blockers = [item for item in resolved if item["status"] in {"missing", "invalid"}]
        if blockers:
            for item in blockers:
                print(f"ERROR {item['name']}: {item.get('error')}", file=sys.stderr)
            return 3

        copy_tree(skillpack, output, {"vendor"})
        vendor_root = output / "vendor"
        vendor_root.mkdir()
        updated_donors = []
        by_name = {item["name"]: item for item in resolved}
        for donor in lock["donors"]:
            item = by_name[donor["name"]]
            source = Path(item["path"])
            donor_destination = vendor_root / donor["name"]
            copy_tree(source, donor_destination)
            source_contract = donor_destination / "SKILL.md"
            donor_contract = donor_destination / "DONOR.md"
            if not source_contract.is_file():
                raise ValueError(f"copied donor contract is missing: {source_contract}")
            source_contract.rename(donor_contract)
            readme = donor_destination / "README.md"
            if readme.is_file():
                readme.write_text(
                    readme.read_text(encoding="utf-8").replace("](SKILL.md)", "](DONOR.md)"),
                    encoding="utf-8",
                )
            nested_contracts = sorted(donor_destination.rglob("SKILL.md"))
            for nested_contract in nested_contracts:
                relative_source = nested_contract.relative_to(donor_destination).as_posix()
                relative_target = nested_contract.with_name("DONOR.md").relative_to(donor_destination).as_posix()
                for markdown in donor_destination.rglob("*.md"):
                    text = markdown.read_text(encoding="utf-8")
                    updated_text = text.replace(relative_source, relative_target)
                    if markdown.name == "README.md":
                        updated_text = updated_text.replace("](SKILL.md)", "](DONOR.md)")
                    if updated_text != text:
                        markdown.write_text(updated_text, encoding="utf-8")
                nested_contract.rename(nested_contract.with_name("DONOR.md"))
            updated = dict(donor)
            updated["version"] = item["actual_version"]
            updated["tree_sha256"] = item["actual_tree_sha256"]
            updated_donors.append(updated)

        _, pack_version = frontmatter_identity(output / "SKILL.md")
        updated_lock = dict(lock)
        updated_lock["pack_version"] = pack_version
        updated_lock["donors"] = updated_donors
        (output / "donors.json").write_text(
            json.dumps(updated_lock, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, UnicodeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1

    print(f"Built candidate with {len(updated_donors)} read-only donor snapshots at {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
