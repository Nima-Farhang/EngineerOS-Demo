"""Build and evaluate the synthetic SQLite commerce-risk project."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MONITORING_TIME = "2026-01-15T12:00:00Z"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(database: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def build_database(database: str | Path) -> None:
    database_path = Path(database)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    if database_path.exists():
        database_path.unlink()
    with connect(database_path) as connection:
        connection.executescript((PROJECT_ROOT / "sql/schema.sql").read_text())
        connection.executescript((PROJECT_ROOT / "sql/seed.sql").read_text())


def evaluate_rules(connection: sqlite3.Connection, monitoring_time: str) -> int:
    monitoring_date = monitoring_time[:10]
    created_at = _utc_now()
    before = connection.total_changes
    connection.execute(
        """
        INSERT OR IGNORE INTO alerts
            (customer_id, rule_id, monitoring_date, status,
             qualifying_event_count, qualifying_amount, created_at)
        SELECT activity.customer_id, rule.rule_id, ?, 'OPEN',
               COUNT(*), SUM(activity.attempted_amount), ?
        FROM v_customer_payment_activity AS activity
        JOIN risk_rules AS rule
          ON rule.rule_code = 'RISK_DECLINED_PAYMENTS' AND rule.enabled = 1
        JOIN regional_rule_config AS config
          ON config.rule_id = rule.rule_id AND config.region = activity.region
        WHERE activity.payment_status = 'DECLINED'
          AND datetime(activity.attempted_at) > datetime(?, '-' || config.window_hours || ' hours')
          AND datetime(activity.attempted_at) <= datetime(?)
        GROUP BY activity.customer_id, rule.rule_id, config.event_count_threshold
        HAVING COUNT(*) >= config.event_count_threshold
        """,
        (monitoring_date, created_at, monitoring_time, monitoring_time),
    )
    connection.execute(
        """
        INSERT OR IGNORE INTO alerts
            (customer_id, rule_id, monitoring_date, status,
             qualifying_event_count, qualifying_amount, created_at)
        SELECT activity.customer_id, rule.rule_id, ?, 'OPEN',
               COUNT(*), SUM(activity.order_amount), ?
        FROM v_completed_order_activity AS activity
        JOIN risk_rules AS rule
          ON rule.rule_code = 'RISK_HIGH_VALUE_ORDER' AND rule.enabled = 1
        JOIN regional_rule_config AS config
          ON config.rule_id = rule.rule_id AND config.region = activity.region
        WHERE activity.order_amount >= config.amount_threshold
          AND datetime(activity.ordered_at) <= datetime(?)
        GROUP BY activity.customer_id, rule.rule_id
        """,
        (monitoring_date, created_at, monitoring_time),
    )
    connection.execute(
        """
        INSERT OR IGNORE INTO alerts
            (customer_id, rule_id, monitoring_date, status,
             qualifying_event_count, qualifying_amount, created_at)
        SELECT activity.customer_id, rule.rule_id, ?, 'OPEN',
               COUNT(*), SUM(activity.order_amount), ?
        FROM v_completed_order_activity AS activity
        JOIN risk_rules AS rule
          ON rule.rule_code = 'RISK_REPEAT_HIGH_VALUE_ORDERS' AND rule.enabled = 1
        JOIN regional_rule_config AS config
          ON config.rule_id = rule.rule_id AND config.region = activity.region
        WHERE activity.order_amount >= config.amount_threshold
          AND datetime(activity.ordered_at) > datetime(?, '-' || config.window_hours || ' hours')
          AND datetime(activity.ordered_at) <= datetime(?)
        GROUP BY activity.customer_id, rule.rule_id,
                 config.event_count_threshold
        HAVING COUNT(*) >= config.event_count_threshold
        """,
        (monitoring_date, created_at, monitoring_time, monitoring_time),
    )
    return connection.total_changes - before


def run_pipeline(database: str | Path, monitoring_time: str = DEFAULT_MONITORING_TIME) -> dict[str, int]:
    build_database(database)
    with connect(database) as connection:
        cursor = connection.execute(
            "INSERT INTO monitoring_runs (monitoring_time, started_at, status) VALUES (?, ?, 'RUNNING')",
            (monitoring_time, _utc_now()),
        )
        created = evaluate_rules(connection, monitoring_time)
        connection.execute(
            "UPDATE monitoring_runs SET completed_at = ?, status = 'COMPLETED' WHERE run_id = ?",
            (_utc_now(), cursor.lastrowid),
        )
        total = connection.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    return {"alerts_created": created, "alerts_total": total}
