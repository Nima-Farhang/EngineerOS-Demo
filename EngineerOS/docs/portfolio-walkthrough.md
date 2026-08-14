# Portfolio Walkthrough

All repository paths below are relative to the repository root. All business
content is fictional and independently written.

## Five-minute recruiter walkthrough

### Minute 0–1: understand the proposition

Read the root `README.md`. The key idea is a visible, human-controlled process
for using an agent without treating generated output as automatically approved,
tested, or deployed.

### Minute 1–2: see the separation

Compare `EngineerOS/` with `Sample-Projects/commerce-risk/`. The workstation
contains rules, knowledge, and tickets; the sibling directory contains runnable
authoritative code.

### Minute 2–3: run the demo

```bash
python EngineerOS/scripts/validate_repository.py
python Sample-Projects/commerce-risk/run_pipeline.py \
  --database /tmp/commerce-risk-demo.db \
  --monitoring-time 2026-01-15T12:00:00Z
```

The baseline pipeline should report two alerts in the temporary database.

### Minute 3–4: follow one decision

Open `EngineerOS/workspaces/commerce-risk/tickets/completed/DEMO-001/` and trace
the cancellation ambiguity from `source/feature-request.md` to the human decision
in `evidence.md`, then into `design.md` and generated tests.

### Minute 4–5: see the control boundary

Read `review.md` and `release-and-rollback.md`. The proposal was reviewed and
guidance exists, but transfer remains `not_transferred` and feature tests remain
`Not Run`. That distinction is the central portfolio claim.

## Fifteen-minute engineer walkthrough

### Minutes 0–3: current source

Inspect:

- `Sample-Projects/commerce-risk/sql/schema.sql`
- `Sample-Projects/commerce-risk/sql/seed.sql`
- `Sample-Projects/commerce-risk/risk_pipeline.py`
- `Sample-Projects/commerce-risk/tests/test_pipeline.py`

Confirm the seven tables, two views, two baseline rules, deterministic seed, and
partial unique index for open-alert suppression.

### Minutes 3–5: authority and understanding

Read `EngineerOS/platform/operating-rules.md`, then compare the DEMO-001
requirement with `task-understanding.md`. Note the explicit Fact, Inference,
Assumption, Unresolved question, and Conflict classifications.

### Minutes 5–8: approved design

Read `design.md`. Focus on the decision to avoid a schema change, reuse current
regional configuration, exclude current cancelled orders, use `ordered_at`, and
match the existing lower-exclusive/upper-inclusive window convention.

### Minutes 8–10: proposal isolation

Compare the three files under `implementation/proposed/` with their destinations
in `Sample-Projects/commerce-risk/`. Cross-check the mappings and
`not_transferred` states in `implementation/change-manifest.yaml`.

### Minutes 10–12: validation honesty

Read `tests/validation-matrix.md` and the eleven generated feature tests. Then
open `evidence.md`: syntax and structural checks are executed evidence, while
feature tests remain explicitly `Not Run`.

### Minutes 12–14: independent review

Read `review.md`. Its first pass found two gaps, a separate authorized fix pass
addressed them, and the second pass reached
`ready_for_manual_transfer_guidance` without claiming runtime success.

### Minutes 14–15: controlled handoff

Scan `release-and-rollback.md` for exact path mapping, backup, isolated test
execution, evidence capture, monitoring, rollback triggers, and separately
controlled Git/release actions.

## What this demonstrates

- Requirements and code are treated as different kinds of authority.
- Ambiguity is visible and resolved before design.
- The smallest compatible design is preferred over unnecessary architecture.
- Proposed code, generated tests, executed evidence, and deployed behavior are
  never conflated.
- Review findings have traceable disposition.
- Rollback and human ownership are designed before transfer.

## What this does not demonstrate

- Autonomous production deployment
- Production security, scale, availability, or observability
- External environment integration
- Replacement of engineering review or accountability
