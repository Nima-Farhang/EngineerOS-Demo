# Engineering Decisions

This retained context is secondary to source and approved requirements.

## SQLite and Python coordination

Use SQLite plus Python's standard library so the sample remains portable and
compact. Evidence: `Sample-Projects/commerce-risk/risk_pipeline.py`.

## Current status determines completed-order eligibility

For DEMO-001, a currently `CANCELLED` order is excluded even if previously
completed. Evidence:
`EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/evidence.md`.
The model has no status history.

## Rolling-window convention

DEMO-001 uses an exclusive lower boundary and inclusive monitoring time,
matching the declined-payment evaluator. Evidence:
`EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/design.md` and
`Sample-Projects/commerce-risk/risk_pipeline.py`.

Human review is required before changing a retained decision.
