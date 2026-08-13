# Testing Guide

Baseline tests are defined in
`Sample-Projects/commerce-risk/tests/test_pipeline.py` using `unittest` and a
temporary SQLite database per test.

## Human execution

From the repository root:

```bash
cd Sample-Projects/commerce-risk
python -m unittest discover -s tests -v
```

Record the command, environment, executor, time, exit status, and complete
result before describing a test as passed. Merely generating or inspecting a
test is not executed evidence
(`EngineerOS/platform/operating-rules.md`).

## Current generated coverage

| Test | Intended check |
|---|---|
| `test_seed_data_creates_expected_alerts` | Baseline seed produces the expected customer/rule pairs |
| `test_rerun_does_not_duplicate_open_alerts` | Same-date evaluation creates no duplicate open alerts |
| `test_regional_threshold_is_configurable` | Changing EAST configuration makes its completed order eligible |
| `test_cancelled_high_value_order_is_not_eligible` | Completed-order view excludes a cancelled high-value order |

## Static checks

Repository structure and public-safety patterns can be checked from the root:

```bash
python EngineerOS/scripts/validate_repository.py
```

## Coverage gaps

**Fact:** Current tests do not directly cover disabled rules, exact time-window
boundaries, missing configuration, closed-alert behavior, malformed timestamps,
or monitoring-run failure status.

**Inference:** These gaps are reasonable for the compact baseline but should be
addressed when a feature changes the corresponding behavior.

**Unresolved question:** No target Python or SQLite version is declared.
