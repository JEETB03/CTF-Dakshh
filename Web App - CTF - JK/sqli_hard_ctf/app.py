import sqlite3
import unicodedata
import os
from flask import Flask, request, render_template_string, flash

app = Flask(__name__)
app.secret_key = 'hard_sqli_secret_2026'

DB_FILE = "vault.db"
FLAG = "DAKSHH{un1c0d3_n0rm4l1z4t10n_sqli_ph4nt0m}"

# --- Setup DB ---
def init_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE config (key TEXT, value TEXT)''')
    c.execute("INSERT INTO config (key, value) VALUES ('admin_note', ?)", (FLAG,))
    c.execute("INSERT INTO config (key, value) VALUES ('sys_status', 'Online')")
    c.execute("INSERT INTO config (key, value) VALUES ('maintenance', 'False')")
    conn.commit()
    conn.close()

# --- WAF: AI/Scanner Defeat ---
def waf(payload):
    # This WAF blocks standard injection characters
    blacklist = ["'", '"', ';', 'union', 'select', '--', '/*']
    for word in blacklist:
        if word in payload.lower():
            return True, word
    return False, ""

# --- HTML Template ---
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head><title>System Configuration Lookup</title></head>
<body style="font-family: Arial; margin: 40px; background-color: #1a1a1a; color: #00ff00;">
    <h2>Restricted Vault Config Lookup</h2>
    <p>Enter a configuration key to check its value.</p>
    
    <form method="POST">
        <input type="text" name="key" placeholder="sys_status" style="padding: 5px;">
        <button type="submit" style="padding: 5px;">Search</button>
    </form>
    
    <br>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color: red;">
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    {% if result %}
        <p><strong>Config Value:</strong> {{ result[0] }}</p>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template_string(HTML_PAGE)
        
    user_key = request.form.get("key", "")
    
    # 1. WAF Check (Blocks standard quotes)
    blocked, word = waf(user_key)
    if blocked:
        flash(f"[SECURITY] Intrusion Attempt Blocked! Illegal sequence/character '{word}' detected.")
        return render_template_string(HTML_PAGE)
        
    # 2. VULNERABILITY: Unicode Normalization AFTER the WAF Check
    # A fullwidth apostrophe '＇' (U+FF07) gets past the WAF, but normalize turns it into a standard ASCII `'` (U+0027).
    normalized_key = unicodedata.normalize('NFKC', user_key)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    result = None
    try:
        # 3. Flawed query using string formatting on the normalized string
        query = f"SELECT value FROM config WHERE key = '{normalized_key}'"
        c.execute(query)
        result = c.fetchone()
    except sqlite3.Error as e:
        # Don't show the error to make it harder
        pass
    finally:
        conn.close()
        
    if not result:
        flash("Configuration key not found.")
        
    return render_template_string(HTML_PAGE, result=result)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5003)
