import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import snowflake.connector
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# Load env vars
load_dotenv()

app = FastAPI()

# Security
SECRET_KEY = "hackathon_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Demo users/roles (in production, use DB)
users_db = {
    "employee1": {"username": "employee1", "hashed_password": pwd_context.hash("password1"), "role": "employee"},
    "manager1": {"username": "manager1", "hashed_password": pwd_context.hash("password2"), "role": "manager"},
    "admin1": {"username": "admin1", "hashed_password": pwd_context.hash("password3"), "role": "admin"},
}

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    role: str

class MFARequest(BaseModel):
    code: str

class FinancialSummary(BaseModel):
    total_budget: float
    total_spent: float
    remaining_budget: float
    last_updated: str

class Transaction(BaseModel):
    id: int
    department: str
    amount: float
    category: str
    date: str

class AuditLog(BaseModel):
    id: int
    user: str
    action: str
    timestamp: str

# Auth helpers
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": role}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required_roles: List[str]):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in required_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker

# Snowflake connection helper
def get_snowflake_conn():
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        )
        return conn
    except Exception as e:
        print("Snowflake connection failed:", e)
        return None

# --- API ROUTES ---

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # MFA stub: always require MFA for demo
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/mfa")
def mfa_verify(req: MFARequest):
    # Stub: accept any code for demo
    if req.code:
        return {"status": "MFA success"}
    raise HTTPException(status_code=400, detail="Invalid MFA code")

@app.get("/financial/summary", response_model=FinancialSummary)
def get_financial_summary(user=Depends(require_role(["employee", "manager", "admin"]))):
    # Demo: return static or mock Snowflake data
    conn = get_snowflake_conn()
    if conn:
        try:
            cs = conn.cursor()
            cs.execute("SELECT SUM(budget), SUM(spent), MAX(updated_at) FROM financial_summary;")
            row = cs.fetchone()
            summary = FinancialSummary(
                total_budget=row[0] or 1000000,
                total_spent=row[1] or 500000,
                remaining_budget=(row[0] or 1000000)-(row[1] or 500000),
                last_updated=str(row[2]) if row[2] else str(datetime.now()),
            )
        finally:
            conn.close()
    else:
        summary = FinancialSummary(
            total_budget=1000000,
            total_spent=500000,
            remaining_budget=500000,
            last_updated=str(datetime.now()),
        )
    return summary

@app.get("/financial/transactions", response_model=List[Transaction])
def get_transactions(user=Depends(require_role(["employee", "manager", "admin"]))):
    # Demo: return static or mock Snowflake data
    conn = get_snowflake_conn()
    txns = []
    if conn:
        try:
            cs = conn.cursor()
            cs.execute("SELECT id, department, amount, category, date FROM transactions LIMIT 50;")
            for row in cs:
                txns.append(Transaction(id=row[0], department=row[1], amount=row[2], category=row[3], date=str(row[4])))
        finally:
            conn.close()
    else:
        txns = [
            Transaction(id=1, department="IT", amount=20000, category="Hardware", date="2025-07-01"),
            Transaction(id=2, department="HR", amount=5000, category="Training", date="2025-07-02"),
        ]
    return txns

@app.get("/audit/logs", response_model=List[AuditLog])
def get_audit_logs(user=Depends(require_role(["admin"]))):
    # Demo: return static or mock Snowflake data
    conn = get_snowflake_conn()
    logs = []
    if conn:
        try:
            cs = conn.cursor()
            cs.execute("SELECT id, user, action, timestamp FROM audit_logs LIMIT 50;")
            for row in cs:
                logs.append(AuditLog(id=row[0], user=row[1], action=row[2], timestamp=str(row[3])))
        finally:
            conn.close()
    else:
        logs = [
            AuditLog(id=1, user="admin1", action="Viewed summary", timestamp=str(datetime.now())),
        ]
    return logs

@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    # For demo: log all accesses (in real, log to DB)
    response = await call_next(request)
    path = request.url.path
    user = request.headers.get("authorization", "anonymous")
    print(f"AUDIT: {datetime.now()} | {user} | {path}")
    return response
