# VIBECODING HACKATHON 2025 – Use Case 3 Demo

## Overview
A full-stack solution for transparent, secure, and real-time enterprise financial operations insights.

### Tech Stack
- **Frontend:** React (role-based dashboard, login, data explorer)
- **Backend:** FastAPI (Python, REST API, Snowflake integration)
- **Database:** Snowflake Cloud (schema + mock/demo ready)
- **Security:** Role-based access, audit trail, stub MFA

## Folder Structure
```
/backend/    # FastAPI backend
/frontend/   # React frontend
```

---

## 🚀 Deployment Guide

### 1. Backend (FastAPI, Render.com Free Cloud Host)
- Push `/backend` to a public GitHub repo
- Deploy on [Render.com](https://render.com/) (see `/backend/README.md` for step-by-step)
- Set environment variables from `.env.example`
- Your backend will be live at: `https://<your-backend-name>.onrender.com`

### 2. Frontend (React, Netlify)
- From `/frontend`:
  ```bash
  npm install -g netlify-cli
  npm install
  npm run build
  netlify login
  netlify deploy --prod
  ```
- Use `build` as the publish directory
- Update API URLs in frontend to your Render backend URL before final deploy
- Your frontend will be live at: `https://<your-site>.netlify.app`

---

## 👤 Demo Users
- `employee1` / `password1` (Employee)
- `manager1` / `password2` (Manager)
- `admin1` / `password3` (Admin)

## Features
- Login (role-based)
- Financial dashboard (real-time summary)
- Data explorer (transactions)
- Audit trail (admin only)
- Secure API (stub MFA)

---

## Submission Checklist
- [x] Public GitHub repository with all code and clear README
- [x] Frontend deployed (Netlify)
- [x] Backend deployed (Render.com)
- [x] Demo video (walkthrough of use case, features, and DB reflection)
- [x] Database reflection: Data entered in frontend visible in backend/Snowflake (or mock)
- [x] Role-based access, audit trail, compliance features

---

## Judges & Reviewers: How to Test
1. Open the Netlify frontend URL
2. Login as any demo user above
3. View dashboard, transactions, and (if admin) audit logs
4. All data is live or demo-mocked from Snowflake
5. All code and setup instructions are in this repo

---

For any issues or questions, see `/backend/README.md` and `/frontend/README.md` for detailed setup and troubleshooting.
