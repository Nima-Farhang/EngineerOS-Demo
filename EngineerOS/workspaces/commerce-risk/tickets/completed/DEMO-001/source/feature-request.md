# Feature Request: Repeat High-Value Orders

## Request identity

- Reference: `DEMO-001`
- Requested rule code: `RISK_REPEAT_HIGH_VALUE_ORDERS`
- Domain: Fictional Commerce Risk Monitoring
- Status: Proposed

## Business context

The fictional retailer's review team can currently identify an individual
completed order that meets a regional amount threshold. The team also wants to
identify customers who place several qualifying completed orders within a
short period, even when each order is reviewed as a separate purchase.

The requested outcome is a configurable rule that summarizes this repeated
behavior for review without changing the behavior of existing rules.

## Requested behavior

For each customer, `RISK_REPEAT_HIGH_VALUE_ORDERS` must:

1. evaluate completed orders only;
2. use a configurable rolling lookback window measured in hours;
3. count orders whose individual order amount is at or above the configured
   per-order amount for the customer's region;
4. create an alert when the qualifying order count is at or above the
   configured count threshold;
5. store both the qualifying order count and the sum of qualifying order
   amounts on the alert;
6. suppress another open alert for the same customer, rule, and monitoring
   date; and
7. leave existing rules and their results unchanged.

Illustrative synthetic configuration may use a 48-hour lookback, three orders,
and a per-order amount of 600 units for `NORTH`. These are examples only; the
values must remain regionally configurable rather than hard-coded behavior.

## Acceptance criteria

- [ ] The new rule is identified by the exact code
  `RISK_REPEAT_HIGH_VALUE_ORDERS` and can be enabled or disabled independently.
- [ ] Evaluation includes only orders eligible as completed under the confirmed
  interpretation of the order-status ambiguity below.
- [ ] The rolling window duration is configurable in whole hours and is applied
  relative to the supplied monitoring time.
- [ ] The qualifying-order count threshold and per-order amount threshold are
  independently configurable by region.
- [ ] An order qualifies only when its own amount is greater than or equal to
  the applicable per-order amount threshold.
- [ ] A customer qualifies only when their qualifying-order count is greater
  than or equal to the applicable count threshold.
- [ ] A created alert stores the qualifying order count and total amount of the
  qualifying orders used by the evaluation.
- [ ] Evaluation does not create more than one open alert for the same customer,
  rule, and monitoring date, including on a same-date rerun.
- [ ] Customers below the count threshold, orders below the amount threshold,
  and orders outside the rolling window do not cause an alert.
- [ ] Regional configuration is honored without one region's values affecting
  another region.
- [ ] Existing declined-payment and high-value-order behavior remains unchanged.

## Scope

### In scope

- Rule definition and regional configuration for window hours, order count, and
  per-order amount.
- Deterministic batch evaluation at a supplied monitoring time.
- Alert creation with qualifying count and total amount.
- Same-date open-alert duplicate suppression.
- Automated validation for qualifying, non-qualifying, boundary, regional, and
  rerun cases.

### Out of scope

- Changes to the existing rule definitions or their thresholds.
- Alert review, assignment, notification, or user-interface workflows.
- Currency conversion, refunds, payment-attempt behavior, or customer scoring.
- Streaming evaluation, external services, or production deployment.
- Retroactive recalculation of alerts created before this rule is introduced.

## Constraints

- All data, names, regions, dates, and threshold examples must remain synthetic.
- The implementation must remain locally runnable with SQLite and Python's
  standard library.
- Configuration must use the existing fictional regions: `NORTH`, `SOUTH`,
  `EAST`, and `WEST`.
- Evaluation must be deterministic for the same database state, configuration,
  and monitoring time.
- Existing rule behavior and existing alert duplicate-suppression behavior must
  be preserved.

## Unresolved requirement ambiguity

An order may initially reach `COMPLETED` status and later be changed to
`CANCELLED` before a monitoring run. It is deliberately unresolved whether the
new rule should:

- exclude the order because its current status at monitoring time is
  `CANCELLED`; or
- include the order because it was completed during the rolling window before
  its later cancellation.

The current source stores one current order status and does not record status
history (`Sample-Projects/commerce-risk/sql/schema.sql`). A human decision is
required before design because the second interpretation may require additional
data not present in the current model. This feature request does not select an
interpretation.
