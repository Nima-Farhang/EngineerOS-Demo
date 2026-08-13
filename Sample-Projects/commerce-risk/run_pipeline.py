#!/usr/bin/env python3
"""Command-line entry point for the synthetic risk pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path

from risk_pipeline import DEFAULT_MONITORING_TIME, run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database", type=Path,
        default=Path(__file__).resolve().parent / "build/commerce_risk.db",
    )
    parser.add_argument("--monitoring-time", default=DEFAULT_MONITORING_TIME)
    args = parser.parse_args()
    result = run_pipeline(args.database, args.monitoring_time)
    print(f"Database: {args.database}")
    print(f"Alerts created: {result['alerts_created']}")
    print(f"Alerts total: {result['alerts_total']}")


if __name__ == "__main__":
    main()
