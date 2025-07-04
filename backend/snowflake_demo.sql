-- Demo schema for Snowflake
CREATE TABLE IF NOT EXISTS financial_summary (
    id INT AUTOINCREMENT,
    budget FLOAT,
    spent FLOAT,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTOINCREMENT,
    department STRING,
    amount FLOAT,
    category STRING,
    date DATE
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTOINCREMENT,
    user STRING,
    action STRING,
    timestamp TIMESTAMP
);
