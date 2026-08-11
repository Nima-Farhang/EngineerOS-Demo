# Codex Build Workflow for the Portfolio Repository

This document contains the exact prompts to give Codex. Run them **one at a
time**, in order, from the repository root. Review the diff after every prompt
and commit each accepted stage separately.

## Non-negotiable clean-room rule

Do not give Codex access to the private workplace repository while developing
this public version. Do not ask it to “anonymise,” “translate,” or “rename”
private files. Build the public demo only from this starter repository and the
fictional requirements below.

---

## Prompt 0 — Repository safety and orientation

```text
Read README.md, AGENTS.md, platform.yaml, platform/operating-rules.md,
workflows/ticket-development.md, workspaces/commerce-risk/instructions.md, and
this WORKFLOW.md.

Do not modify files yet.

Inspect the current repository and report:
1. the intended architecture and operating model;
2. the public-demo confidentiality boundary;
3. missing components required for a credible portfolio demonstration;
4. a proposed implementation sequence that follows the stages in WORKFLOW.md;
5. any conflict or ambiguity in the current instructions.

All project names, rules, data, thresholds, people, organisations, and
infrastructure must remain fictional and independently created. Do not request
or use any employer or client source material.
```

Human action: confirm that Codex understands the clean-room boundary before
continuing.

---

## Prompt 1 — Build the synthetic sample project

```text
Implement only the synthetic sample project under:
workspaces/commerce-risk/project-code/sample-project

Read and follow AGENTS.md and the operating rules. Do not modify ticket
artifacts yet.

Create a small, coherent, locally understandable Commerce Risk Monitoring data
project. Use standard SQL that is easy to read and can run with SQLite where
practical. The project must be wholly fictional.

Required capabilities:
- synthetic customers, orders, payments, configurable risk rules, and alerts;
- SQL DDL for approximately 5 to 7 tables;
- at least 2 curated views;
- a deterministic rule-evaluation implementation, using SQL and/or Python;
- synthetic seed data with no real people or organisations;
- one command that builds the local database and runs the sample pipeline;
- automated tests for the baseline behaviour;
- a project README explaining architecture, data grain, execution, and limits.

Suggested baseline rules, which may be refined but must remain fictional:
1. flag a customer with at least three declined payments within 24 hours;
2. flag a single order above a configurable regional threshold;
3. do not create duplicate open alerts for the same customer, rule, and
   monitoring date.

Keep the implementation compact enough for a reviewer to understand in about
15 minutes. Prefer Python standard library plus SQLite; avoid external cloud
services and unnecessary dependencies.

After implementation:
- run the project and its tests locally;
- report files changed, commands run, and actual results;
- clearly separate executed evidence from expected behaviour;
- do not build the demo ticket yet.
```

Human action: run the commands independently and inspect the generated data.
Commit as: `feat: add synthetic commerce risk sample project`.

---

## Prompt 2 — Create curated workspace knowledge

```text
Create concise, manually reviewable documentation under:
workspaces/commerce-risk/knowledge

Use the actual synthetic sample-project source as the highest authority. Do not
invent components that are not implemented. Do not change project code.

Create:
- architecture-overview.md
- data-model.md
- rule-engine.md
- testing-guide.md
- debugging-guide.md
- glossary.md

Each document must cite relevant repository-relative source paths. Clearly mark
facts, inferences, assumptions, and unresolved questions where applicable.
Avoid repeating the entire source code. Explain enough for a new engineer or
coding agent to navigate the project efficiently.

Also update workspaces/commerce-risk/knowledge/README.md with an index and a
statement that curated knowledge is secondary to project code.

Run repository validation and report the result.
```

Commit as: `docs: add curated commerce risk knowledge`.

---

## Prompt 3 — Create a fictional requirement source

```text
Create a fictional feature request at:
workspaces/commerce-risk/tickets/completed/DEMO-001/source/feature-request.md

Do not implement the feature and do not alter sample-project source.

The requirement should request a new configurable rule named
RISK_REPEAT_HIGH_VALUE_ORDERS with this fictional behaviour:
- evaluate completed orders only;
- within a configurable rolling number of hours;
- create an alert when a customer has at least a configurable number of orders,
  each at or above a configurable per-order amount;
- calculate and store the qualifying order count and total qualifying amount;
- suppress duplicate open alerts for the same customer, rule, and monitoring
  date;
- support regional configuration;
- preserve existing rule behaviour.

Include:
- business context;
- explicit acceptance criteria;
- in-scope and out-of-scope items;
- constraints;
- one deliberate but realistic ambiguity concerning whether cancelled orders
  after initial completion remain eligible.

Use only synthetic values and names. The ambiguity must be visible rather than
silently resolved.
```

Commit as: `docs: add fictional DEMO-001 requirement`.

---

## Prompt 4 — Stage 1: understand DEMO-001

```text
Work only on Stage 1 — Intake and Understanding for DEMO-001.

Ticket path:
workspaces/commerce-risk/tickets/completed/DEMO-001

Requirement source:
workspaces/commerce-risk/tickets/completed/DEMO-001/source/feature-request.md

Read the operating rules, workspace instructions, requirement source, project
manifest, relevant sample-project code, and relevant curated knowledge.
Initialise missing ticket files from the ticket template without overwriting
source documents.

Create or update ticket.md and task-understanding.md. Include:
- traceable requirement sources;
- requested outcome without proposing a solution;
- acceptance criteria;
- current implementation facts with source paths;
- dependencies and likely affected areas;
- facts, inferences, assumptions, unresolved questions, and conflicts;
- the deliberate cancelled-order ambiguity as unresolved;
- proportional ticket artifacts likely to be needed.

Do not design or implement the solution. Do not edit sample-project source.
Stop with the human-confirmation status Pending and report the Stage 1
acceptance-criteria status.
```

Human action: decide the ambiguity for the demo. Recommended fictional decision:
“Orders cancelled before the monitoring run are excluded.” Record the decision
in `evidence.md`, including your name/date and scope.

Commit as: `docs: complete DEMO-001 task understanding`.

---

## Prompt 5 — Stage 2: design DEMO-001

```text
Work only on Stage 2 — Design for DEMO-001.

Read all DEMO-001 artifacts and verify that evidence.md contains explicit human
confirmation of Stage 1, including the cancelled-order decision. If it does
not, stop without designing.

Keep the sample project read-only. Inspect only the relevant code and knowledge.
Create design.md with:
- requirement traceability;
- the smallest compatible design;
- alternatives considered;
- exact affected source and intended destination paths;
- data grain and interfaces;
- configuration changes;
- duplicate-suppression behaviour;
- edge cases, performance, rerun, compatibility, and rollback considerations;
- validation strategy;
- risks and open questions;
- approval status Pending.

Do not create implementation files or full test scripts. Report the design
acceptance-criteria status and stop for explicit human approval.
```

Human action: review the design and record explicit approval in `evidence.md`.
Commit as: `docs: design DEMO-001 rule change`.

---

## Prompt 6 — Stage 3: develop proposed changes

```text
Work only on Stage 3 — Develop Proposed Changes for DEMO-001.

Verify explicit human approval of the current design in evidence.md. If approval
is absent or does not cover the current design, stop.

Keep authoritative sample-project files unchanged. For every approved change,
create a proposed file under:
workspaces/commerce-risk/tickets/completed/DEMO-001/implementation/proposed/<project-relative-path>

Preserve the intended destination hierarchy. Implement only the approved
scope. Update:
- implementation/changed-files.md
- implementation/change-manifest.yaml

Each manifest entry must include source path, proposed path, change type, reason,
intended destination, review status, and transfer status.

Perform static checks and syntax checks that do not require modifying project
source. Do not execute the proposed change against the authoritative sample
project. Do not mark anything transferred. Report files changed and validation
actually performed.
```

Commit as: `feat: add ticket-local DEMO-001 proposed changes`.

---

## Prompt 7 — Stage 4: generate tests

```text
Work only on Stage 4 — Generate Validation for DEMO-001.

Read the confirmed requirement, approved design, current sample-project source,
and proposed implementation. Create ticket-local validation under:
workspaces/commerce-risk/tickets/completed/DEMO-001/tests

Include:
- automated unit or integration tests suitable for the proposed destination;
- a validation matrix mapping every acceptance criterion to one or more tests;
- positive, negative, boundary, rerun, duplicate-suppression, regional
  configuration, and cancelled-order cases;
- clear expected results;
- instructions for a human to execute the validation after manual transfer.

Do not alter authoritative sample-project source. You may run isolated tests
against a temporary copy assembled from the proposed files, provided the
process is reproducible and does not overwrite source.

Record generated artifacts in evidence.md. Record actual isolated execution
only if it was genuinely run, including command, context, and result. Never
represent isolated temporary execution as deployment or shared-environment
validation.
```

Commit as: `test: add DEMO-001 validation package`.

---

## Prompt 8 — Stage 5: independent review

```text
Act as an independent reviewer for DEMO-001. Do not change implementation or
test files during the first review pass.

Review the requirement, human decisions, approved design, current project code,
proposed files, manifest, tests, and evidence. Inspect for:
- acceptance-criteria coverage;
- correctness and determinism;
- duplicate alert behaviour;
- data-grain mistakes;
- boundary and cancelled-order handling;
- backward compatibility;
- rerun safety;
- maintainability and unnecessary complexity;
- mismatch between proposed files and manifest;
- unsupported claims of executed validation;
- accidental modification of authoritative sample-project source.

Write review.md with severity-ranked findings, evidence paths, required
disposition, and one allowed outcome:
- blocked
- changes_required
- ready_for_manual_transfer_guidance

Do not fix findings in this prompt. Report the review outcome.
```

Human action: where findings exist, ask Codex in a separate prompt to fix only
accepted findings, then rerun Prompt 8 until the outcome is
`ready_for_manual_transfer_guidance`.

Commit as: `docs: review DEMO-001 proposed change`.

---

## Prompt 9 — Stage 6: release and rollback guidance

```text
Work only on Stage 6 — Manual Transfer, Execution, and Rollback Guidance for
DEMO-001.

Proceed only if review.md says ready_for_manual_transfer_guidance. Do not copy
files into the authoritative sample project and do not perform Git actions.

Create or update release-and-rollback.md with:
- preconditions and required approvals;
- ordered mapping from proposed paths to intended destinations;
- pre-transfer integrity checks;
- manual transfer instructions;
- commands a human can run to rebuild the local sample database and execute
  tests after transfer;
- expected results and evidence to capture;
- post-change monitoring;
- explicit rollback triggers;
- ordered rollback instructions;
- separately controlled source-control and release actions.

Cross-check every path against change-manifest.yaml. Keep transfer statuses as
not_transferred until human evidence exists. Report completion status.
```

Commit as: `docs: add DEMO-001 release and rollback guidance`.

---

## Prompt 10 — Add repository-level quality controls

```text
Improve repository-level quality controls without changing the business
behaviour of the sample project or DEMO-001.

Add or enhance:
- structural validation for required ticket artifacts;
- validation of change-manifest required fields and referenced paths;
- checks that proposed files remain ticket-local;
- checks that generated tests are not described as executed without evidence;
- public-safety scans for emails, private URLs, credentials, workplace terms,
  and prohibited binary document types;
- Markdown link checking where practical;
- GitHub Actions to run repository validation and sample-project tests.

Use lightweight, maintainable tooling. Document local commands. Run all checks
and report actual results.
```

Commit as: `ci: add portfolio repository quality gates`.

---

## Prompt 11 — Produce the portfolio presentation layer

```text
Prepare the repository for an external engineering reviewer.

Do not change sample business behaviour. Improve README.md and docs with:
- the problem this workstation solves;
- architecture and source-authority model;
- human checkpoints;
- a concise end-to-end DEMO-001 walkthrough;
- exact local setup and demo commands;
- an architecture diagram using Mermaid;
- a workflow diagram using Mermaid;
- design tradeoffs and limitations;
- repository structure;
- a 5-minute recruiter walkthrough and a 15-minute engineer walkthrough;
- a clear statement that all data and rules are synthetic;
- a section explaining that the project demonstrates engineering judgement,
  not autonomous production deployment.

Remove empty or redundant documentation. Keep the main README scannable and
link to deeper documents. Run all validation and tests, then report results.
```

Commit as: `docs: complete portfolio presentation`.

---

## Prompt 12 — Final public-release audit

```text
Perform a final public-release audit of the entire repository and Git history.
Do not modify files during the first pass.

Check for:
- employer, client, employee, or customer names;
- workplace email addresses, URLs, paths, ticket numbers, system names, rules,
  thresholds, screenshots, document metadata, or copied wording;
- secrets, tokens, connection strings, private keys, and environment IDs;
- unexpected binaries, archives, emails, PDFs, Office files, or nested .git
  directories;
- generated claims presented as executed evidence;
- broken setup commands, tests, links, or GitHub Actions;
- licensing or attribution issues;
- unnecessary personal information in commit metadata.

Run repository validation, sample-project tests, and an available secret scanner
such as gitleaks if installed. Produce `docs/public-release-audit.md` with:
- scope;
- commands and tools actually run;
- findings;
- required remediation;
- residual risks;
- final recommendation: blocked or ready_for_publication.

Do not claim ready_for_publication if any material issue remains.
```

Only publish after reviewing this audit yourself.
