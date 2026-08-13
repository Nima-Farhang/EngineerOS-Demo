# Data Model

The schema authority is `Sample-Projects/commerce-risk/sql/schema.sql`.

## Tables and grain

| Object | Row grain | Key and important relationships |
|---|---|---|
| `customers` | One customer | `customer_id`; region is one of four fixed values |
| `orders` | One order | `order_id`; belongs to one customer |
| `payments` | One payment attempt | `payment_id`; belongs to one order |
| `risk_rules` | One rule definition | `rule_id`; `rule_code` is unique |
| `regional_rule_config` | One rule and region | Composite key; belongs to one rule |
| `monitoring_runs` | One pipeline run | Generated `run_id` |
| `alerts` | One detected customer/rule/date while open | Generated `alert_id`; belongs to a customer and rule |

## Curated views

- `v_customer_payment_activity` has one row per payment attempt and adds the
  order's customer and the customer's region.
- `v_completed_order_activity` has one row per completed order and adds customer
  and region context. Pending and cancelled orders are excluded.

Both definitions are in `Sample-Projects/commerce-risk/sql/schema.sql`.

## Constraints

**Fact:** Customer regions are `NORTH`, `SOUTH`, `EAST`, or `WEST`. Order,
payment, run, and alert statuses have explicit check constraints. Monetary
values cannot be negative. Foreign keys are enabled for every connection by
`Sample-Projects/commerce-risk/risk_pipeline.py`.

**Fact:** A partial unique index permits at most one `OPEN` alert for a given
customer, rule, and monitoring date. A closed alert does not occupy that unique
slot (`Sample-Projects/commerce-risk/sql/schema.sql`).

**Inference:** More than one closed alert for the same customer, rule, and date
is structurally possible because the uniqueness condition applies only to open
rows.

**Assumption:** Timestamps are stored as comparable UTC text accepted by
SQLite's `datetime()` function.

**Unresolved question:** The schema does not specify a currency for amount
columns.

## Seed profile

The deterministic seed contains four fictional customers, six orders, five
payment attempts, two enabled rules, and regional configuration for both rules
(`Sample-Projects/commerce-risk/sql/seed.sql`). Seed values are examples, not
general business requirements.
