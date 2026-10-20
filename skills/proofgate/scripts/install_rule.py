#!/usr/bin/env python3
"""Install the self-contained Proofgate rule without touching other guidance."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = re.compile(r"<!-- proofgate:start v\d+ -->")
END = "<!-- proofgate:end -->"


def install(project: Path, language: str, check: bool = False) -> str:
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f"Project directory does not exist: {project}")

    target = project / "AGENTS.md"
    if target.is_symlink():
        raise ValueError("Review the AGENTS.md symlink target before editing it")

    template_path = Path(__file__).resolve().parents[1] / "assets" / f"rule.{language}.md"
    rule = template_path.read_text(encoding="utf-8").strip() + "\n"
    original = target.read_text(encoding="utf-8") if target.exists() else ""
    starts = list(START.finditer(original))
    ends = [m.start() for m in re.finditer(re.escape(END), original)]

    if len(starts) != len(ends) or len(starts) > 1:
        raise ValueError("Malformed or repeated Proofgate markers; review AGENTS.md manually")

    if starts:
        start = starts[0].start()
        end = ends[0] + len(END)
        if ends[0] < start:
            raise ValueError("Proofgate markers are out of order")
        updated = original[:start] + rule.rstrip("\n") + original[end:]
    elif re.search(r"\bproofgate\b", original, re.IGNORECASE):
        raise ValueError("Existing unmarked Proofgate guidance needs manual review")
    else:
        updated = original.rstrip("\n")
        if updated:
            updated += "\n\n"
        updated += rule

    if updated == original:
        return "unchanged"
    if check:
        return "missing-or-outdated"
    target.write_text(updated, encoding="utf-8")
    return "created" if not original else "updated"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--lang", choices=("en", "th"), default="en")
    parser.add_argument("--check", action="store_true", help="Report without writing")
    args = parser.parse_args()
    try:
        result = install(args.project, args.lang, args.check)
    except (OSError, ValueError) as error:
        parser.exit(2, f"proofgate: {error}\n")
    print(result)
    return 0 if result == "unchanged" or not args.check else 1


if __name__ == "__main__":
    raise SystemExit(main())
