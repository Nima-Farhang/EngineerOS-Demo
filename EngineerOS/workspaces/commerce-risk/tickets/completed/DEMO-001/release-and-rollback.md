# Manual Transfer, Execution, and Rollback

## Status

- Guidance status: Complete
- Review prerequisite: Met — `review.md` is
  `ready_for_manual_transfer_guidance`
- Transfer status: `not_transferred` for all manifest entries
- Generated test status: `Not Run`
- Release/deployment status: Not performed

This document provides human actions only. It does not authorize an agent to
transfer files, execute tests, commit, push, deploy, or release.

## Preconditions

Before manual transfer, a human must confirm all of the following:

1. `review.md` still says `ready_for_manual_transfer_guidance`.
2. The approved design and proposed files have not changed since that review.
3. `implementation/change-manifest.yaml` contains exactly the three mappings
   listed below and every transfer status is `not_transferred`.
4. The destination worktree is understood and unrelated changes will not be
   overwritten.
5. A recoverable copy of each current destination file is created in a
   human-selected backup directory outside `Sample-Projects/commerce-risk/`.
6. The human explicitly approves transfer and accepts the approved assumptions:
   current cancelled orders are excluded, `ordered_at` is used, the rolling
   lower bound is exclusive, and the upper bound is inclusive.
7. Python 3 and its standard-library SQLite module are available.

## Proposed-to-destination mapping

This ordered mapping exactly matches `implementation/change-manifest.yaml`.

| Order | Proposed path | Intended destination | Human owner |
|---|---|---|---|
| 1 | `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/sql/seed.sql` | `Sample-Projects/commerce-risk/sql/seed.sql` | Human transfer owner |
| 2 | `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/risk_pipeline.py` | `Sample-Projects/commerce-risk/risk_pipeline.py` | Human transfer owner |
| 3 | `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/README.md` | `Sample-Projects/commerce-risk/README.md` | Human transfer owner |

The ticket-local generated test is not a project transfer entry. It should be
copied only into an isolated temporary validation tree as described below.

## Pre-transfer integrity checks

Run from the repository root and save the output:

```bash
python EngineerOS/scripts/validate_repository.py
git status --short
sha256sum \
  EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/sql/seed.sql \
  EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/risk_pipeline.py \
  EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/README.md
diff -u Sample-Projects/commerce-risk/sql/seed.sql \
  EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/sql/seed.sql
diff -u Sample-Projects/commerce-risk/risk_pipeline.py \
  EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/risk_pipeline.py
diff -u Sample-Projects/commerce-risk/README.md \
  EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/README.md
```

`diff` is expected to return exit status 1 when the reviewed differences are
present. Any unexpected difference, missing path, validation failure, or
unrelated destination edit stops transfer.

Record current destination hashes separately:

```bash
sha256sum \
  Sample-Projects/commerce-risk/sql/seed.sql \
  Sample-Projects/commerce-risk/risk_pipeline.py \
  Sample-Projects/commerce-risk/README.md
```

## Backup

Choose and record an explicit backup directory. Do not place it inside the
authoritative project. For example, after replacing the placeholder with an
approved existing path:

```bash
mkdir -p <approved-backup-directory>/sql
cp Sample-Projects/commerce-risk/sql/seed.sql \
  <approved-backup-directory>/sql/seed.sql
cp Sample-Projects/commerce-risk/risk_pipeline.py \
  <approved-backup-directory>/risk_pipeline.py
cp Sample-Projects/commerce-risk/README.md \
  <approved-backup-directory>/README.md
```

Verify the backup files exist and record their hashes before continuing.

## Manual transfer steps

Only after explicit human transfer approval, run from the repository root:

```bash
cp EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/sql/seed.sql \
  Sample-Projects/commerce-risk/sql/seed.sql
cp EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/risk_pipeline.py \
  Sample-Projects/commerce-risk/risk_pipeline.py
cp EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/README.md \
  Sample-Projects/commerce-risk/README.md
```

Confirm byte-for-byte transfer:

```bash
cmp EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/sql/seed.sql \
  Sample-Projects/commerce-risk/sql/seed.sql
cmp EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/risk_pipeline.py \
  Sample-Projects/commerce-risk/risk_pipeline.py
cmp EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/README.md \
  Sample-Projects/commerce-risk/README.md
```

All three `cmp` commands should exit 0 with no output. Only after saving human
evidence should the manifest and changed-files transfer statuses be updated.

## Validation steps

Use an isolated temporary tree so the generated feature test is not silently
added to authoritative project source:

```bash
validation_dir=$(mktemp -d)
cp -R Sample-Projects/commerce-risk/. "$validation_dir/"
cp EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/tests/test_repeat_high_value_orders.py \
  "$validation_dir/tests/test_repeat_high_value_orders.py"
cd "$validation_dir"
python --version
python -c "import sqlite3; print(sqlite3.sqlite_version)"
python run_pipeline.py --database "$validation_dir/validation.db" \
  --monitoring-time 2026-01-15T12:00:00Z
python -m unittest discover -s tests -v
```

The human should retain the temporary directory until results are reviewed. It
may be removed later only by a deliberate human cleanup decision.

| Order | Human action | Expected result | Evidence to capture |
|---|---|---|---|
| 1 | Run repository validation from the repository root | `Repository validation passed.` | Command, output, exit code, executor, date/time |
| 2 | Run pipeline in the isolated tree | Exit 0; database created; baseline seed reports 2 alerts created and 2 total | Full output, database path, Python/SQLite versions |
| 3 | Run unittest discovery in the isolated tree | Existing four tests and eleven DEMO-001 tests run successfully; total 15 | Complete test names/output, exit code, executor, date/time |
| 4 | Inspect transfer diff in the real worktree | Only the three approved destination files have intended content changes | `git diff -- Sample-Projects/commerce-risk` captured for human review |
| 5 | Record results in `evidence.md` | Executed evidence is separate from generated expectations | Human-authored evidence entry and references |

Do not describe an expected result as passed until a human records the actual
execution evidence.

## Post-change monitoring

For this local demo, monitoring is a human inspection immediately after
transfer and validation:

- Confirm `RISK_REPEAT_HIGH_VALUE_ORDERS` exists once and has four regional
  configuration rows with non-null window, count, and amount values.
- Confirm the baseline pipeline still produces the two existing seed alerts;
  the seed intentionally does not create a repeat-order alert.
- Review the isolated feature-test output for count/total, boundaries,
  cancellation, regions, same-date suppression, and different-date behavior.
- Confirm no database, cache, test, or backup artifact appeared under
  `Sample-Projects/commerce-risk/` unexpectedly.
- Re-run repository validation after transfer.

Any unexpected alert count, duplicate, missing configuration, test failure,
unapproved file change, or repository validation failure triggers rollback.

## Rollback triggers

- Any `cmp` mismatch immediately after transfer.
- Pipeline or test command exits nonzero.
- Baseline existing-rule results change unexpectedly.
- The repeat rule includes a pending/currently cancelled order or violates a
  configured boundary.
- Duplicate open alerts appear for the same customer/rule/monitoring date.
- A manifest/destination mismatch or unapproved file modification is found.
- Repository validation fails.
- The human owner withdraws transfer approval before acceptance.

## Rollback steps

Use the exact recorded backup directory; replace the placeholder before running
commands.

| Order | Human action | Verification |
|---|---|---|
| 1 | Stop further validation, source-control, or release activity | No later-stage action continues |
| 2 | Restore backup `sql/seed.sql` to `Sample-Projects/commerce-risk/sql/seed.sql` | `cmp` restored file against backup exits 0 |
| 3 | Restore backup `risk_pipeline.py` to `Sample-Projects/commerce-risk/risk_pipeline.py` | `cmp` restored file against backup exits 0 |
| 4 | Restore backup `README.md` to `Sample-Projects/commerce-risk/README.md` | `cmp` restored file against backup exits 0 |
| 5 | Rebuild a database at an isolated temporary path and run existing baseline tests | Human records actual results; do not infer success |
| 6 | Run repository validation | Human records actual result |
| 7 | Record rollback reason, executor, time, restored hashes, and validation evidence in `evidence.md` | Evidence is complete and transfer statuses reflect the human decision |

Example restore commands:

```bash
cp <approved-backup-directory>/sql/seed.sql \
  Sample-Projects/commerce-risk/sql/seed.sql
cp <approved-backup-directory>/risk_pipeline.py \
  Sample-Projects/commerce-risk/risk_pipeline.py
cp <approved-backup-directory>/README.md \
  Sample-Projects/commerce-risk/README.md
```

Do not use destructive Git reset or checkout commands for rollback.

## Source-control and release controls

Transfer, test execution, source control, and release are separate human
decisions:

1. Manual transfer requires explicit human approval and evidence.
2. Test execution and result confirmation require a human executor.
3. A commit requires a separate review of the final diff and explicit approval.
4. Push, pull-request, publication, deployment, or release actions require
   separate explicit approval and are not performed by this guidance.
5. This SQLite sample has no deployment target; “release” means a human-approved
   repository change only.

Until evidence exists, retain every manifest transfer status as
`not_transferred`.
