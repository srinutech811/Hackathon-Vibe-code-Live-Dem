# Backend (Flask) – Simple Live Demo

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Configure Snowflake credentials in `.env` (see example below).
   - Copy `.env.example` to `.env` and fill in your values.
3. Run the server:
   ```
   python flask_app.py
   ```

## .env Example
```
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_DATABASE=your_db
SNOWFLAKE_SCHEMA=MY_DEMO_SCHEMA
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

## Endpoints
- `/api/summary` (GET): Financial summary
- `/api/transactions` (GET): List of transactions

## Demo Database Schema
See `snowflake_demo.sql` for table setup.

---

## Live Demo Instructions
- Start this backend, then open `../frontend/index.html` in your browser.
- The frontend will call this backend for live Snowflake data.
