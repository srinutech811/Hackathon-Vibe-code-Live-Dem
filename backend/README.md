# Backend (FastAPI)

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Configure Snowflake credentials in `.env` (see example below).
3. Run the server:
   ```
   uvicorn main:app --reload
   ```

## .env Example
```
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_DATABASE=your_db
SNOWFLAKE_SCHEMA=public
SNOWFLAKE_WAREHOUSE=your_warehouse
```

## Endpoints
- `/auth/login` (POST): Login, returns JWT
- `/auth/mfa` (POST): Stub MFA
- `/financial/summary` (GET): Dashboard metrics
- `/financial/transactions` (GET): Data explorer
- `/audit/logs` (GET): Audit trail (admin)

## Demo Database Schema
See `snowflake_demo.sql` for table setup.

---

## 🚀 Deploy to Render.com (Free Cloud Python Host)

1. Push your `/backend` code to a public GitHub repo.
2. Go to [Render.com](https://render.com/) and create a free account.
3. Click "New Web Service" and connect your GitHub repo.
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
6. Add environment variables from `.env.example` (SNOWFLAKE configs).
7. Deploy! Your API will be live at `https://<your-backend-name>.onrender.com`

For local dev, use `.env`. For Render, use their dashboard to set secrets.

---
