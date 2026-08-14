# Ticket

## Identity

- Ticket ID: `DEMO-001`
- Title: Add configurable repeat high-value orders rule
- Owner: Human owner not assigned
- Status: EngineerOS Workflow Complete — Handoff Ready

## Requirement sources

| Source | Authority | Version/date |
|---|---|---|
| `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/source/feature-request.md` | Proposed ticket requirement | Undated; inspected 2026-08-13 |

## Requested outcome

Add a separately enabled, regionally configurable rule named
`RISK_REPEAT_HIGH_VALUE_ORDERS`. At a supplied monitoring time, it must identify
customers with a configured minimum number of individually high-value completed
orders inside a configured rolling-hour window, store the qualifying count and
total, suppress duplicate open alerts for the same customer/rule/date, and
preserve existing rules.

This is an outcome statement only. No implementation approach is approved at
Stage 1.

## Acceptance criteria

- [ ] The rule uses the exact code `RISK_REPEAT_HIGH_VALUE_ORDERS` and can be
  enabled or disabled independently.
- [ ] Only orders eligible under a human-confirmed completed-order interpretation
  are evaluated.
- [ ] Rolling window hours are configurable and relative to monitoring time.
- [ ] Count and per-order amount thresholds are independently configurable by
  region.
- [ ] Each qualifying order meets or exceeds its regional amount threshold.
- [ ] A customer meets or exceeds the configured qualifying-order count.
- [ ] The alert stores the qualifying count and summed qualifying amount.
- [ ] Same-customer/rule/monitoring-date reruns do not create a duplicate open
  alert.
- [ ] Below-count, below-amount, and outside-window cases do not alert.
- [ ] Configuration for one region does not affect another region.
- [ ] Existing declined-payment and high-value-order behavior is preserved.

## Scope and constraints

### In scope

- A configurable batch rule, regional configuration, alert metrics, duplicate
  suppression, and automated validation.
- Deterministic operation at a supplied monitoring time using SQLite and
  Python's standard library.

### Out of scope

- Changes to existing rule requirements or thresholds.
- Alert-review workflows, notifications, scoring, currency conversion, refunds,
  streaming, external services, production deployment, or historic backfill.

### Required human checkpoints

- Confirm this task understanding and decide the cancelled-after-completion
  interpretation before design.
- Approve the subsequent design before proposed development.
- Decide whether proposed files are transferred, execute tests, confirm results,
  and separately approve source-control or release actions.
