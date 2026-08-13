# Architecture Overview

## Facts

- The authoritative project is a Python standard-library and SQLite batch
  application under `Sample-Projects/commerce-risk/`. Its documented entry
  point is `Sample-Projects/commerce-risk/run_pipeline.py`.
- Database creation and rule evaluation are implemented in
  `Sample-Projects/commerce-risk/risk_pipeline.py`.
- Schema and deterministic inputs are separate SQL files:
  `Sample-Projects/commerce-risk/sql/schema.sql` and
  `Sample-Projects/commerce-risk/sql/seed.sql`.
- A run rebuilds the target database, loads the seed data, creates a monitoring
  run, evaluates both enabled rules, and completes the run. The rebuild removes
  an existing database at the supplied path
  (`Sample-Projects/commerce-risk/risk_pipeline.py`).
- The project has no external service or third-party package dependency
  (`Sample-Projects/commerce-risk/README.md`).

```text
schema.sql + seed.sql
         |
         v
   SQLite database <--- run_pipeline.py
         |
         v
 two curated views
         |
         v
 configured SQL rule evaluation ---> alerts
```

## Boundaries

The sample is a local, single-process teaching project. Authentication,
streaming ingestion, user interfaces, external integrations, and production
operations are explicitly outside its stated limits
(`Sample-Projects/commerce-risk/README.md`).

## Inferences

- Rebuilding on each CLI run favors reproducibility and reviewer comprehension
  over preserving operational history.
- SQL performs the data-intensive evaluation while Python coordinates schema,
  seed, run-state, and connection lifecycle.

## Assumptions

- ISO-like UTC input timestamps are supplied in the same format as the seed
  data. The CLI does not validate or normalize the monitoring-time argument.

## Unresolved questions

- The code records a `FAILED` monitoring status as an allowed value, but no
  exception path currently writes that status.

## Conflicts

- Workspace guidance mentions stored procedures
  (`EngineerOS/workspaces/commerce-risk/instructions.md`), but the authoritative
  SQLite implementation uses SQL statements coordinated by Python. SQLite does
  not provide conventional stored procedures.
