# Task Understanding

## Outcome in plain language

The fictional Commerce Risk project needs a third rule that detects repeated
high-value completed orders for a customer during a configurable recent period.
The count, per-order amount, and rolling hours vary by region. A qualifying
alert must record the count and total amount without creating a second open
alert for the same customer, rule, and monitoring date. Existing rules must
continue to behave as they do now.

No solution is proposed or approved in this artifact.

## Sources inspected

| Source | Authority | Relevant evidence |
|---|---|---|
| `Sample-Projects/commerce-risk/risk_pipeline.py` | Current implementation | Build lifecycle, current rule evaluation, monitoring-date derivation, alert writes |
| `Sample-Projects/commerce-risk/sql/schema.sql` | Current implementation | Tables, views, configuration columns, constraints, duplicate index |
| `Sample-Projects/commerce-risk/sql/seed.sql` | Current implementation | Current rule definitions, regions, thresholds, and synthetic baseline |
| `Sample-Projects/commerce-risk/tests/test_pipeline.py` | Current generated validation | Existing expected behavior and coverage |
| `Sample-Projects/commerce-risk/README.md` | Project documentation | Architecture, commands, data grain, and limits |
| `EngineerOS/workspaces/commerce-risk/project-code/SOURCE-MANIFEST.yaml` | Source location control | Identifies the sibling project as authoritative and read-only by default |
| `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/source/feature-request.md` | Proposed requirement | Requested outcome, criteria, scope, constraints, and ambiguity |
| `EngineerOS/workspaces/commerce-risk/knowledge/README.md` and linked knowledge | Curated secondary context | Navigation and maintained explanations; secondary to source |
| `EngineerOS/platform/operating-rules.md` | Platform governance | Authority, evidence language, human checkpoints, and change isolation |

## Scope

### In scope

- Understand the requested rule, trace it to current project behavior, identify
  dependencies and likely affected areas, and expose uncertainty.
- Recognize required validation for qualifying, negative, boundary, regional,
  duplicate-suppression, and compatibility cases.

### Out of scope

- Selecting a schema or evaluator design.
- Editing authoritative source, proposing implementation files, or generating
  full test scripts.
- Resolving the cancellation ambiguity without an explicit human decision.
- Transfer, test execution, Git actions, or release activity.

## Current implementation

### Facts

- `risk_rules` supports an independently enabled unique rule code, and
  `regional_rule_config` has nullable `window_hours`,
  `event_count_threshold`, and `amount_threshold` columns with one row per rule
  and region (`Sample-Projects/commerce-risk/sql/schema.sql`).
- `orders` stores only its current `order_status`; there is no order-status
  history or completion timestamp distinct from `ordered_at`
  (`Sample-Projects/commerce-risk/sql/schema.sql`).
- `v_completed_order_activity` exposes only orders whose current status is
  `COMPLETED` (`Sample-Projects/commerce-risk/sql/schema.sql`).
- Alerts already store `qualifying_event_count` and `qualifying_amount`
  (`Sample-Projects/commerce-risk/sql/schema.sql`).
- A partial unique index restricts open alerts to one customer/rule/monitoring
  date, and current evaluators use `INSERT OR IGNORE`
  (`Sample-Projects/commerce-risk/sql/schema.sql` and
  `Sample-Projects/commerce-risk/risk_pipeline.py`).
- Existing Python evaluation implements declined-payment and high-value-order
  rules; no repeat-high-value rule exists
  (`Sample-Projects/commerce-risk/risk_pipeline.py`).
- The CLI rebuilds the database on every full pipeline invocation. A direct
  call to `evaluate_rules` evaluates the current database without rebuilding it
  (`Sample-Projects/commerce-risk/risk_pipeline.py`).

## Dependencies and likely affected areas

### Inferences

- Rule seed/configuration data will likely be affected because the requested
  rule needs a definition and four regional configurations
  (`Sample-Projects/commerce-risk/sql/seed.sql`).
- Rule evaluation will likely be affected because all current rule SQL is
  coordinated in `evaluate_rules`
  (`Sample-Projects/commerce-risk/risk_pipeline.py`).
- Tests and project documentation will likely need updates to demonstrate the
  new behavior and preserved baseline
  (`Sample-Projects/commerce-risk/tests/test_pipeline.py` and
  `Sample-Projects/commerce-risk/README.md`).
- Schema impact depends on the human cancellation decision. Excluding currently
  cancelled orders can use current-state data; including previously completed
  orders after cancellation cannot be established from the current model.

These are impact observations, not a proposed design.

## Evidence and uncertainty

### Facts

- The requirement calls for regional window, count, and per-order amount
  configuration, stored count and total, rerun suppression, and preservation of
  existing behavior
  (`EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/source/feature-request.md`).
- Current regional configuration already contains fields with those three value
  types (`Sample-Projects/commerce-risk/sql/schema.sql`).
- Current timestamps are text and rule SQL relies on SQLite `datetime()`
  (`Sample-Projects/commerce-risk/risk_pipeline.py`).

### Inferences

- The existing completed-order view could provide current-status eligibility,
  but using it would implicitly choose exclusion of currently cancelled orders.
- Boundary semantics must be made explicit during design because the requirement
  defines a rolling window but does not state whether its lower boundary is
  inclusive. The current declined-payment rule uses an exclusive lower boundary
  and inclusive upper boundary.
- Compatibility validation must retain the two baseline alert expectations in
  the current generated tests.

### Assumptions

- “Monitoring date” continues to mean the first ten characters of a valid
  monitoring timestamp, matching current code, unless a later approved design
  states otherwise.
- “Total qualifying amount” means the sum of the same individual orders counted
  toward the threshold; the requirement wording supports this interpretation,
  but it should be confirmed with Stage 1.
- Existing fictional regions remain the complete initial configuration set.

### Unresolved questions

1. If an order was once completed but is `CANCELLED` at monitoring time, is it
   excluded based on current status or included based on its earlier history?
2. Is the rolling window lower boundary exclusive or inclusive? Is the supplied
   monitoring time itself inclusive?
3. Does `ordered_at` represent the relevant completion time, or would a separate
   completion timestamp be required?
4. Should missing or incomplete regional configuration silently yield no result
   as current joins do, or be treated as a configuration error?
5. When a same-date alert was closed, may a later evaluation create a new open
   alert? The current index permits that behavior.

### Conflicts

- Workspace guidance describes stored procedures
  (`EngineerOS/workspaces/commerce-risk/instructions.md`), while authoritative
  source implements SQLite SQL coordinated by Python. For current behavior, the
  source is authoritative; the user has also directed continued use of SQLite
  and Python.
- No conflict was found between the proposed feature request and current alert
  storage capacity. The cancellation-history option conflicts with the amount
  of historical state currently available, not with an approved requirement
  decision, because that decision is still unresolved.

## Proportional ticket artifacts likely needed

- Stage 1: `ticket.md`, `task-understanding.md`, and `evidence.md`.
- Stage 2: `design.md` after explicit Stage 1 confirmation.
- Stage 3: ticket-local proposed source files, `implementation/changed-files.md`,
  and `implementation/change-manifest.yaml` after design approval.
- Stage 4: ticket-local tests and an acceptance-criteria validation matrix.
- Stage 5: `review.md`.
- Stage 6: `release-and-rollback.md` only after a ready review outcome.

## Stage 1 acceptance status

- Requirement sources traced: Met.
- Requested outcome captured without a solution: Met.
- Acceptance criteria and scope captured: Met.
- Current implementation facts cited: Met.
- Dependencies and likely affected areas identified: Met.
- Evidence classifications and conflicts recorded: Met.
- Cancellation ambiguity preserved: Met; human decision outstanding.
- Human confirmation: Pending.

## Human confirmation

- Status: Confirmed
- Decision reference: `evidence.md` Stage 1 human decision dated 2026-08-13
