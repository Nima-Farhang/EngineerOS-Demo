from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from risk_pipeline import DEFAULT_MONITORING_TIME, connect, evaluate_rules, run_pipeline


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database = Path(self.temporary_directory.name) / "test.db"
        run_pipeline(self.database, DEFAULT_MONITORING_TIME)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_seed_data_creates_expected_alerts(self) -> None:
        with connect(self.database) as connection:
            rows = connection.execute(
                """SELECT c.display_name, r.rule_code FROM alerts AS a
                   JOIN customers AS c ON c.customer_id = a.customer_id
                   JOIN risk_rules AS r ON r.rule_id = a.rule_id
                   ORDER BY r.rule_code"""
            ).fetchall()
        self.assertEqual(
            [(row["display_name"], row["rule_code"]) for row in rows],
            [("Cedar Finch", "RISK_DECLINED_PAYMENTS"),
             ("Amber Otter", "RISK_HIGH_VALUE_ORDER")],
        )

    def test_rerun_does_not_duplicate_open_alerts(self) -> None:
        with connect(self.database) as connection:
            created = evaluate_rules(connection, DEFAULT_MONITORING_TIME)
            count = connection.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
        self.assertEqual(created, 0)
        self.assertEqual(count, 2)

    def test_regional_threshold_is_configurable(self) -> None:
        with connect(self.database) as connection:
            connection.execute(
                """UPDATE regional_rule_config SET amount_threshold = 650
                   WHERE region = 'EAST' AND rule_id = (
                     SELECT rule_id FROM risk_rules WHERE rule_code = 'RISK_HIGH_VALUE_ORDER')"""
            )
            created = evaluate_rules(connection, DEFAULT_MONITORING_TIME)
            count = connection.execute(
                """SELECT COUNT(*) FROM alerts AS a JOIN customers AS c USING (customer_id)
                   WHERE c.region = 'EAST'"""
            ).fetchone()[0]
        self.assertEqual(created, 1)
        self.assertEqual(count, 1)

    def test_cancelled_high_value_order_is_not_eligible(self) -> None:
        with connect(self.database) as connection:
            count = connection.execute(
                """SELECT COUNT(*) FROM alerts AS a JOIN customers AS c USING (customer_id)
                   WHERE c.region = 'WEST'"""
            ).fetchone()[0]
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
