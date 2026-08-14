# Demo Build and Improvement History

This document preserves the staged instructions used to construct and improve
the public demonstration. It is historical/reproduction guidance, not the
primary workflow for day-to-day use. Use `EngineerOS/WORKFLOW.md` for Question
Mode and Ticket Mode.

You are working in the `EngineerOS-Demo` repository.

Your objective is to improve EngineerOS so that it more accurately demonstrates the operating model of a reusable AI-assisted engineering workstation while remaining a completely synthetic, clean-room, public-safe portfolio project.

Do NOT attempt to make the sample project resemble any real employer system or production architecture.

## Core objective

EngineerOS should demonstrate this concept:

> A persistent engineering context and workflow layer around project repositories that enables an AI coding agent to understand a codebase, answer engineering questions from evidence, investigate issues, develop controlled ticket changes, generate validation, review proposals, retain engineering knowledge, and prepare human-controlled implementation guidance.

The repository should demonstrate BOTH:

1. **Question / investigation mode**

   * understand an unfamiliar project;
   * answer engineering questions from project code and curated knowledge;
   * distinguish facts, inferences, assumptions, conflicts and unresolved questions;
   * remain read-only.

2. **Ticket development mode**

   * understand a requirement;
   * resolve ambiguity through human checkpoints;
   * design before development;
   * create ticket-local proposed changes;
   * generate validation without misrepresenting execution;
   * independently review the proposal;
   * prepare manual transfer, execution and rollback guidance;
   * keep authoritative source human-controlled.

The existing DEMO-001 is a good ticket-development example and should be preserved unless a correction is genuinely necessary.

---

# Mandatory safety boundary

This is a clean-room public demo.

Never introduce or infer:

* employer or client names;
* real workplace project names;
* real ticket identifiers;
* workplace email addresses;
* internal URLs;
* screenshots or copied documents;
* proprietary schemas or object names;
* real thresholds or business rules;
* real infrastructure paths;
* real cloud environment identifiers;
* credentials or connection strings;
* copied or lightly renamed workplace code;
* casino, gaming, AML or transaction-monitoring domain architecture;
* details from any external/private repository that are not already synthetic material in this repository.

Do not try to make the sample technically resemble a particular real-world employer platform.

Preserve the fictional `commerce-risk` domain.

Use only independently written synthetic examples.

---

# Step 1 — Inspect before changing anything

Read the complete repository first.

At minimum inspect:

* `README.md`
* `EngineerOS/AGENTS.md`
* `EngineerOS/platform.yaml`
* `EngineerOS/platform/operating-rules.md`
* `EngineerOS/WORKFLOW.md`
* `EngineerOS/workflows/ticket-development.md`
* all files under `EngineerOS/docs/`
* the commerce-risk workspace configuration and instructions;
* all curated knowledge files;
* the project source manifest;
* ticket template files;
* all DEMO-001 artifacts;
* `Sample-Projects/commerce-risk/`;
* repository validator;
* GitHub Actions workflow;
* `.gitignore`;
* license location and scope.

Also inspect Git history where available for public-release concerns, but do not rewrite history.

Before modifying anything, produce a concise internal gap analysis and use it to guide implementation.

Do not ask me questions unless a genuinely blocking safety issue prevents progress. Make conservative reasonable decisions and document them.

---

# Step 2 — Preserve the core architecture

Keep this architectural separation:

```text
EngineerOS platform
    ↓
workspace context
    ↓
source manifest
    ↓
authoritative synthetic project
    ↓
ticket-local proposed changes
```

The authoritative sample project must remain separate from ticket proposals.

Normal analysis and design must treat `Sample-Projects/commerce-risk` as read-only.

Proposed implementation must remain beneath the applicable ticket:

```text
implementation/proposed/<project-relative-path>
```

Do not weaken the human-control model.

---

# Step 3 — Make Question Mode a first-class feature

The current repository demonstrates ticket development much more strongly than day-to-day codebase investigation.

Add a proper reusable Question Mode.

Create an appropriate reusable prompt/document, preferably:

```text
EngineerOS/prompts/question-mode.md
```

or another clean structure if you determine a better location.

The Question Mode instructions must tell a coding agent to:

1. load the operating rules;
2. load the applicable workspace instructions;
3. resolve authoritative source through `SOURCE-MANIFEST.yaml`;
4. inspect project code before relying on summaries;
5. inspect relevant curated knowledge;
6. use completed-ticket precedent only as supporting evidence;
7. distinguish:

   * Fact
   * Inference
   * Assumption
   * Conflict
   * Unresolved question
8. cite stable repository paths for important conclusions;
9. report missing evidence;
10. remain read-only;
11. not create a ticket unless ticket work is explicitly requested.

Make this generic enough to support future workspaces.

---

# Step 4 — Add a concrete Question Mode demonstration

Create:

```text
EngineerOS/docs/question-mode-demo.md
```

Use only the synthetic commerce-risk project.

Provide several realistic example engineering investigations, such as:

* Where and how are duplicate open alerts prevented?
* How does regional configuration affect rule evaluation?
* What happens when a regional rule configuration is missing?
* Which project areas would likely be affected if a configuration model changed?
* How is rerun behaviour controlled?

For each example show:

```text
Question
Relevant evidence
Finding
Fact / inference / assumption classification
Relevant repository paths
```

Do not invent behaviour not supported by project code.

Where a conclusion is an inference rather than a direct fact, explicitly label it.

This document should demonstrate how EngineerOS helps an engineer investigate an unfamiliar codebase without changing it.

---

# Step 5 — Clarify the EngineerOS mental model

Improve the architecture documentation and README so that a reviewer can immediately understand four concepts:

```text
Platform
    HOW AI-assisted engineering is performed

Workspace
    WHAT project/domain context the agent receives

Project Source
    WHAT the software currently implements

Ticket
    WHAT change is currently being investigated or proposed
```

Add a simple Mermaid diagram where useful.

Make clear that EngineerOS is not merely a ticket template system.

It is a persistent engineering context and workflow layer around project repositories.

---

# Step 6 — Clarify knowledge accumulation

The repository should demonstrate that curated knowledge and previous engineering work improve future investigation and ticket development.

Update documentation to show a lifecycle similar to:

```text
Project code
    +
curated knowledge
    +
previous ticket evidence
    ↓
better engineering context
    ↓
new investigation or ticket
    ↓
new evidence and engineering decisions
    ↓
retained reusable knowledge
```

Do not claim that knowledge automatically updates itself.

Human review remains required.

---

# Step 7 — Slightly strengthen the commerce-risk knowledge base

Keep it compact.

Do NOT create dozens of artificial files.

Review the current knowledge set and add only high-value missing documents if useful.

Potential additions include:

```text
operations-guide.md
common-investigations.md
known-behaviours.md
engineering-decisions.md
```

Only add files that contain meaningful synthetic engineering context.

Avoid duplicated documentation.

The purpose is to demonstrate useful persistent engineering knowledge, not file count.

---

# Step 8 — Add architecture decisions

Create:

```text
EngineerOS/docs/architecture-decisions.md
```

Document the important design decisions behind EngineerOS.

At minimum include decisions covering:

1. project source is authoritative for implemented behaviour;
2. workspace knowledge is secondary and may become stale;
3. project source is read-only by default;
4. proposed implementation remains ticket-local;
5. design approval precedes proposed development;
6. generated validation is not executed evidence;
7. humans retain control of transfer, source control and release;
8. sample projects must remain synthetic and locally runnable;
9. multiple future workspaces/projects should be supported without changing the platform model.

Keep ADRs concise and engineering-focused.

---

# Step 9 — Separate reusable workflow instructions from demo construction history

Review `EngineerOS/WORKFLOW.md`.

Currently it mixes reusable ticket operation with prompts that appear to describe creation of the demo itself and DEMO-001.

Refactor this cleanly.

The primary workflow documentation should focus on how someone USES EngineerOS:

```text
Question Mode

Ticket Mode:
1. Intake / understanding
2. Design
3. Proposed development
4. Generated validation
5. Independent review
6. Manual transfer / execution / rollback guidance
```

Preserve useful historical/demo prompts only if they add portfolio value.

If retained, move them to an appropriately named document such as:

```text
EngineerOS/docs/demo-build-history.md
```

or:

```text
EngineerOS/docs/demo-reproduction.md
```

Do not let repository-construction instructions obscure the reusable engineering workflow.

---

# Step 10 — Clarify ticket completion semantics

DEMO-001 currently lives under:

```text
tickets/completed/
```

while its implementation remains:

```text
not_transferred
```

and generated feature validation remains:

```text
Not Run
```

This is potentially confusing.

Do not automatically rename the directory structure unless necessary.

Instead establish clear lifecycle semantics.

For example, document that:

> `completed` means the EngineerOS analysis/design/proposal/review/handoff workflow has completed. It does not imply that the proposed project change was transferred, executed, tested in its destination, committed, deployed or released.

Make this distinction visible in:

* ticket workflow documentation;
* README;
* DEMO-001 walkthrough where relevant.

If you identify a cleaner low-complexity lifecycle model, you may implement it, but avoid unnecessary state-machine complexity.

---

# Step 11 — Add reproducible isolated proposal validation

The baseline sample project is easy to run, but validating the DEMO-001 proposal currently requires manually assembling a temporary tree.

Create a lightweight script such as:

```text
EngineerOS/scripts/validate_ticket_proposal.py
```

It should support DEMO-001 and ideally use a structure that could later support other tickets.

The script must:

1. identify the ticket and its `change-manifest.yaml`;
2. create a temporary project directory;
3. copy the authoritative synthetic sample project into the temporary directory;
4. overlay proposed files according to the manifest;
5. copy appropriate generated tests into the temporary project;
6. run the project's tests in the temporary tree;
7. report the exact result;
8. confirm that authoritative project files were not modified;
9. clean up temporary files where practical.

It must NEVER overwrite:

```text
Sample-Projects/commerce-risk
```

The output must clearly distinguish:

```text
isolated temporary validation
```

from:

```text
manual transfer
deployment
shared-environment validation
production evidence
```

A successful isolated run may be recorded as executed isolated validation, but must never imply transfer or deployment.

Use Python standard-library functionality where practical.

---

# Step 12 — Make the proposal validation easy to demonstrate

Document a command similar to:

```bash
python EngineerOS/scripts/validate_ticket_proposal.py DEMO-001
```

The command should be suitable for a reviewer cloning the repository.

Expected presentation should make clear:

```text
Authoritative project modified: No
Temporary proposal assembled: Yes
Baseline tests: <actual result>
DEMO-001 tests: <actual result>
Validation type: isolated temporary validation
Transfer state: not_transferred
```

Do not hard-code false results.

Output must reflect actual execution.

---

# Step 13 — Fix the public-release audit model

Review:

```text
EngineerOS/docs/public-release-audit.md
```

It currently mixes repository publication safety with DEMO-001 deployment/runtime evidence.

Separate these concepts.

A public repository does NOT need DEMO-001 to be transferred or deployed in order to be publishable.

In fact:

```text
not_transferred
Not Run
```

may be intentional evidence of the human-control boundary.

The public-release audit should primarily assess:

* confidential/proprietary content;
* personal data;
* emails;
* URLs;
* secrets;
* credential shapes;
* prohibited binary files;
* broken links;
* unexpected archives;
* nested Git repositories;
* licensing;
* repository validation;
* local reproducibility;
* GitHub Actions configuration;
* clean-room provenance;
* intentional public identity information.

Treat intentional DEMO-001 non-transfer as a demo state rather than automatically as a publication blocker.

Do not falsely mark DEMO-001 feature tests as executed unless they actually are.

If you run the new isolated proposal validator, clearly record that execution as isolated temporary validation only.

---

# Step 14 — Resolve license scope

The repository currently has a license under `EngineerOS/`.

Review whether the intended license should cover the full repository.

Unless there is a compelling reason otherwise, move or create the appropriate MIT license at:

```text
/LICENSE
```

so the scope clearly includes both:

```text
EngineerOS/
Sample-Projects/
```

Update README links accordingly.

Do not create conflicting licenses.

Preserve the existing copyright holder if present.

Do not invent additional authors.

---

# Step 15 — Strengthen clean-room provenance documentation

Add a concise, credible clean-room explanation to the root README or a linked document.

Explain that EngineerOS reproduces general engineering workflow ideas rather than a real company's architecture.

Explicitly state that the repository does not contain:

* copied workplace source code;
* renamed proprietary schemas;
* workplace documents;
* screenshots;
* production architecture diagrams;
* real business thresholds;
* real tickets;
* real environment configuration;
* customer or employee data;
* credentials;
* lightly renamed proprietary material.

Make clear that the commerce-risk sample was independently designed as a fictional system.

Do not overclaim that automated scanning can prove provenance.

---

# Step 16 — Make automated safety claims accurate

Review `EngineerOS/scripts/validate_repository.py` and documentation describing it.

The validator may check concrete detectable patterns such as:

* email addresses;
* private/local URLs;
* credential shapes;
* prohibited file types;
* nested `.git` directories;
* broken repository-local Markdown links;
* common confidentiality phrases;
* required repository structures;
* change manifest consistency;
* proposal isolation.

Do not imply that a keyword scanner proves the absence of proprietary material.

Documentation should state that automated validation supplements but does not replace human clean-room review.

Improve the validator where useful but keep it maintainable and standard-library based where practical.

---

# Step 17 — Preserve the synthetic technical abstraction

Do NOT make `commerce-risk` more similar to any real financial-crime or casino platform.

Keep the current generic design concepts:

```text
customers
orders
payments
risk rules
regional configuration
monitoring runs
alerts
```

Do not add real-world employer technology purely for similarity.

Avoid unnecessary Azure, ADF, Synapse, ServiceNow, casino, gaming or AML-specific architecture.

The portfolio should reproduce the ENGINEERING OPERATING MODEL, not a proprietary technical topology.

---

# Step 18 — Improve reviewer onboarding

Update the root README so a reviewer has three clear routes.

## 2-minute overview

Understand:

* what EngineerOS is;
* platform/workspace/project/ticket separation;
* human-control philosophy.

## 5-minute interactive demo

Run:

```bash
python EngineerOS/scripts/validate_repository.py
python Sample-Projects/commerce-risk/run_pipeline.py ...
```

and optionally the isolated DEMO-001 validator.

## 15-minute engineering walkthrough

Inspect:

* operating rules;
* Question Mode;
* sample code;
* requirement;
* task understanding;
* human decision;
* design;
* ticket-local proposal;
* validation matrix;
* review;
* evidence;
* transfer/rollback guidance.

Keep the root README scannable.

Move deep explanation into linked docs.

---

# Step 19 — Add "Try it with Codex" examples

Add concise ready-to-paste prompts to the README or a linked usage guide.

Include at least:

## Example A — Question Mode

Something equivalent to:

```text
Read EngineerOS/AGENTS.md and investigate the commerce-risk workspace.

Explain how duplicate open alerts are prevented.

Use authoritative project code as the primary source.
Inspect relevant curated knowledge only as supporting context.
Distinguish facts from inferences.
Cite repository paths for important conclusions.
Do not modify any files.
```

## Example B — New Ticket

Provide a generic prompt that starts Stage 1 using a fictional requirement.

Do not make the examples dependent on private tools or services.

---

# Step 20 — Ensure workspace extensibility is visible

EngineerOS should continue to have only one fully implemented workspace unless another workspace genuinely adds value.

Do NOT create a second large sample project just to prove extensibility.

Instead make the generic structure clear:

```text
EngineerOS/workspaces/<workspace>/
Sample-Projects/<project>/
```

and ensure platform/workflow documentation does not unnecessarily hard-code commerce-risk where generic behaviour is intended.

Workspace-specific rules should remain inside the commerce-risk workspace.

---

# Step 21 — Improve consistency

Audit for contradictions across:

* README;
* platform.yaml;
* operating rules;
* AGENTS.md;
* WORKFLOW.md;
* ticket workflow;
* architecture docs;
* portfolio walkthrough;
* DEMO-001 evidence;
* review;
* public-release audit;
* validator;
* GitHub Actions.

Examples of things to resolve:

* terminology drift;
* inconsistent stage names;
* ambiguity about what `completed` means;
* conflicting statements about who may execute local validation;
* claims that are stronger than evidence;
* stale paths;
* inconsistent source-authority ordering.

Use one canonical vocabulary across the repository.

---

# Step 22 — Keep the repository compact

Do not over-engineer this.

Avoid:

* agent orchestration frameworks;
* external databases;
* cloud infrastructure;
* containers unless clearly necessary;
* package dependencies where standard library is sufficient;
* autonomous deployment;
* complex schema frameworks;
* unnecessary abstractions;
* fake enterprise architecture;
* dozens of placeholder knowledge files.

EngineerOS should remain understandable by an engineer in approximately 15 minutes.

---

# Step 23 — Validate everything

After modifications, run all applicable checks.

At minimum:

```bash
python EngineerOS/scripts/validate_repository.py
```

Run baseline project tests:

```bash
cd Sample-Projects/commerce-risk
python -m unittest discover -s tests -v
```

Run the new isolated DEMO-001 validation command.

Run relevant syntax checks.

Check Markdown links.

Check:

```bash
git diff --check
```

where Git metadata is available.

Confirm that the authoritative sample project was not unintentionally changed by the isolated validation process.

If `gitleaks` or another external secret scanner is installed, run it.

If it is unavailable, state that truthfully rather than treating it as executed evidence.

---

# Step 24 — Perform a final public-safety review

Search the complete current worktree for:

* employer/client names;
* workplace terminology;
* real ticket numbers;
* personal/workplace emails;
* internal/private URLs;
* credentials;
* connection strings;
* tokens;
* private keys;
* unexpected archives;
* Office files;
* PDFs;
* screenshots;
* document metadata;
* absolute machine-specific paths;
* proprietary source fragments;
* copied or lightly renamed workplace material.

Do not rely solely on automated scanning.

If anything looks potentially derived from a real workplace system, replace it with a newly designed synthetic equivalent or remove it.

Do not expose the potentially sensitive material in your final response.

---

# Step 25 — Final result

When finished, give me:

1. a concise summary of what you changed;
2. the important architectural improvements;
3. files added;
4. files materially modified;
5. tests/checks actually executed;
6. actual results;
7. any remaining limitations;
8. whether you consider the current tree technically ready for a human final public-release review.

Do not claim it is approved for publication on my behalf.

Do not commit, push, rewrite Git history, open a pull request or perform any release action.

Leave those actions to me.
