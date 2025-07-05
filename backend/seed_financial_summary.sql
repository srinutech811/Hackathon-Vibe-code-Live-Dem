-- Seed demo data for financial_summary with department
INSERT INTO financial_summary (department, budget, spent, updated_at) VALUES
  ('IT',    50000, 20000, CURRENT_TIMESTAMP),
  ('HR',    30000, 12000, CURRENT_TIMESTAMP),
  ('Sales', 70000, 35000, CURRENT_TIMESTAMP),
  ('Ops',   40000, 15000, CURRENT_TIMESTAMP);
