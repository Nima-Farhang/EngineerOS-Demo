# DEMO-001 Validation Matrix

Generated validation status: **Not Run**.

Test references point to `test_repeat_high_value_orders.py` in this directory.

| Acceptance criterion | Test coverage | Expected result |
|---|---|---|
| Exact rule code and independent enablement | `test_rule_code_configuration_and_independent_disablement` | Definition exists with four complete regional rows; disabled rule creates no repeat-order alert |
| Current completed orders only | `test_pending_and_cancelled_orders_are_excluded` | Pending and currently cancelled orders do not contribute |
| Configurable rolling hours | `test_window_is_lower_exclusive_and_upper_inclusive` | Only rows in the configured interval contribute |
| Regional count and amount configuration | `test_regional_configuration_is_isolated` | NORTH qualifies under NORTH values; EAST does not borrow them |
| Per-order amount is inclusive | `test_qualifying_orders_store_exact_count_and_total`, `test_below_amount_orders_do_not_count_or_contribute_to_total` | An order equal to the threshold counts; one below it does not |
| Customer count is inclusive | `test_qualifying_orders_store_exact_count_and_total`, `test_below_count_does_not_alert` | Count equal to threshold qualifies; lower count does not |
| Store count and total amount | `test_qualifying_orders_store_exact_count_and_total` | Alert stores count `3` and total `1950` |
| Suppress same-date duplicate open alerts | `test_same_date_rerun_does_not_duplicate_open_alert` | Two evaluations leave one open repeat-rule alert |
| Permit distinct monitoring-date alert identity | `test_different_monitoring_date_can_create_a_distinct_open_alert` | Qualifying evaluations on two dates create one open alert for each date |
| Below count, below amount, and outside window do not alert | `test_below_count_does_not_alert`, `test_below_amount_orders_do_not_count_or_contribute_to_total`, `test_window_is_lower_exclusive_and_upper_inclusive` | Non-qualifying rows do not create or inflate an alert |
| Regional isolation | `test_regional_configuration_is_isolated` | Each customer uses only configuration for their own region |
| Preserve existing rules | `test_existing_rule_results_are_preserved` | Baseline declined-payment and high-value-order customer/rule pairs remain unchanged |

## Required scenario coverage

| Scenario type | Coverage |
|---|---|
| Positive | Exact count, exact amount, stored total |
| Negative | Disabled, below count, below amount, pending, cancelled |
| Boundary | Lower time excluded; upper time included; exact amount/count included |
| Rerun | Same-date open-alert suppression |
| Regional | Different NORTH and EAST amount thresholds |
| Cancelled-order decision | Current `CANCELLED` status excluded |
| Compatibility | Both existing rule results retained |
| Build/CLI compatibility | CLI builds and evaluates an isolated temporary database |

The build/CLI case is covered by
`test_build_and_cli_are_compatible_at_an_isolated_path`.

## Execution evidence

No test outcome is recorded here. A human must execute the validation and add
the command, environment, date/time, complete result, and executor to
`../evidence.md` before any test is described as passed.
