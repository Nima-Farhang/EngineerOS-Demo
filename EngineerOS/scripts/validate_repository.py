#!/usr/bin/env python3
"""Validate repository structure, ticket integrity, links, and public safety."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TICKETS = ROOT / "EngineerOS/workspaces/commerce-risk/tickets"
REQUIRED_REPOSITORY_PATHS = [
    "README.md", "EngineerOS/AGENTS.md", "EngineerOS/platform.yaml",
    "EngineerOS/platform/operating-rules.md", "EngineerOS/WORKFLOW.md",
    "EngineerOS/workspaces/commerce-risk/instructions.md",
    "EngineerOS/workspaces/commerce-risk/project-code/SOURCE-MANIFEST.yaml",
    "Sample-Projects/commerce-risk/README.md",
]
REQUIRED_COMPLETED_TICKET_PATHS = [
    "ticket.md", "task-understanding.md", "design.md", "evidence.md",
    "review.md", "release-and-rollback.md", "source",
    "implementation/change-manifest.yaml", "implementation/changed-files.md",
    "implementation/proposed", "tests/README.md", "tests/validation-matrix.md",
]
MANIFEST_FIELDS = {
    "source_path", "proposed_path", "change_type", "reason",
    "intended_destination", "review_status", "transfer_status",
}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".sql", ".py", ".json", ".txt"}
PROHIBITED_BINARY_SUFFIXES = {
    ".7z", ".doc", ".docm", ".docx", ".eml", ".gz", ".msg", ".pdf",
    ".ppt", ".pptm", ".pptx", ".rar", ".tar", ".xls", ".xlsm", ".xlsx",
    ".zip",
}
EMAIL_PATTERN = re.compile(r"(?<![\w.-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
PRIVATE_URL_PATTERNS = [
    re.compile(r"https?://(?:localhost|127\.0\.0\.1)(?::\d+)?(?:/|\b)", re.I),
    re.compile(r"https?://(?:10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)(?::\d+)?(?:/|\b)", re.I),
    re.compile(r"https?://[^\s/)]+\.(?:internal|intranet|local)(?:/|\b)", re.I),
]
CREDENTIAL_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.I),
    re.compile(r"(?:password|passwd|api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]+['\"]", re.I),
    re.compile(r"(?:postgres|mysql|mongodb(?:\+srv)?)://[^\s:@]+:[^\s@]+@", re.I),
]
WORKPLACE_PATTERNS = [
    re.compile(r"\binternal use only\b", re.I),
    re.compile(r"\bcompany confidential\b", re.I),
    re.compile(r"\bcustomer confidential\b", re.I),
    re.compile(r"\bproprietary and confidential\b", re.I),
]
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_manifest_entries(path: Path, errors: list[str]) -> list[dict[str, str]]:
    """Parse the deliberately simple list-of-mappings manifest shape."""
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^  - [a-z_]+:", raw_line):
            if current is not None:
                entries.append(current)
            current = {}
            key, value = raw_line[4:].split(":", 1)
            current[key.strip()] = value.strip().strip('"')
        elif current is not None and re.match(r"^    [a-z_]+:", raw_line):
            key, value = raw_line.strip().split(":", 1)
            current[key.strip()] = value.strip().strip('"')
    if current is not None:
        entries.append(current)
    if not entries:
        errors.append(f"Manifest has no change entries: {relative(path)}")
    return entries


def validate_manifest(ticket: Path, errors: list[str]) -> None:
    manifest = ticket / "implementation/change-manifest.yaml"
    if not manifest.is_file():
        return
    proposed_root = (ticket / "implementation/proposed").resolve()
    for index, entry in enumerate(parse_manifest_entries(manifest, errors), start=1):
        missing = sorted(MANIFEST_FIELDS - entry.keys())
        if missing:
            errors.append(
                f"Manifest entry {index} missing {', '.join(missing)}: {relative(manifest)}"
            )
            continue
        proposed = (ROOT / entry["proposed_path"]).resolve()
        source = (ROOT / entry["source_path"]).resolve()
        destination = (ROOT / entry["intended_destination"]).resolve()
        if not proposed.is_relative_to(proposed_root):
            errors.append(f"Proposed path escapes ticket-local tree: {entry['proposed_path']}")
        if not proposed.is_file():
            errors.append(f"Manifest proposed path does not exist: {entry['proposed_path']}")
        if not source.is_file():
            errors.append(f"Manifest source path does not exist: {entry['source_path']}")
        if entry["change_type"] == "modify" and source != destination:
            errors.append(f"Modify destination differs from source: {entry['intended_destination']}")
        if entry["change_type"] not in {"add", "modify", "delete"}:
            errors.append(f"Unsupported manifest change type: {entry['change_type']}")
        if entry["transfer_status"] not in {"not_transferred", "transferred", "rolled_back"}:
            errors.append(f"Unsupported transfer status: {entry['transfer_status']}")


def validate_completed_tickets(errors: list[str]) -> None:
    completed_root = TICKETS / "completed"
    if not completed_root.exists():
        return
    for ticket in sorted(path for path in completed_root.iterdir() if path.is_dir()):
        for required in REQUIRED_COMPLETED_TICKET_PATHS:
            if not (ticket / required).exists():
                errors.append(f"Missing completed-ticket artifact: {relative(ticket / required)}")
        validate_manifest(ticket, errors)
        evidence = ticket / "evidence.md"
        if evidence.is_file():
            text = evidence.read_text(encoding="utf-8")
            generated = text.partition("## Generated validation")[2].partition("## Executed evidence")[0]
            for line in generated.splitlines():
                if line.startswith("|") and "tests/" in line and "Not Run" not in line:
                    errors.append(
                        f"Generated test is not marked Not Run in {relative(evidence)}: {line.strip()}"
                    )


def validate_markdown_links(path: Path, text: str, errors: list[str]) -> None:
    for target in MARKDOWN_LINK_PATTERN.findall(text):
        clean_target = target.strip().strip("<>").split("#", 1)[0]
        if not clean_target or clean_target.startswith("/"):
            continue
        if not (path.parent / clean_target).resolve().exists():
            errors.append(f"Broken Markdown link in {relative(path)}: {target}")


def validate_public_safety(path: Path, text: str, errors: list[str]) -> None:
    if path.name != "validate_repository.py":
        for pattern in CREDENTIAL_PATTERNS:
            if pattern.search(text):
                errors.append(f"Possible credential in {relative(path)}")
    for match in EMAIL_PATTERN.finditer(text):
        errors.append(f"Email address in public text {relative(path)}: {match.group(0)}")
    for pattern in PRIVATE_URL_PATTERNS:
        if pattern.search(text):
            errors.append(f"Private/local URL in {relative(path)}")
    for pattern in WORKPLACE_PATTERNS:
        if pattern.search(text):
            errors.append(f"Workplace confidentiality phrase in {relative(path)}")


def main() -> int:
    errors: list[str] = []
    for item in REQUIRED_REPOSITORY_PATHS:
        if not (ROOT / item).exists():
            errors.append(f"Missing required path: {item}")
    validate_completed_tickets(errors)
    for path in ROOT.rglob("*"):
        if path.is_dir() and path.name == ".git" and path != ROOT / ".git":
            errors.append(f"Nested Git directory: {relative(path)}")
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in PROHIBITED_BINARY_SUFFIXES:
            errors.append(f"Prohibited binary/document type: {relative(path)}")
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".gitignore", "LICENSE"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Non-UTF-8 text file: {relative(path)}")
            continue
        validate_public_safety(path, text, errors)
        if path.suffix.lower() == ".md":
            validate_markdown_links(path, text, errors)
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
