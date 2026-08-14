# Common Investigations

Use these routes for discovery, then confirm in authoritative source.

| Investigation | Confirm in `Sample-Projects/commerce-risk/` |
|---|---|
| Duplicate open alert | `sql/schema.sql` partial index; evaluator inserts |
| Missing regional result | `risk_pipeline.py`; `sql/seed.sql` |
| Unexpected completed-order alert | Completed-order view; evaluator filter |
| Unexpected declined count | Declined evaluator time/status filters |
| Prior local data disappeared | `build_database` and `run_pipeline` lifecycle |
| Configuration-model impact | Schema, seed, evaluator, tests, then knowledge |

**Fact:** these paths describe current behavior. **Inference:** an impact route
is not guaranteed until a requirement is known. Use Question Mode first; create
a ticket only when a change is explicitly requested.
