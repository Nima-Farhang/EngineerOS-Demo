# Architecture Decisions

## AD-001: Project source describes implemented behavior

Resolve source through the workspace manifest and use it as primary evidence
for current behavior. Requirements govern intended change.

## AD-002: Curated knowledge is secondary

Use reviewed knowledge for navigation, report conflicts, and defer to current
source because knowledge can become stale.

## AD-003: Project source is read-only by default

Question Mode, intake, and design do not modify authoritative code.

## AD-004: Proposed implementation is ticket-local

Complete proposed files and their manifest remain under a ticket until a human
decides whether to transfer them.

## AD-005: Design approval precedes development

Resolve material ambiguity and approve the current design before development.

## AD-006: Generated validation is not executed evidence

Tests begin as `Not Run`; source and expected results do not prove execution.

## AD-007: Humans control irreversible workflow actions

Humans retain control of transfer, result confirmation, source control,
rollback, and release.

## AD-008: Samples are synthetic and locally runnable

Samples use independently written fictional rules/data and lightweight tools,
with no production environment dependency.

## AD-009: Extensibility uses conventions

New contexts use `EngineerOS/workspaces/<workspace>/` and sibling projects use
`Sample-Projects/<project>/`; another demo is not required.
