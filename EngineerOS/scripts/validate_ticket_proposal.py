#!/usr/bin/env python3
"""Run ticket proposal tests in an isolated temporary project tree."""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IGNORED_HASH_PARTS = {"__pycache__", "build"}


def simple_yaml_value(path: Path, key: str) -> str:
    pattern = re.compile(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip('"')
    raise ValueError(f"Missing {key!r} in {path.relative_to(ROOT)}")


def manifest_entries(path: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^  - [a-z_]+:", line):
            if current is not None:
                entries.append(current)
            current = {}
            key, value = line[4:].split(":", 1)
            current[key.strip()] = value.strip().strip('"')
        elif current is not None and re.match(r"^    [a-z_]+:", line):
            key, value = line.strip().split(":", 1)
            current[key.strip()] = value.strip().strip('"')
    if current is not None:
        entries.append(current)
    if not entries:
        raise ValueError(f"No changes in {path.relative_to(ROOT)}")
    return entries


def find_ticket(ticket_id: str) -> Path:
    matches = sorted(
        path
        for path in (ROOT / "EngineerOS/workspaces").glob(
            f"*/tickets/*/{ticket_id}"
        )
        if path.is_dir()
    )
    if len(matches) != 1:
        raise ValueError(f"Expected one ticket named {ticket_id}; found {len(matches)}")
    return matches[0]


def hash_tree(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if any(part in IGNORED_HASH_PARTS for part in relative.parts) or path.suffix == ".pyc":
            continue
        hashes[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def run_tests(project: Path, pattern: str) -> tuple[bool, int | None]:
    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        pattern,
        "-v",
    ]
    result = subprocess.run(command, cwd=project, capture_output=True, text=True)
    print(f"\nCommand: {' '.join(command)}")
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    combined = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", combined)
    return result.returncode == 0, int(match.group(1)) if match else None


def format_result(passed: bool, count: int | None) -> str:
    count_text = f"{count} tests" if count is not None else "count unavailable"
    return f"{'PASS' if passed else 'FAIL'} ({count_text})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticket_id", help="Ticket directory name, for example DEMO-001")
    args = parser.parse_args()

    ticket = find_ticket(args.ticket_id)
    workspace = ticket.parents[2]
    source_manifest = workspace / "project-code/SOURCE-MANIFEST.yaml"
    authoritative = (ROOT / simple_yaml_value(source_manifest, "path")).resolve()
    manifest = ticket / "implementation/change-manifest.yaml"
    entries = manifest_entries(manifest)
    before = hash_tree(authoritative)
    transfer_states = sorted({entry.get("transfer_status", "missing") for entry in entries})

    assembled = False
    baseline_passed = False
    baseline_count: int | None = None
    feature_passed = False
    feature_count: int | None = None

    print("Validation type: isolated temporary validation")
    print("This is not manual transfer, deployment, shared-environment validation, or production evidence.")
    try:
        with tempfile.TemporaryDirectory(prefix=f"engineeros-{args.ticket_id.lower()}-") as temporary:
            project = Path(temporary) / authoritative.name
            shutil.copytree(authoritative, project)
            for entry in entries:
                proposed = (ROOT / entry["proposed_path"]).resolve()
                destination = (ROOT / entry["intended_destination"]).resolve()
                destination_relative = destination.relative_to(authoritative)
                temporary_destination = project / destination_relative
                change_type = entry.get("change_type")
                if change_type in {"add", "modify"}:
                    temporary_destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(proposed, temporary_destination)
                elif change_type == "delete":
                    temporary_destination.unlink(missing_ok=True)
                else:
                    raise ValueError(f"Unsupported change type: {change_type}")
            assembled = True
            baseline_passed, baseline_count = run_tests(project, "test_pipeline.py")
            generated_tests = sorted((ticket / "tests").glob("test_*.py"))
            if not generated_tests:
                raise ValueError("No generated ticket tests found")
            for test in generated_tests:
                shutil.copy2(test, project / "tests" / test.name)
            feature_results = [run_tests(project, test.name) for test in generated_tests]
            feature_passed = all(result[0] for result in feature_results)
            counts = [result[1] for result in feature_results]
            feature_count = sum(count for count in counts if count is not None)
            if any(count is None for count in counts):
                feature_count = None
    finally:
        after = hash_tree(authoritative)
        unchanged = before == after
        print("\nSummary")
        print(f"Ticket: {args.ticket_id}")
        print(f"Authoritative project modified: {'No' if unchanged else 'Yes'}")
        print(f"Temporary proposal assembled: {'Yes' if assembled else 'No'}")
        print(f"Baseline tests: {format_result(baseline_passed, baseline_count)}")
        print(f"DEMO-001 tests: {format_result(feature_passed, feature_count)}")
        print("Validation type: isolated temporary validation")
        print(f"Transfer state: {', '.join(transfer_states)}")
        print("Temporary files cleaned up: Yes")

    return 0 if unchanged and assembled and baseline_passed and feature_passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, ValueError) as error:
        print(f"Validation setup failed: {error}", file=sys.stderr)
        sys.exit(2)
