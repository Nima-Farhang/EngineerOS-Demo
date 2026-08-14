INSERT INTO customers (customer_id, display_name, region, created_at) VALUES
    (1, 'Cedar Finch', 'NORTH', '2026-01-01T09:00:00Z'),
    (2, 'Amber Otter', 'SOUTH', '2026-01-02T09:00:00Z'),
    (3, 'Silver Wren', 'EAST', '2026-01-03T09:00:00Z'),
    (4, 'Juniper Fox', 'WEST', '2026-01-04T09:00:00Z');

INSERT INTO orders (order_id, customer_id, order_status, order_amount, ordered_at) VALUES
    (101, 1, 'PENDING', 40.00, '2026-01-15T02:00:00Z'),
    (102, 1, 'PENDING', 55.00, '2026-01-15T04:00:00Z'),
    (103, 1, 'PENDING', 65.00, '2026-01-15T06:00:00Z'),
    (104, 2, 'COMPLETED', 1250.00, '2026-01-15T08:00:00Z'),
    (105, 3, 'COMPLETED', 700.00, '2026-01-15T09:00:00Z'),
    (106, 4, 'CANCELLED', 2100.00, '2026-01-15T10:00:00Z');

INSERT INTO payments (payment_id, order_id, payment_status, attempted_amount, attempted_at) VALUES
    (1001, 101, 'DECLINED', 40.00, '2026-01-15T02:05:00Z'),
    (1002, 102, 'DECLINED', 55.00, '2026-01-15T04:05:00Z'),
    (1003, 103, 'DECLINED', 65.00, '2026-01-15T06:05:00Z'),
    (1004, 104, 'APPROVED', 1250.00, '2026-01-15T08:05:00Z'),
    (1005, 105, 'APPROVED', 700.00, '2026-01-15T09:05:00Z');

INSERT INTO risk_rules (rule_id, rule_code, description, enabled) VALUES
    (1, 'RISK_DECLINED_PAYMENTS', 'Repeated declined payment attempts', 1),
    (2, 'RISK_HIGH_VALUE_ORDER', 'Completed order meets regional amount threshold', 1),
    (3, 'RISK_REPEAT_HIGH_VALUE_ORDERS', 'Repeated high-value completed orders inside a regional window', 1);

INSERT INTO regional_rule_config
    (rule_id, region, window_hours, event_count_threshold, amount_threshold)
VALUES
    (1, 'NORTH', 24, 3, NULL), (1, 'SOUTH', 24, 3, NULL),
    (1, 'EAST', 24, 3, NULL), (1, 'WEST', 24, 3, NULL),
    (2, 'NORTH', NULL, NULL, 1000.00), (2, 'SOUTH', NULL, NULL, 1000.00),
    (2, 'EAST', NULL, NULL, 800.00), (2, 'WEST', NULL, NULL, 1500.00),
    (3, 'NORTH', 48, 3, 600.00), (3, 'SOUTH', 36, 2, 550.00),
    (3, 'EAST', 24, 2, 500.00), (3, 'WEST', 72, 4, 750.00);
