# DEMO-001 Human Validation Instructions

These tests target the proposed destination. On 2026-08-14 an authorized
isolated temporary runner reported all eleven passing; human result confirmation
is pending. They import `risk_pipeline` as it will exist after a human-approved
manual transfer.

## Preconditions

1. A human has approved transfer of the proposed implementation.
2. The three proposed files have been copied to their destinations exactly as
   mapped in `../implementation/change-manifest.yaml`.
3. This test file has been copied to
   `Sample-Projects/commerce-risk/tests/test_repeat_high_value_orders.py`, or an
   equivalent temporary validation tree has been assembled without changing
   authoritative source.
4. Python 3 with the standard-library `sqlite3` module is available.

## Human command after manual transfer

From the repository root:

```bash
cd Sample-Projects/commerce-risk
python -m unittest discover -s tests -v
```

## Isolated temporary alternative

The reproducible reviewer command is:

```bash
python EngineerOS/scripts/validate_ticket_proposal.py DEMO-001
```

It copies source and proposed files into a temporary directory, runs baseline
and DEMO-001 tests there, verifies authoritative source hashes, reports actual
results, and cleans up. It does not transfer the proposal.

The equivalent manual process is described below.

A human may instead create a temporary project tree containing:

- the current `sql/schema.sql`, `run_pipeline.py`, and existing tests;
- the proposed `README.md`, `risk_pipeline.py`, and `sql/seed.sql`; and
- `test_repeat_high_value_orders.py` copied into its `tests/` directory.

Run the same unittest discovery command inside that temporary tree. Record it
as isolated temporary validation, not transfer, deployment, or shared
environment evidence.

## Expected results

- All existing baseline tests pass.
- All eleven DEMO-001 tests pass.
- No test writes into authoritative project source; each generated feature test
  uses a temporary database.

Capture the full command, Python version, SQLite version, working directory,
executor, date/time, exit code, and complete test output in `../evidence.md`.
