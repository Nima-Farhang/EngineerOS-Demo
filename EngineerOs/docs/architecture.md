# Architecture

The repository separates four concerns:

1. **Platform governance** — global evidence, safety, and approval rules.
2. **Workspace context** — fictional domain-specific instructions and knowledge.
3. **Sample project** — synthetic source code used as current-state evidence.
4. **Ticket workspaces** — isolated analysis, design, proposed changes, tests,
   review, and release guidance.

Proposed files remain inside a ticket until a human chooses to transfer them to
the sample project. This makes the workflow reviewable and prevents an agent
from silently changing authoritative source during analysis.
