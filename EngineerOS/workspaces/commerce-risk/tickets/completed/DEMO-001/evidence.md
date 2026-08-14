# Evidence

## Human decisions

| Stage | Decision | Human | Date | Conditions | Reference |
|---|---|---|---|---|---|
| Stage 1 | Confirmed task understanding; orders currently marked `CANCELLED` at monitoring time are excluded even if previously completed | Repository owner | 2026-08-13 | Decision applies to DEMO-001 design and validation | User confirmation recorded in conversation; `task-understanding.md` |
| Stage 2 | Approved `design.md` and its documented assumptions; proceed to ticket-local proposed development | Repository owner | 2026-08-14 | Authoritative project remains unchanged; implementation stays ticket-local | User instruction to move to Prompt 6; `design.md` |

## Generated validation

| Artifact | Purpose | Execution status |
|---|---|---|
| None | Stage 1 does not generate implementation validation | Not Run |
| `tests/test_repeat_high_value_orders.py` | Automated DEMO-001 positive, negative, boundary, rerun, regional, cancellation, and regression validation | Not Run |
| `tests/validation-matrix.md` | Map every acceptance criterion to generated tests and expected results | Not Run |
| `tests/README.md` | Human execution and evidence-capture instructions | Not Run |

Use `Not Run` until execution is actually recorded.

## Executed evidence

| Action | Context | Executor | Date/time | Result | Reference |
|---|---|---|---|---|---|
| `python EngineerOS/scripts/validate_repository.py` | Repository root after Stage 1 artifact generation | Coding agent | 2026-08-13 | Passed: `Repository validation passed.` | `EngineerOS/scripts/validate_repository.py` |
| Python AST parse | Ticket-local proposed `risk_pipeline.py` | Coding agent | 2026-08-14 | Passed | `implementation/proposed/risk_pipeline.py` |
| SQL static completeness inspection | Ticket-local proposed `seed.sql`; corrected expected insert-block count from four to five | Coding agent | 2026-08-14 | Passed after correcting the check assertion; no SQL was executed | `implementation/proposed/sql/seed.sql` |
| Manifest and proposed-path consistency check | Three approved proposed files and manifest entries | Coding agent | 2026-08-14 | Passed: three existing proposed paths; all review statuses pending and transfer statuses not transferred | `implementation/change-manifest.yaml` |
| `python EngineerOS/scripts/validate_repository.py` | Repository root after Stage 3 proposed development | Coding agent | 2026-08-14 | Passed: `Repository validation passed.` | `EngineerOS/scripts/validate_repository.py` |
| Authoritative-source isolation check | `git diff --name-only -- Sample-Projects` during Stage 3 | Coding agent | 2026-08-14 | Passed: no authoritative sample-project paths reported | `Sample-Projects/commerce-risk/` |
| Python AST and test-method inventory | Ticket-local Stage 4 test module | Coding agent | 2026-08-14 | Passed: valid Python syntax and nine discovered `test_*` methods; tests not executed | `tests/test_repeat_high_value_orders.py` |
| Ticket validation-document link check | Two Markdown files under `tests/` | Coding agent | 2026-08-14 | Passed: no broken local Markdown links; tests not executed | `tests/README.md`, `tests/validation-matrix.md` |
| `python EngineerOS/scripts/validate_repository.py` | Repository root after Stage 4 generation | Coding agent | 2026-08-14 | Passed: `Repository validation passed.`; feature tests not executed | `EngineerOS/scripts/validate_repository.py` |
| Authoritative-source isolation check | `git diff --name-only -- Sample-Projects` during Stage 4 | Coding agent | 2026-08-14 | Passed: no authoritative sample-project paths reported | `Sample-Projects/commerce-risk/` |
| Accepted-finding static verification | Updated ticket-local feature test and design summary | Coding agent | 2026-08-14 | Passed: Python AST parsed with eleven `test_*` methods, including different-date and isolated CLI/build cases; tests not executed | `tests/test_repeat_high_value_orders.py`, `design.md` |
| Second independent review | Requirement, design, proposal, manifest, tests, and evidence after accepted fixes | Independent coding-agent review | 2026-08-14 | `ready_for_manual_transfer_guidance`; both first-pass findings resolved; tests not executed | `review.md` |
| Release/manifest path cross-check | Stage 6 guidance against three manifest entries | Coding agent | 2026-08-14 | Passed: all proposed and destination paths exist and appear in guidance; review statuses ready; transfer statuses not transferred | `release-and-rollback.md`, `implementation/change-manifest.yaml` |
| `python EngineerOS/scripts/validate_repository.py` | Repository root after Stage 6 guidance | Coding agent | 2026-08-14 | Passed: `Repository validation passed.`; no transfer or feature-test execution performed | `EngineerOS/scripts/validate_repository.py` |
| Authoritative-source isolation check | `git diff --name-only -- Sample-Projects` after Stage 6 guidance | Coding agent | 2026-08-14 | Passed: no authoritative sample-project paths reported | `Sample-Projects/commerce-risk/` |

## Outstanding evidence

- Human execution and confirmation of validation generated in a later stage.
- Human decision whether reviewed proposed files are transferred.
