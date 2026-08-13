# Operating Rules

## 1. Source authority

Use the most authoritative available evidence for each claim:

1. Project code describes the current implementation.
2. Approved ticket requirements describe the intended change.
3. Official project documentation describes approved design and behaviour.
4. Curated workspace knowledge provides maintained context.
5. Completed demo tickets provide precedent, not mandatory rules.
6. Generated reference material supports discovery only.
7. General knowledge may fill non-project-specific gaps.

When sources conflict, report the conflict. Do not silently reconcile it.
Cite stable repository paths for material conclusions.

## 2. Evidence language

Use these labels consistently:

- **Fact:** directly supported by an identified source.
- **Inference:** a reasoned conclusion from identified facts.
- **Assumption:** an unverified premise used to progress.
- **Unresolved question:** information still required.
- **Conflict:** material sources disagree.
- **Executed evidence:** a recorded result from an action actually performed.

Generated code, expected results, static inspection, and test scripts are not
executed evidence.

## 3. Human control

A human must confirm requirements, approve the design, decide whether proposed
changes are applied, execute tests, confirm results, and approve source-control
or release actions. An agent must not infer approval from silence.

## 4. Safety and confidentiality

This is a synthetic public portfolio project. Do not import proprietary source
material, workplace documents, personal data, real credentials, or internal
infrastructure details. Use fictional examples and synthetic data only.

## 5. Change isolation

The sample project is read-only during analysis and design. During development,
create proposed files beneath:

`<ticket>/implementation/proposed/<project-relative-path>`

Maintain a change manifest that maps each proposed file to its intended project
destination.

## 6. Honest validation

Record generated tests as `Not Run` until a human executes them. Never state
that a test passed or a release succeeded without recorded executed evidence.
