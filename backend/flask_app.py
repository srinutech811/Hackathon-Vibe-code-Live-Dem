import os
import uuid
from flask import Flask, jsonify, request
import snowflake.connector
from flask_cors import CORS
from functools import wraps
from datetime import datetime

# Demo users for role-based login
USERS = {
    'employee1': {'password': 'password1', 'role': 'employee'},
    'manager1': {'password': 'password2', 'role': 'manager'},
    'admin1': {'password': 'password3', 'role': 'admin'},
}
SESSIONS = {}  # session_token: {'username': ..., 'role': ...}

# Set your Snowflake credentials here or via environment variables
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER', 'your_user')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD', 'your_password')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT', 'your_account')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE', 'your_db')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE', 'your_warehouse')

app = Flask(__name__)
CORS(app)

def get_snowflake_conn():
    print(f"[DEBUG] Connecting to Snowflake with:")
    print(f"  USER: {SNOWFLAKE_USER}")
    print(f"  ACCOUNT: {SNOWFLAKE_ACCOUNT}")
    print(f"  DATABASE: {SNOWFLAKE_DATABASE}")
    print(f"  SCHEMA: {SNOWFLAKE_SCHEMA}")
    print(f"  WAREHOUSE: {SNOWFLAKE_WAREHOUSE}")
    try:
        return snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            warehouse=SNOWFLAKE_WAREHOUSE,
        )
    except Exception as e:
        print(f"[ERROR] Snowflake connection failed: {e}")
        raise

def log_audit(user, action):
    try:
        conn = get_snowflake_conn()
        cs = conn.cursor()
        cs.execute("INSERT INTO audit_logs (user, action, timestamp) VALUES (%s, %s, %s)", (
            user, action, datetime.utcnow()
        ))
        cs.close()
        conn.close()
    except Exception as e:
        print('Audit log error:', e)

def require_role(roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            session = SESSIONS.get(token)
            if not session or session['role'] not in roles:
                return jsonify({'error': 'Not authorized'}), 403
            request.user = session
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    print(f"LOGIN ATTEMPT: username={username!r}, password={password!r}")  # Debug print
    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = str(uuid.uuid4())
    SESSIONS[token] = {'username': username, 'role': user['role']}
    log_audit(username, 'login')
    return jsonify({'token': token, 'role': user['role']})

@app.route('/api/mfa', methods=['POST'])
def mfa():
    # Stub for demo
    return jsonify({'success': True, 'message': 'MFA not implemented in demo'})

@app.route('/api/summary')
@require_role(['employee', 'manager', 'admin'])
def summary():
    try:
        user = request.user['username']
        conn = get_snowflake_conn()
        cs = conn.cursor()
        cs.execute("SELECT department, budget, spent, updated_at FROM financial_summary;")
        rows = cs.fetchall()
        result = [
            {
                'department': row[0],
                'budget': row[1] or 0,
                'spent': row[2] or 0,
                'remaining': (row[1] or 0) - (row[2] or 0),
                'last_updated': str(row[3]) if row[3] else ''
            }
            for row in rows
        ]
        cs.close()
        conn.close()
        log_audit(user, 'view_summary')
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions')
@require_role(['employee', 'manager', 'admin'])
def transactions():
    try:
        user = request.user['username']
        conn = get_snowflake_conn()
        cs = conn.cursor()
        cs.execute("SELECT id, department, amount, category, date FROM transactions ORDER BY id DESC LIMIT 50;")
        txns = [
            {'id': row[0], 'department': row[1], 'amount': row[2], 'category': row[3], 'date': str(row[4])}
            for row in cs.fetchall()
        ]
        cs.close()
        conn.close()
        log_audit(user, 'view_transactions')
        return jsonify(txns)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_transaction', methods=['POST'])
@require_role(['manager', 'admin'])
def add_transaction():
    try:
        user = request.user['username']
        data = request.json
        conn = get_snowflake_conn()
        cs = conn.cursor()
        cs.execute(
            "INSERT INTO transactions (department, amount, category, date) VALUES (%s, %s, %s, %s)",
            (data['department'], data['amount'], data['category'], data['date'])
        )
        conn.commit()
        cs.close()
        conn.close()
        log_audit(user, f"add_transaction: {data}")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audit_logs')
@require_role(['admin'])
def audit_logs():
    try:
        user = request.user['username']
        conn = get_snowflake_conn()
        cs = conn.cursor()
        cs.execute("SELECT id, user, action, timestamp FROM audit_logs ORDER BY id DESC LIMIT 50;")
        logs = [
            {'id': row[0], 'user': row[1], 'action': row[2], 'timestamp': str(row[3])}
            for row in cs.fetchall()
        ]
        cs.close()
        conn.close()
        log_audit(user, 'view_audit_logs')
        return jsonify(logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_frontend():
    return app.send_static_file('../frontend/index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
