# Question Mode

Use this mode when the user asks a question about a project, requests an
investigation, or wants current-state explanation without asking for a change.

## Procedure

1. Read `EngineerOS/platform/operating-rules.md`.
2. Identify and read the applicable
   `EngineerOS/workspaces/<workspace>/instructions.md`.
3. Resolve authoritative source through that workspace's
   `project-code/SOURCE-MANIFEST.yaml`.
4. Inspect relevant project code before relying on summaries or precedent.
5. Inspect only the curated knowledge relevant to the question. Treat it as
   secondary to project source.
6. Use completed tickets only as supporting evidence or precedent. They do not
   override current code or approved requirements.
7. Classify material conclusions consistently:
   - **Fact:** directly supported by a cited source.
   - **Inference:** reasoned from cited facts.
   - **Assumption:** an unverified premise needed to proceed.
   - **Conflict:** material sources disagree.
   - **Unresolved question:** required evidence is missing.
8. Cite stable repository-root-relative paths for important conclusions.
9. State missing evidence and explain how it limits confidence.
10. Remain read-only. Do not edit project, workspace, knowledge, or ticket files.
11. Do not create a ticket unless the user explicitly requests ticket work.

## Response shape

Use the smallest structure that makes the evidence clear:

```text
Answer
Facts and paths
Inferences or assumptions
Conflicts or unresolved questions
```

Omit empty sections. Do not imply test execution, transfer, deployment, or
production behavior without recorded executed evidence.
