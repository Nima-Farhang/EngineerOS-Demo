PRAGMA foreign_keys = ON;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,
    region TEXT NOT NULL CHECK (region IN ('NORTH', 'SOUTH', 'EAST', 'WEST')),
    created_at TEXT NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_status TEXT NOT NULL CHECK (order_status IN ('PENDING', 'COMPLETED', 'CANCELLED')),
    order_amount NUMERIC NOT NULL CHECK (order_amount >= 0),
    ordered_at TEXT NOT NULL
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    payment_status TEXT NOT NULL CHECK (payment_status IN ('APPROVED', 'DECLINED')),
    attempted_amount NUMERIC NOT NULL CHECK (attempted_amount >= 0),
    attempted_at TEXT NOT NULL
);

CREATE TABLE risk_rules (
    rule_id INTEGER PRIMARY KEY,
    rule_code TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    enabled INTEGER NOT NULL DEFAULT 1 CHECK (enabled IN (0, 1))
);

CREATE TABLE regional_rule_config (
    rule_id INTEGER NOT NULL REFERENCES risk_rules(rule_id),
    region TEXT NOT NULL CHECK (region IN ('NORTH', 'SOUTH', 'EAST', 'WEST')),
    window_hours INTEGER CHECK (window_hours > 0),
    event_count_threshold INTEGER CHECK (event_count_threshold > 0),
    amount_threshold NUMERIC CHECK (amount_threshold >= 0),
    PRIMARY KEY (rule_id, region)
);

CREATE TABLE monitoring_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    monitoring_time TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('RUNNING', 'COMPLETED', 'FAILED'))
);

CREATE TABLE alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    rule_id INTEGER NOT NULL REFERENCES risk_rules(rule_id),
    monitoring_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'CLOSED')),
    qualifying_event_count INTEGER NOT NULL,
    qualifying_amount NUMERIC NOT NULL,
    created_at TEXT NOT NULL
);

CREATE UNIQUE INDEX one_open_alert_per_customer_rule_date
ON alerts(customer_id, rule_id, monitoring_date)
WHERE status = 'OPEN';

CREATE VIEW v_customer_payment_activity AS
SELECT p.payment_id, o.customer_id, c.region, p.order_id,
       p.payment_status, p.attempted_amount, p.attempted_at
FROM payments AS p
JOIN orders AS o ON o.order_id = p.order_id
JOIN customers AS c ON c.customer_id = o.customer_id;

CREATE VIEW v_completed_order_activity AS
SELECT o.order_id, o.customer_id, c.region, o.order_amount, o.ordered_at
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.order_status = 'COMPLETED';
