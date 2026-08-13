# Glossary

Definitions reflect the authoritative schema and evaluator in
`Sample-Projects/commerce-risk/sql/schema.sql` and
`Sample-Projects/commerce-risk/risk_pipeline.py`.

| Term | Meaning |
|---|---|
| Alert | A stored rule detection for a customer and monitoring date, with qualifying count and amount |
| Attempted amount | Amount associated with one payment attempt |
| Completed order activity | Curated order rows whose current status is `COMPLETED` |
| Customer | Fictional purchaser assigned to one region |
| Event count threshold | Minimum declined-attempt count configured for a rule and region |
| Monitoring date | First ten characters of the supplied monitoring timestamp, used in duplicate identity |
| Monitoring run | Record of one coordinated evaluation with timing and status |
| Monitoring time | Caller-supplied upper evaluation time |
| Open alert | Active alert participating in the partial uniqueness constraint |
| Order amount | Non-negative amount stored for one order; currency is unspecified |
| Payment attempt | One approved or declined payment event belonging to an order |
| Region | One of `NORTH`, `SOUTH`, `EAST`, or `WEST` |
| Regional rule configuration | Threshold values for one rule and one region |
| Risk rule | Enabled or disabled named evaluator definition |
| Window hours | Lookback duration for declined payment evaluation |

## Evidence notes

**Fact:** Status values and regions above are schema constraints.

**Assumption:** “Active” is a descriptive interpretation of `OPEN`; the project
does not implement an alert-review workflow.

**Unresolved question:** Currency and business ownership terminology are not
defined by the current project.
