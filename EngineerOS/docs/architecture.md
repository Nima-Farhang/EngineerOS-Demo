# Architecture

The repository separates four concerns:

1. **Platform governance** — global evidence, safety, and approval rules under
   `EngineerOS/platform/` and `EngineerOS/workflows/`.
2. **Workspace context** — fictional domain-specific instructions and knowledge
   under `EngineerOS/workspaces/<workspace>/`.
3. **Sample projects** — runnable synthetic source code under
   `Sample-Projects/<project>/`, alongside rather than inside EngineerOS.
4. **Ticket workspaces** — isolated analysis, design, proposed changes, tests,
   review, and release guidance under
   `EngineerOS/workspaces/<workspace>/tickets/`.

All paths in EngineerOS documentation are relative to the repository root
unless a command explicitly says to change directory first.

Each workspace's `project-code/SOURCE-MANIFEST.yaml` points to its authoritative
project directory. Proposed files remain inside a ticket until a human chooses
to transfer them to that project. This makes the workflow reviewable and
prevents an agent from silently changing authoritative source during analysis.
