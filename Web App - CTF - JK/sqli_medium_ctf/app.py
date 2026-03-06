import sqlite3
import os
from flask import Flask, request, render_template, flash

app = Flask(__name__)
app.secret_key = 'medium_sqli_secret_2026'

DB_FILE = "users.db"

FLAG = "DAKSHH{w4f_byp4ss_w1th0ut_c0mp4r1s0ns}"

# --- Setup DB ---
def init_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, profile_data TEXT)''')
    # Admin holds the flag
    c.execute("INSERT INTO users (username, profile_data) VALUES ('admin', ?)", (FLAG,))
    # Dummy users
    c.execute("INSERT INTO users (username, profile_data) VALUES ('guest1', 'Just a normal user')")
    c.execute("INSERT INTO users (username, profile_data) VALUES ('guest2', 'Another normal user')")
    c.execute("INSERT INTO users (username, profile_data) VALUES ('test_user', 'Testing account')")
    conn.commit()
    conn.close()

# --- WAF: The Anti-AI Filter ---
import re
def waf(payload):
    # Block EVERYTHING an AI would use for a typical blind SQLi or string slicing
    blacklist = [
        '<', '>', '=', 'between', 'like', 'in', 'and', 'or', 'union',
        'substr', 'substring', 'mid', 'char', 'hex', 'ascii', 'limit', 'offset'
    ]
    payload_lower = payload.lower()
    for word in blacklist:
        if word in ['<', '>', '=']:
            if word in payload_lower:
                return True, word
        else:
            if re.search(r'\b' + word + r'\b', payload_lower):
                return True, word
    return False, ""

@app.route("/")
def index():
    sort_param = request.args.get("sort", "id")
    
    # 1. WAF Check
    blocked, word = waf(sort_param)
    if blocked:
        flash(f"WAF Blocked Request: Illegal keyword/character '{word}' detected.")
        return render_template('index.html', users=[], str=str)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    users = []
    try:
        # VULNERABILITY: Unsafe injection in the ORDER BY clause
        query = f"SELECT id, username FROM users ORDER BY {sort_param}"
        c.execute(query)
        users = c.fetchall()
    except sqlite3.Error as e:
        flash(f"Database Error: {e}")
    finally:
        conn.close()
        
    return render_template('index.html', users=users, str=str)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5002)
