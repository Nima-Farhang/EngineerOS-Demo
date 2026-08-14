# EngineerOS Operating Workflow

EngineerOS is a persistent context and workflow layer around project
repositories. It supports read-only investigation and controlled ticket
development. All paths are repository-root-relative.

Before either mode, read `EngineerOS/AGENTS.md`, the operating rules, applicable
workspace instructions, and its `project-code/SOURCE-MANIFEST.yaml`.

## Question Mode

Use Question Mode for codebase explanation, impact investigation, and debugging
orientation. Follow `EngineerOS/prompts/question-mode.md`: inspect source before
summaries, classify evidence, cite paths, report gaps, remain read-only, and do
not create a ticket unless explicitly requested.

## Ticket Mode

Use one stage at a time. A later stage starts only when its prerequisite human
decision is explicitly recorded.

### 1. Intake and understanding

Trace requirements, state the outcome without designing it, inspect current
code and knowledge, identify scope/dependencies, and classify evidence.

**Checkpoint:** a human confirms understanding and resolves material ambiguity.

### 2. Design

Produce the smallest compatible design with traceability, affected paths,
interfaces/grain, configuration, edge cases, compatibility, rerun behavior,
validation, risk, and rollback considerations. Keep source read-only.

**Checkpoint:** a human approves the current design and assumptions.

### 3. Proposed development

Create complete proposed files only under
`EngineerOS/workspaces/<workspace>/tickets/<lifecycle>/<ticket>/implementation/proposed/<project-relative-path>`.
Maintain the manifest. Do not transfer or edit authoritative source.

### 4. Generated validation

Generate ticket-local tests and a criteria matrix. Mark tests `Not Run` until
genuinely executed. Name temporary execution as isolated validation—not
transfer, deployment, shared-environment validation, or production evidence.

### 5. Independent review

Review requirements, decisions, design, current code, proposal, manifest,
tests, and evidence. Use `blocked`, `changes_required`, or
`ready_for_manual_transfer_guidance`. Fix accepted findings separately and
review again.

### 6. Manual transfer, execution, and rollback guidance

After a ready review, document mapped paths, approvals, backups, integrity
checks, human transfer/execution, evidence, monitoring, rollback, and separately
controlled Git/release actions. Do not transfer or release.

## Lifecycle semantics

`tickets/completed/` means the EngineerOS understanding, design, proposal,
validation-generation, review, and handoff workflow is complete. It does **not**
mean transfer, destination execution, commit, deployment, or release.

- `not_transferred`: authoritative source was not changed from the proposal.
- `Not Run`: generated validation lacks recorded execution evidence.
- `ready_for_manual_transfer_guidance`: review supports handoff, not transfer.

## Knowledge retention

Project code, human-reviewed knowledge, and prior ticket evidence improve later
work. New reusable findings may be proposed for knowledge after human review.
Knowledge never updates itself or overrides current source.

Construction/improvement instructions are preserved separately in
`EngineerOS/docs/demo-build-history.md`.
