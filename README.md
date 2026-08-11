# AI Engineering Workstation

A clean-room portfolio demonstration of an evidence-led, human-controlled
workflow for AI-assisted software and data engineering.

The repository shows how a coding agent can:

- investigate an unfamiliar codebase using source authority;
- separate facts, inferences, assumptions, and unresolved questions;
- design before implementation;
- create ticket-local proposed changes without silently editing source;
- generate tests without claiming they were executed;
- perform an independent review;
- prepare manual transfer, validation, and rollback guidance.

## Current status

This is the minimum starter repository. Follow [`WORKFLOW.md`](WORKFLOW.md) to
have Codex build the synthetic sample project, documentation, completed demo
ticket, validation tooling, and final portfolio presentation.

## Public-safe design

All systems, data, rules, thresholds, tickets, and people in this repository
must be fictional. Do not import or lightly rename employer or client material.

## Start

```bash
python scripts/validate_repository.py
```

Then run the prompts in `WORKFLOW.md` sequentially, reviewing and committing the
result after each stage.
