# Rule Engine

The implementation authority is the `evaluate_rules` function in
`Sample-Projects/commerce-risk/risk_pipeline.py`; configuration is seeded in
`Sample-Projects/commerce-risk/sql/seed.sql`.

## Declined payments

**Fact:** `RISK_DECLINED_PAYMENTS` considers declined payment attempts after the
exclusive lower boundary `monitoring_time - window_hours` and at or before the
monitoring time. It groups by customer and alerts when the count reaches the
regional `event_count_threshold`. The alert stores the count and summed
attempted amount.

## High-value completed orders

**Fact:** `RISK_HIGH_VALUE_ORDER` reads the completed-order view, compares each
order with its regional `amount_threshold`, and excludes activity after the
monitoring time. Qualifying rows are grouped by customer and rule; the alert
stores the number and sum of all qualifying orders.

**Inference:** Although the baseline description speaks of a single high-value
order, multiple qualifying completed orders for one customer are represented by
one aggregated alert on a run date.

## Enablement and regional configuration

Both evaluators require `risk_rules.enabled = 1` and an exact region match in
`regional_rule_config`. Missing regional configuration therefore yields no
alert for that rule and region
(`Sample-Projects/commerce-risk/risk_pipeline.py`).

## Duplicate suppression and reruns

Both inserts use `INSERT OR IGNORE`. The partial unique index in
`Sample-Projects/commerce-risk/sql/schema.sql` suppresses another open alert for
the same customer, rule, and monitoring date. Direct calls to `evaluate_rules`
are rerun-safe for open alerts. The CLI-level `run_pipeline` first rebuilds the
database, so separate CLI runs do not preserve earlier alerts.

## Assumptions

- `monitoring_date` is derived from the first ten characters of the monitoring
  timestamp; the caller supplies a correctly formatted value.
- Amount aggregation uses SQLite numeric behavior and no currency conversion.

## Unresolved questions

- Expected behavior after an alert is closed and the same condition is detected
  again on the same monitoring date is not documented beyond the schema, which
  permits a new open alert.
- The code does not define behavior for malformed timestamps or incomplete
  configuration rows.

## Conflicts

No conflict was found between the SQL schema and Python evaluator. The stored
procedure wording in workspace guidance differs from the SQLite/Python
implementation; project code remains authoritative.
