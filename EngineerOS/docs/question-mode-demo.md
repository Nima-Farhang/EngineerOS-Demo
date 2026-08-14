# Question Mode Demonstration

This read-only demonstration applies
`EngineerOS/prompts/question-mode.md` to the synthetic commerce-risk project.
Project code is primary evidence; curated knowledge is supporting context.

## Where are duplicate open alerts prevented?

**Question:** Where and how are duplicate open alerts prevented?

**Relevant evidence:**

- `Sample-Projects/commerce-risk/sql/schema.sql` defines a partial unique index
  over customer, rule, and monitoring date where status is `OPEN`.
- `Sample-Projects/commerce-risk/risk_pipeline.py` uses `INSERT OR IGNORE` for
  both current evaluators.

**Finding:** **Fact:** the database constraint is the final duplicate guard;
attempted duplicate inserts are ignored by the evaluator. **Inference:** two
closed alerts with the same identity are structurally possible because the
index applies only to open rows.

## How does regional configuration affect evaluation?

**Question:** How does regional configuration affect rule evaluation?

**Relevant evidence:**

- `Sample-Projects/commerce-risk/sql/schema.sql` gives configuration a
  rule-and-region grain.
- `Sample-Projects/commerce-risk/risk_pipeline.py` joins configuration by rule
  ID and the customer's region.
- `Sample-Projects/commerce-risk/sql/seed.sql` provides values for all four
  fictional regions.

**Finding:** **Fact:** each current evaluator uses only the configuration row
matching its rule and customer region. **Inference:** changing one region's
threshold cannot directly change another region's evaluation unless source data
or configuration keys are also changed.

## What if regional configuration is missing?

**Question:** What happens when a regional rule configuration is missing?

**Relevant evidence:** `Sample-Projects/commerce-risk/risk_pipeline.py` uses an
inner join to `regional_rule_config` and has no missing-configuration error path.

**Finding:** **Fact:** activity without a matching configuration row is absent
from the evaluator query and creates no alert. **Unresolved question:** current
requirements do not say whether a future project should instead fail the run.

## What would a configuration-model change affect?

**Question:** Which areas would likely be affected if the configuration model
changed?

**Relevant evidence:**

- Schema: `Sample-Projects/commerce-risk/sql/schema.sql`
- Seed configuration: `Sample-Projects/commerce-risk/sql/seed.sql`
- Query joins: `Sample-Projects/commerce-risk/risk_pipeline.py`
- Configuration test: `Sample-Projects/commerce-risk/tests/test_pipeline.py`
- Supporting context:
  `EngineerOS/workspaces/commerce-risk/knowledge/data-model.md` and
  `EngineerOS/workspaces/commerce-risk/knowledge/rule-engine.md`

**Finding:** **Inference:** those schema, seed, evaluator, test, and knowledge
areas are likely affected. The exact set is an unresolved question until a
specific requirement defines the new model. Question Mode identifies impact;
it does not propose or apply a change.

## How is rerun behavior controlled?

**Question:** How is rerun behavior controlled?

**Relevant evidence:**

- `Sample-Projects/commerce-risk/risk_pipeline.py` rebuilds the database in a
  full `run_pipeline` call.
- Direct `evaluate_rules` calls reuse current database state and rely on the
  partial unique index plus `INSERT OR IGNORE`.
- `Sample-Projects/commerce-risk/tests/test_pipeline.py` contains a generated
  same-date duplicate-suppression test.

**Finding:** **Fact:** full CLI runs rebuild local state, while repeated direct
evaluation of one database suppresses a second same-date open alert.
**Assumption:** the caller supplies a valid monitoring timestamp because the
current CLI does not validate its format.

## Read-only outcome

No ticket or project modification is needed to answer these questions. If a
user asks to change behavior, switch explicitly to Ticket Mode and begin with
intake and understanding.
