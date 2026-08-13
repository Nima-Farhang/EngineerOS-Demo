#!/usr/bin/env python3
"""Basic structural and confidentiality validation for the public demo repo."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "README.md",
    "EngineerOs/AGENTS.md",
    "EngineerOs/platform.yaml",
    "EngineerOs/platform/operating-rules.md",
    "EngineerOs/WORKFLOW.md",
    "EngineerOs/workspaces/commerce-risk/instructions.md",
    "Projects-Codes/commerce-risk/README.md",
]

# Generic patterns only: do not embed organization-specific names in this
# public demonstration repository.
PROHIBITED_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.I),
    re.compile(r"(?:password|passwd|api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]+['\"]", re.I),
    re.compile(r"https?://(?:localhost|127\.0\.0\.1)(?::\d+)?/[^\s)]*", re.I),
]
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".sql", ".py", ".json", ".txt"}


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).exists():
            errors.append(f"Missing required file: {relative}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Non-UTF-8 text file: {path.relative_to(ROOT)}")
            continue
        for pattern in PROHIBITED_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"Prohibited pattern {pattern.pattern!r} in {path.relative_to(ROOT)}"
                )

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
