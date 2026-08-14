# Commerce Risk Workspace Instructions

## Fictional domain

The sample platform detects potentially risky purchase behaviour for a
fictional online retailer. It is not based on a real employer, customer, or
production system.

## Intended sample architecture

Synthetic order and payment rows flow into relational tables. Curated views
standardise customer activity. Set-based SQLite statements coordinated by
Python evaluate configurable risk rules and write alert records for review.

## Naming

Use neutral fictional names such as:

- schemas: `staging`, `risk`, `reporting`
- entities: customers, orders, payments, risk rules, alerts
- regions: `NORTH`, `SOUTH`, `EAST`, `WEST`

Do not use casino, gaming, AML, transaction-monitoring, employer, or internal
platform terminology.

## Technical scope

Keep the demo runnable locally with lightweight tooling. Prefer SQL files,
Python validation scripts, YAML configuration, Markdown documentation, and
GitHub Actions. Avoid cloud dependencies unless they are optional and mocked.
