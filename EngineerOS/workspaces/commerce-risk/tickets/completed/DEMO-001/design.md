# Design

## Objective

Add `RISK_REPEAT_HIGH_VALUE_ORDERS` as a separately enabled, regionally
configured batch rule. It will detect customers with enough individually
qualifying, currently completed orders in a rolling window, store their count
and total amount, preserve existing behavior, and reuse current open-alert
duplicate suppression.

This design is based on the confirmed requirement in
`source/feature-request.md` and the Stage 1 decision in `evidence.md`.

## Requirement traceability

| Requirement | Design response |
|---|---|
| Exact independently enabled rule code | Add one enabled `risk_rules` seed row for `RISK_REPEAT_HIGH_VALUE_ORDERS` |
| Completed orders only | Read `v_completed_order_activity`, which filters current status to `COMPLETED` |
| Exclude currently cancelled orders | Reuse the current-status view per the human decision in `evidence.md` |
| Configurable rolling hours | Read `regional_rule_config.window_hours` for the customer region |
| Configurable count and per-order amount | Read `event_count_threshold` and `amount_threshold` from the same regional row |
| Individual amount qualification | Filter each order with `order_amount >= amount_threshold` before aggregation |
| Customer count qualification | Group by customer/rule/config thresholds and use `HAVING COUNT(*) >= event_count_threshold` |
| Store count and total | Insert `COUNT(*)` and `SUM(order_amount)` into existing alert metric columns |
| Same-date duplicate suppression | Use `INSERT OR IGNORE` with the existing partial unique open-alert index |
| Negative and window cases | Filter below-amount rows and orders outside `(monitoring time - window, monitoring time]` |
| Regional isolation | Join rule configuration on rule ID and the order's customer region |
| Preserve existing rules | Add a third evaluator without changing either existing query or existing seed configuration |

## Proposed approach

1. Add the new rule definition and one configuration row for each existing
   region to `sql/seed.sql`. Each row uses the existing window, count, and
   amount columns.
2. Add one set-based `INSERT OR IGNORE ... SELECT` statement to
   `evaluate_rules` after the existing evaluators.
3. Source eligible rows from `v_completed_order_activity`. Filter by the
   regional per-order threshold and rolling-time bounds, group by customer and
   rule, then apply the regional count threshold.
4. Store the count and sum generated from exactly the filtered qualifying
   order rows.
5. Extend baseline project documentation to describe the third rule.
6. Create validation separately in the Stage 4 ticket-local test package.

No schema change is proposed. Existing columns, view, foreign keys, and partial
unique index are sufficient (`Sample-Projects/commerce-risk/sql/schema.sql`).

## Alternatives considered

### Add order-status history and a completion timestamp

Rejected for this ticket. The human decision excludes orders currently marked
`CANCELLED`, so historical completion eligibility is not required. Adding
history would materially expand the data model and migration surface.

### Add a dedicated configuration table for the new rule

Rejected. `regional_rule_config` already has all required parameter types and
one-row-per-rule/region grain. Another table would duplicate the existing
configuration interface.

### Implement row-by-row evaluation in Python

Rejected. Existing rules use set-based SQLite statements inside
`evaluate_rules`; another SQL statement is smaller, consistent, and
deterministic.

### Change the completed-order view to include window logic

Rejected. Monitoring time and regional window are evaluation parameters, not
stable view semantics. Keeping them in the evaluator avoids coupling the view
to one rule.

## Affected paths

All current and destination paths are repository-root-relative.

| Current source | Intended ticket-local proposed path | Intended destination | Change type |
|---|---|---|---|
| `Sample-Projects/commerce-risk/sql/seed.sql` | `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/sql/seed.sql` | `Sample-Projects/commerce-risk/sql/seed.sql` | Modify |
| `Sample-Projects/commerce-risk/risk_pipeline.py` | `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/risk_pipeline.py` | `Sample-Projects/commerce-risk/risk_pipeline.py` | Modify |
| `Sample-Projects/commerce-risk/README.md` | `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/README.md` | `Sample-Projects/commerce-risk/README.md` | Modify |

Stage 4 validation will be created under
`EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/tests/`; its
final destination suitability will be mapped there. No full test script is
created during design.

## Interfaces and data grain

### Input interface

- `monitoring_time`: existing text argument passed to `evaluate_rules`.
- `risk_rules`: one rule-definition row, independently enabled.
- `regional_rule_config`: one row per new rule and region containing all three
  non-null thresholds.
- `v_completed_order_activity`: one current completed order per row with
  customer, region, amount, and `ordered_at`.

### Evaluation grain

Eligible input grain is one completed order. Output candidate grain is one
customer, rule, and monitoring date. Aggregated metrics cover only orders that
meet status, amount, and time filters.

### Output interface

One open `alerts` row stores customer, rule, monitoring date,
`qualifying_event_count`, `qualifying_amount`, status, and creation time. No
column or return-type changes are proposed. `run_pipeline` will continue to
return `alerts_created` and `alerts_total`, now including the new rule where its
seed data qualifies.

## Configuration changes

Add four regional rows for the new rule. Proposed values must be fictional and
must exercise regional behavior while remaining easy to understand. Stage 3
should use independently written values and document them in the proposed
README. All `window_hours`, `event_count_threshold`, and `amount_threshold`
values must be non-null for this rule.

The requested `NORTH` values of 48 hours, three orders, and 600 units are
illustrative, not mandatory. Stage 3 may use those synthetic values for NORTH
and distinct synthetic values elsewhere if they support a coherent demo.

## Time and status semantics

- Eligibility is based on current `order_status = 'COMPLETED'`; current
  `CANCELLED` and `PENDING` orders are excluded.
- `ordered_at` is the only available order event timestamp and will be used as
  the rolling-window timestamp.
- Match current declined-payment semantics: lower bound exclusive and upper
  bound inclusive, expressed as
  `(monitoring_time - window_hours, monitoring_time]`.
- `monitoring_date` continues to be derived as `monitoring_time[:10]`.

The `ordered_at` choice is a documented compatibility assumption because the
current model has no separate completion timestamp.

## Duplicate-suppression and rerun behavior

The evaluator will use `INSERT OR IGNORE`. The existing partial unique index on
customer, rule, and monitoring date where status is `OPEN` remains the final
constraint. Re-evaluating the same database on the same monitoring date will
not add another open alert. If the earlier alert is closed, the schema permits
a new open alert; this preserves current behavior and is not changed by this
ticket.

The CLI rebuilds its target database before every complete run. Rerun validation
must therefore call `evaluate_rules` twice on the same built database when
checking duplicate suppression.

## Compatibility and downstream effects

- Existing evaluator SQL and existing configuration values remain unchanged.
- The alerts schema and Python result shape remain unchanged.
- Baseline alert totals may increase when the enhanced seed data intentionally
  contains a qualifying repeat-order customer. Tests must assert rule-specific
  results rather than assuming the former global total without accounting for
  the new rule.
- SQLite and Python standard-library-only execution remains intact.
- Consumers that enumerate rule codes may observe one new value; no such
  consumer exists in current source.

## Edge cases and error handling

- Exactly-at-amount and exactly-at-count cases qualify.
- An order exactly on the lower time boundary does not qualify; one exactly at
  monitoring time qualifies.
- Below-amount rows do not contribute to either count or total.
- Currently pending or cancelled rows do not qualify.
- Missing regional configuration produces no result through the inner join,
  matching current behavior. No new error path is introduced.
- A disabled rule produces no result.
- A customer cannot combine orders from another customer's region because
  region comes from each order's customer.
- Malformed timestamps remain outside scope; current CLI does not validate
  them.

## Performance and maintainability

The proposed evaluator scans the completed-order view and joins small rule and
configuration tables. This is proportionate for the compact sample. The schema
has no index on order status/time/customer beyond the primary key, so a larger
dataset could require an index after measurement. Adding one now is unnecessary
for the demonstrated scale and would expand scope.

Keeping the query adjacent to existing rule statements favors local
readability. Repeated query structure is acceptable for three compact rules;
generalizing a rule framework is not justified by current requirements.

## Validation strategy

Stage 4 should map every acceptance criterion to automated tests using a
temporary database assembled from approved proposed files. Required cases:

- exact rule code and independent disablement;
- qualifying count and stored total;
- below-count, below-amount, and outside-window negatives;
- exact count, amount, lower-time, and upper-time boundaries;
- current `CANCELLED` and `PENDING` exclusions;
- distinct regional configurations;
- same-date evaluation rerun and open-alert suppression;
- behavior after a different monitoring date where relevant;
- existing declined-payment and high-value-order regression expectations;
- seed/build/CLI compatibility at an isolated temporary path.

Generated tests must remain `Not Run` unless execution is genuinely recorded.
Any isolated run must be identified as temporary validation, not transfer or
deployment.

## Rollback strategy

Before transfer, rollback is removal of the ticket-local proposed files. After
a human-approved manual transfer, rollback would restore the prior versions of
the three destination files and rebuild the local database. Because no schema
migration is proposed and the demo database is rebuilt, no data migration
rollback is expected. Detailed commands belong to Stage 6 after independent
review.

## Risks and open questions

### Risks

- `ordered_at` may not represent completion time in a future richer model.
- Missing configuration silently suppresses evaluation, matching current code
  but potentially hiding configuration mistakes.
- Current timestamp parsing accepts caller input without validation.
- Closed same-date alerts permit a later open alert; this is existing schema
  behavior and may surprise a reader if not documented.

### Open questions carried as design assumptions

- The lower rolling boundary is exclusive and upper boundary inclusive, to
  match the existing declined-payment evaluator.
- `ordered_at` is the relevant event time because no completion timestamp
  exists.
- Missing configuration yields no result rather than an exception.
- A closed same-date alert may be followed by a new open alert.

These assumptions require approval with this design. The cancelled-order
question is resolved: current `CANCELLED` orders are excluded.

## Design acceptance status

- Requirement traceability: Met.
- Smallest compatible design: Met; no schema change.
- Exact source, proposed, and destination paths: Met.
- Grain, interfaces, configuration, and duplicate behavior: Met.
- Edge, performance, rerun, compatibility, and rollback considerations: Met.
- Validation strategy: Met.
- Risks and open questions: Met.
- Human design approval: Approved on 2026-08-14.

## Human design approval

- Status: Approved
- Approver: Repository owner
- Date: 2026-08-14
- Conditions: Approved by instruction to proceed to Prompt 6; includes the
  documented time-boundary, `ordered_at`, missing-configuration, and
  closed-alert assumptions.
