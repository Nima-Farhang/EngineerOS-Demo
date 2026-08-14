# Curated Knowledge

This directory contains maintained context for the fictional Commerce Risk
sample project. Curated knowledge is secondary to the authoritative project
code in `Sample-Projects/commerce-risk/`. When documentation and code disagree,
use the code for current implemented behaviour and record the conflict.

All paths in these documents are relative to the repository root.

## Index

- [Architecture overview](architecture-overview.md) — components, data flow,
  boundaries, and operational model.
- [Data model](data-model.md) — tables, views, keys, and row grain.
- [Rule engine](rule-engine.md) — implemented evaluation and suppression logic.
- [Testing guide](testing-guide.md) — baseline coverage and human-run commands.
- [Debugging guide](debugging-guide.md) — reproducible inspection steps.
- [Glossary](glossary.md) — project-specific terms and status values.
- [Common investigations](common-investigations.md) — evidence routes for
  recurring questions.
- [Engineering decisions](engineering-decisions.md) — reusable reviewed
  workspace decisions.

## Knowledge lifecycle

```text
project code + curated knowledge + previous ticket evidence
                         ↓
          new investigation or ticket
                         ↓
        new evidence and human decisions
                         ↓
       proposed knowledge update + human review
```

Knowledge does not update automatically and never overrides project source.
