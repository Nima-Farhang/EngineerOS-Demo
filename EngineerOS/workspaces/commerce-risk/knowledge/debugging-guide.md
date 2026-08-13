# Debugging Guide

## Reproduce from a clean database

From the repository root, use an explicit temporary destination so debugging
does not create artifacts in project source:

```bash
python Sample-Projects/commerce-risk/run_pipeline.py \
  --database /tmp/commerce-risk-debug.db \
  --monitoring-time 2026-01-15T12:00:00Z
```

The runner prints the destination, alerts created, and total alerts
(`Sample-Projects/commerce-risk/run_pipeline.py`). Be aware that the destination
is deleted and rebuilt by `build_database`
(`Sample-Projects/commerce-risk/risk_pipeline.py`).

## Inspect a result

If the `sqlite3` command is installed:

```bash
sqlite3 /tmp/commerce-risk-debug.db ".tables"
sqlite3 /tmp/commerce-risk-debug.db \
  "SELECT c.display_name, r.rule_code, a.qualifying_event_count, a.qualifying_amount FROM alerts a JOIN customers c USING (customer_id) JOIN risk_rules r USING (rule_id);"
```

## Symptom guide

| Symptom | Check |
|---|---|
| No alert appears | Rule enablement, exact region configuration, status filters, threshold, and monitoring time |
| Unexpected declined count | Exclusive lower and inclusive upper window boundaries in `evaluate_rules` |
| Duplicate insert is ignored | Existing open customer/rule/date row and the partial unique index |
| Cancelled or pending order is absent | `v_completed_order_activity` filters to `COMPLETED` |
| Previous data disappears | `run_pipeline` rebuilds the target database before evaluation |
| Foreign-key error | Referenced customer, order, or rule and `PRAGMA foreign_keys` |

Relevant sources are `Sample-Projects/commerce-risk/risk_pipeline.py` and
`Sample-Projects/commerce-risk/sql/schema.sql`.

## Evidence classification

**Fact:** CLI output confirms only the summary returned by the runner.
Inspecting generated SQL or expected rows is not executed evidence.

**Assumption:** The debugging host has a compatible Python 3 and SQLite build.

**Unresolved question:** The project has no structured logging or retained
failure record, so unexpected exceptions require console capture.
