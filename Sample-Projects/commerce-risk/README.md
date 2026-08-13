# Synthetic Commerce Risk Sample Project

This compact, fictional project demonstrates a deterministic commerce-risk
pipeline using only Python's standard library and SQLite.

## Architecture

`sql/schema.sql` defines seven tables and two curated views. `sql/seed.sql`
loads synthetic customers, orders, payments, rules, and regional configuration.
`risk_pipeline.py` rebuilds a database and evaluates the configured rules.

The pipeline rebuilds the database, loads deterministic seed data, evaluates
enabled rules at a supplied monitoring time, and writes open alerts. Duplicate
alerts for the same customer, rule, and monitoring date are suppressed.

## Data grain

| Object | Grain |
|---|---|
| `customers` | One row per synthetic customer |
| `orders` | One row per order |
| `payments` | One row per payment attempt |
| `risk_rules` | One row per rule definition |
| `regional_rule_config` | One row per rule and region |
| `monitoring_runs` | One row per pipeline run |
| `alerts` | One detected customer/rule/date while open |

The curated views provide one row per payment attempt with customer context and
one row per completed order with customer context.

## Run locally

From this directory:

```bash
python run_pipeline.py
```

This creates `build/commerce_risk.db` and prints a summary. An alternate path
and deterministic monitoring time can be supplied:

```bash
python run_pipeline.py --database /tmp/commerce-risk.db \
  --monitoring-time 2026-01-15T12:00:00Z
```

Run the baseline tests manually with:

```bash
python -m unittest discover -s tests -v
```

## Baseline rules

- `RISK_DECLINED_PAYMENTS`: alerts when a customer has at least the configured
  number of declined attempts inside the configured window.
- `RISK_HIGH_VALUE_ORDER`: alerts for a completed order at or above its
  regional configured amount.

Both rules use regional configuration. A partial unique index prevents more
than one open alert for the same customer, rule, and monitoring date.

## Limits

This is a local teaching example, not a production monitoring system. It uses
small batch inputs, SQLite timestamps, and a single-process runner. It has no
external services, authentication, user interface, streaming ingestion, or
production operational controls. All identities, data, dates, and thresholds
are synthetic.
