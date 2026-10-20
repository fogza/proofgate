#!/usr/bin/env python3
"""Check the structure of a PR's AC-to-evidence report, not its truth."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


HEADER = ["id", "criterion", "status", "evidence"]
PLACEHOLDERS = {"", "-", "n/a", "todo", "tbd", "<source>", "<evidence>"}


def cells(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def validate(body: str) -> list[str]:
    errors: list[str] = []
    section = re.search(
        r"(?ims)^##\s+Acceptance criteria\s*$([\s\S]*?)(?=^##\s+|\Z)", body
    )
    if not section:
        return ["Add a '## Acceptance criteria' section using the Proofgate PR template"]
    content = section.group(1)
    source = re.search(r"(?im)^Source:\s*(.+)$", content)
    if not source or source.group(1).strip().lower() in PLACEHOLDERS:
        errors.append("Name the originating request, issue, or spec in Source")

    lines = [line for line in content.splitlines() if line.lstrip().startswith("|")]
    if len(lines) < 3 or [value.lower() for value in cells(lines[0])] != HEADER:
        errors.append("Use table columns: ID | Criterion | Status | Evidence")
        return errors
    if not all(re.fullmatch(r":?-{3,}:?", value) for value in cells(lines[1])):
        errors.append("Add a Markdown table separator row")

    rows = lines[2:]
    if not rows:
        errors.append("Add at least one acceptance criterion")
    seen: set[str] = set()
    for number, line in enumerate(rows, start=1):
        row = cells(line)
        if len(row) != 4:
            errors.append(f"AC row {number}: expected four columns")
            continue
        identifier, criterion, status, evidence = row
        if not identifier or identifier in seen:
            errors.append(f"AC row {number}: ID is missing or repeated")
        seen.add(identifier)
        if criterion.lower() in PLACEHOLDERS or criterion.startswith("<"):
            errors.append(f"AC row {number}: describe the criterion")
        if status.lower() != "verified":
            errors.append(f"AC row {number}: status must be verified before merge")
        if evidence.lower() in PLACEHOLDERS or evidence.startswith("<"):
            errors.append(f"AC row {number}: provide concrete evidence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--body-file", type=Path)
    source.add_argument("--body-env")
    args = parser.parse_args()
    try:
        body = args.body_file.read_text(encoding="utf-8") if args.body_file else os.environ[args.body_env]
    except (OSError, KeyError) as error:
        parser.exit(2, f"proofgate: {error}\n")
    errors = validate(body)
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        return 1
    print("PASS: AC/evidence report is structurally complete; review and tests must verify its claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
