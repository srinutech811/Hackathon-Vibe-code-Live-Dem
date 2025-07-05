# VIBECODE Hackathon Demo – Live Presentation Guide

This document is your step-by-step script and checklist for a 5–20 min live demo and video submission for the VIBECODE Hackathon Use Case 3: "The Opacity and Inefficiency of Enterprise Financial Operations Insights."

---

## 1. **Project Introduction (1–2 min)**
- Project Name: **VIBECODE Hackathon Demo**
- Use Case: Transparency and efficiency in enterprise financial operations
- Tech Stack: Python Flask backend, single HTML/JS frontend, Snowflake DB
- No signup, no build tools—runs anywhere, easy for judges to test
- Key Features: Role-based access, real-time Snowflake reflection, audit logging, department-level summary

---

## 2. **Pain Point & Solution Overview (1–2 min)**
- Problem: Finance data is siloed, slow, and lacks transparency for employees, managers, and admins
- Solution: Unified dashboard with role-based access, live Snowflake integration, and audit logs
- Demo shows how this solves reporting, compliance, and transparency pain points

---

## 3. **Live Demo Walkthrough (10–15 min)**
### **A. Login Flow**
- Show Gmail-style login (username, then password)
- Mention demo users (employee1/password1, manager1/password2, admin1/password3)

### **B. Dashboard Features**
- **Financial Summary Table**
  - Shows department-wise budget, spent, remaining, last updated
  - Data comes live from Snowflake
- **Transactions Table**
  - Shows latest 50 transactions from Snowflake
- **Role-Based UI**
  - Employee: View only
  - Manager: Can add transactions
  - Admin: Can add transactions & view audit logs
- **Add Transaction**
  - Show form (with dropdown for category)
  - Add a transaction as manager/admin, show instant reflection in table
- **Audit Logs**
  - Log in as admin, show audit logs (who did what, when)

### **C. Security & Compliance**
- Session token auth, role-based endpoints, audit logging
- Only authorized actions allowed for each role

### **D. Snowflake Integration**
- Show Snowflake table (if possible)
- Prove real-time data reflection (add or update, see in Snowflake)

---

## 4. **Q&A and Value Proposition (2–3 min)**
- Invite questions about security, extensibility, or real-world fit
- Emphasize:
  - No manual reporting
  - All actions are auditable
  - Easy to deploy and extend
  - Works with real enterprise data

---

## 5. **How to Run the Demo (for judges)**
- Backend: `pip install -r requirements.txt && python flask_app.py`
- Frontend: Open `index.html` in browser
- Snowflake: Use provided SQL to create tables and seed data
- No signup, no cloud account needed

---

## 6. **Video Recording Tips**
- Use screen recorder (OBS, Zoom, etc.)
- Show each role (employee, manager, admin)
- Narrate your actions and what’s happening
- Keep video under 20 min
- Export as MP4 or MOV for easy download

---

## 7. **Downloadable Assets**
- This guide (Live_Demo_Guide.md)
- Video file (record and upload after demo)
- All code and SQL files in repo

---

**Good luck! Your demo is ready for a winning hackathon presentation.**
