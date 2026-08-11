# Repository Instructions for Coding Agents

Read these files before making changes:

1. `platform/operating-rules.md`
2. `workflows/ticket-development.md`
3. the applicable workspace `instructions.md`
4. the current ticket artifacts

## Public-demo boundary

This repository must remain a clean-room demonstration. Never introduce:

- employer, client, employee, customer, or internal project names;
- workplace ticket numbers, email addresses, URLs, file paths, screenshots,
  documents, code, schemas, rules, thresholds, or architecture details;
- credentials, connection strings, tokens, or environment identifiers;
- copied or lightly renamed proprietary material.

All business rules, source data, identities, thresholds, and system names must
be fictional and independently written for this repository.

## Working rules

- Treat sample project code as authoritative for current implemented behaviour.
- Distinguish facts, inferences, assumptions, unresolved questions, and conflicts.
- Keep project source read-only unless a prompt explicitly authorises a change.
- Put proposed project changes under the ticket's `implementation/proposed/` tree.
- Do not claim generated tests were executed.
- Stop at required human checkpoints.
