"""Validation for DEMO-001 after approved proposed files are transferred."""
from __future__ import annotations

import tempfile
import subprocess
import sys
import unittest
from pathlib import Path

from risk_pipeline import DEFAULT_MONITORING_TIME, build_database, connect, evaluate_rules


RULE_CODE = "RISK_REPEAT_HIGH_VALUE_ORDERS"


class RepeatHighValueOrdersTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database = Path(self.temporary_directory.name) / "test.db"
        build_database(self.database)
        self.connection = connect(self.database)

    def tearDown(self) -> None:
        self.connection.close()
        self.temporary_directory.cleanup()

    def configure(
        self,
        region: str,
        *,
        window_hours: int,
        count_threshold: int,
        amount_threshold: float,
    ) -> None:
        self.connection.execute(
            """
            UPDATE regional_rule_config
            SET window_hours = ?, event_count_threshold = ?, amount_threshold = ?
            WHERE region = ?
              AND rule_id = (SELECT rule_id FROM risk_rules WHERE rule_code = ?)
            """,
            (window_hours, count_threshold, amount_threshold, region, RULE_CODE),
        )

    def add_order(
        self,
        order_id: int,
        customer_id: int,
        status: str,
        amount: float,
        ordered_at: str,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO orders
                (order_id, customer_id, order_status, order_amount, ordered_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (order_id, customer_id, status, amount, ordered_at),
        )

    def repeat_alerts(self, customer_id: int | None = None):
        sql = """
            SELECT a.customer_id, a.monitoring_date,
                   a.qualifying_event_count, a.qualifying_amount
            FROM alerts AS a
            JOIN risk_rules AS r ON r.rule_id = a.rule_id
            WHERE r.rule_code = ? AND a.status = 'OPEN'
        """
        parameters: list[object] = [RULE_CODE]
        if customer_id is not None:
            sql += " AND a.customer_id = ?"
            parameters.append(customer_id)
        return self.connection.execute(sql, parameters).fetchall()

    def add_three_qualifying_north_orders(self) -> None:
        self.configure(
            "NORTH", window_hours=48, count_threshold=3, amount_threshold=600
        )
        self.add_order(201, 1, "COMPLETED", 600, "2026-01-14T10:00:00Z")
        self.add_order(202, 1, "COMPLETED", 650, "2026-01-14T11:00:00Z")
        self.add_order(203, 1, "COMPLETED", 700, "2026-01-15T12:00:00Z")

    def test_rule_code_configuration_and_independent_disablement(self) -> None:
        definition = self.connection.execute(
            "SELECT enabled FROM risk_rules WHERE rule_code = ?", (RULE_CODE,)
        ).fetchone()
        regions = self.connection.execute(
            """
            SELECT region, window_hours, event_count_threshold, amount_threshold
            FROM regional_rule_config
            WHERE rule_id = (SELECT rule_id FROM risk_rules WHERE rule_code = ?)
            ORDER BY region
            """,
            (RULE_CODE,),
        ).fetchall()
        self.assertIsNotNone(definition)
        self.assertEqual(len(regions), 4)
        self.assertTrue(
            all(
                row["window_hours"] is not None
                and row["event_count_threshold"] is not None
                and row["amount_threshold"] is not None
                for row in regions
            )
        )

        self.add_three_qualifying_north_orders()
        self.connection.execute(
            "UPDATE risk_rules SET enabled = 0 WHERE rule_code = ?", (RULE_CODE,)
        )
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        self.assertEqual(self.repeat_alerts(1), [])

    def test_qualifying_orders_store_exact_count_and_total(self) -> None:
        self.add_three_qualifying_north_orders()
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        alerts = self.repeat_alerts(1)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["qualifying_event_count"], 3)
        self.assertEqual(alerts[0]["qualifying_amount"], 1950)

    def test_below_count_does_not_alert(self) -> None:
        self.configure(
            "NORTH", window_hours=48, count_threshold=3, amount_threshold=600
        )
        self.add_order(211, 1, "COMPLETED", 700, "2026-01-14T10:00:00Z")
        self.add_order(212, 1, "COMPLETED", 800, "2026-01-14T11:00:00Z")
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        self.assertEqual(self.repeat_alerts(1), [])

    def test_below_amount_orders_do_not_count_or_contribute_to_total(self) -> None:
        self.configure(
            "NORTH", window_hours=48, count_threshold=2, amount_threshold=600
        )
        self.add_order(221, 1, "COMPLETED", 599, "2026-01-14T09:00:00Z")
        self.add_order(222, 1, "COMPLETED", 600, "2026-01-14T10:00:00Z")
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        self.assertEqual(self.repeat_alerts(1), [])

    def test_window_is_lower_exclusive_and_upper_inclusive(self) -> None:
        self.configure(
            "NORTH", window_hours=48, count_threshold=2, amount_threshold=600
        )
        self.add_order(231, 1, "COMPLETED", 900, "2026-01-13T12:00:00Z")
        self.add_order(232, 1, "COMPLETED", 600, "2026-01-13T12:00:01Z")
        self.add_order(233, 1, "COMPLETED", 700, "2026-01-15T12:00:00Z")
        self.add_order(234, 1, "COMPLETED", 1000, "2026-01-15T12:00:01Z")
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        alerts = self.repeat_alerts(1)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["qualifying_event_count"], 2)
        self.assertEqual(alerts[0]["qualifying_amount"], 1300)

    def test_pending_and_cancelled_orders_are_excluded(self) -> None:
        self.configure(
            "NORTH", window_hours=48, count_threshold=2, amount_threshold=600
        )
        self.add_order(241, 1, "COMPLETED", 600, "2026-01-14T09:00:00Z")
        self.add_order(242, 1, "CANCELLED", 800, "2026-01-14T10:00:00Z")
        self.add_order(243, 1, "PENDING", 900, "2026-01-14T11:00:00Z")
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        self.assertEqual(self.repeat_alerts(1), [])

    def test_regional_configuration_is_isolated(self) -> None:
        self.configure(
            "NORTH", window_hours=48, count_threshold=2, amount_threshold=600
        )
        self.configure(
            "EAST", window_hours=48, count_threshold=2, amount_threshold=800
        )
        self.add_order(251, 1, "COMPLETED", 650, "2026-01-14T09:00:00Z")
        self.add_order(252, 1, "COMPLETED", 700, "2026-01-14T10:00:00Z")
        self.add_order(253, 3, "COMPLETED", 650, "2026-01-14T09:00:00Z")
        self.add_order(254, 3, "COMPLETED", 700, "2026-01-14T10:00:00Z")
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        self.assertEqual(len(self.repeat_alerts(1)), 1)
        self.assertEqual(self.repeat_alerts(3), [])

    def test_same_date_rerun_does_not_duplicate_open_alert(self) -> None:
        self.add_three_qualifying_north_orders()
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        alerts = self.repeat_alerts(1)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["monitoring_date"], "2026-01-15")

    def test_different_monitoring_date_can_create_a_distinct_open_alert(self) -> None:
        self.configure(
            "NORTH", window_hours=72, count_threshold=3, amount_threshold=600
        )
        self.add_order(261, 1, "COMPLETED", 600, "2026-01-14T10:00:00Z")
        self.add_order(262, 1, "COMPLETED", 650, "2026-01-14T11:00:00Z")
        self.add_order(263, 1, "COMPLETED", 700, "2026-01-15T12:00:00Z")
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        evaluate_rules(self.connection, "2026-01-16T12:00:00Z")
        dates = [row["monitoring_date"] for row in self.repeat_alerts(1)]
        self.assertEqual(sorted(dates), ["2026-01-15", "2026-01-16"])

    def test_build_and_cli_are_compatible_at_an_isolated_path(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        database = Path(self.temporary_directory.name) / "cli.db"
        result = subprocess.run(
            [
                sys.executable,
                str(project_root / "run_pipeline.py"),
                "--database",
                str(database),
                "--monitoring-time",
                DEFAULT_MONITORING_TIME,
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(database.is_file())
        self.assertIn("Alerts created:", result.stdout)
        with connect(database) as connection:
            rule = connection.execute(
                "SELECT rule_code FROM risk_rules WHERE rule_code = ?", (RULE_CODE,)
            ).fetchone()
        self.assertIsNotNone(rule)

    def test_existing_rule_results_are_preserved(self) -> None:
        evaluate_rules(self.connection, DEFAULT_MONITORING_TIME)
        rows = self.connection.execute(
            """
            SELECT c.display_name, r.rule_code
            FROM alerts AS a
            JOIN customers AS c ON c.customer_id = a.customer_id
            JOIN risk_rules AS r ON r.rule_id = a.rule_id
            WHERE r.rule_code IN ('RISK_DECLINED_PAYMENTS', 'RISK_HIGH_VALUE_ORDER')
            ORDER BY r.rule_code
            """
        ).fetchall()
        self.assertEqual(
            [(row["display_name"], row["rule_code"]) for row in rows],
            [
                ("Cedar Finch", "RISK_DECLINED_PAYMENTS"),
                ("Amber Otter", "RISK_HIGH_VALUE_ORDER"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
