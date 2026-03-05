import os
import threading
import uuid
import requests
from flask import Flask, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
# In a real CTF, secret key should be random and secure.
app.secret_key = 'super_secret_host_header_key_2026'

# In-memory database for the challenge
users = {
    "admin": {
        "password": "super_long_unguessable_password_12345!@#",
        "email": "admin@hitk-ctf.com",
        "reset_token": None
    }
}

FLAG = "DAKSHH{h0st_h34d3r_p01s0n1ng_f0r_t4h_w1n}"

# --- HTML Templates ---
HOME_HTML = '''
<!DOCTYPE html>
<html>
<head><title>HITK Corporate Login</title></head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h2>Secure Login</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color: red; list-style-type: none; padding: 0;">
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <br>
    <a href="/forgot_password">Forgot Password?</a>
</body>
</html>
'''

FORGOT_PWD_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Password Reset</title></head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h2>Reset Password</h2>
    <p>Enter your username to receive a password reset link.</p>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color: green; list-style-type: none; padding: 0;">
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="POST" action="/forgot_password">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <button type="submit">Send Reset Link</button>
    </form>
    <br>
    <a href="/">Back to Login</a>
</body>
</html>
'''

RESET_PWD_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Set New Password</title></head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h2>Enter New Password</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color: red; list-style-type: none; padding: 0;">
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="POST" action="/reset_password">
        <input type="hidden" name="token" value="{{ token }}">
        <input type="password" name="new_password" placeholder="New Password" required><br><br>
        <button type="submit">Reset Password</button>
    </form>
</body>
</html>
'''


# --- Helper to simulate Admin Email Click ---
def simulate_admin_click(reset_link):
    """
    Simulates the admin receiving the email and clicking the reset link.
    In a real scenario, this happens because the attacker poisoned the Host header,
    causing the app to generate a link to the attacker's server. When the admin clicks
    it, the token is leaked to the attacker.
    """
    try:
        # We make a quick GET request to whatever link was generated.
        # Timeout is short so we don't hang the server.
        requests.get(reset_link, timeout=3)
        print(f"[Admin Bot] Clicked link: {reset_link}")
    except Exception as e:
        print(f"[Admin Bot] Failed to click link: {e}")


# --- Routes ---
@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username == "admin" and users["admin"]["password"] == password:
        return f"<h1>Welcome Admin!</h1><p>Here is your flag: {FLAG}</p>"
    else:
        flash("Invalid credentials.")
        return redirect(url_for("home"))

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template_string(FORGOT_PWD_HTML)
    
    username = request.form.get("username")
    
    if username in users:
        # 1. Generate a secure, random reset token
        token = str(uuid.uuid4())
        users[username]["reset_token"] = token
        
        # 2. VULNERABILITY: Use the user-supplied Host header to build the link
        # Instead of a hardcoded internal domain or trusted config
        host = request.headers.get("Host", "127.0.0.1:5000")
        
        reset_link = f"http://{host}/reset_password?token={token}"
        
        print(f"[System] Generated reset link for {username}: {reset_link}")
        
        # 3. Simulate sending the email and the admin clicking the link
        if username == "admin":
            threading.Thread(target=simulate_admin_click, args=(reset_link,)).start()
            
        flash(f"A password reset link has been sent to {users[username]['email']}.")
    else:
        # Prevent username enumeration (always say it was sent)
        flash("If that username exists, a reset link was sent.")
        
    return redirect(url_for("forgot_password"))

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            flash("Missing reset token.")
            return redirect(url_for("home"))
        return render_template_string(RESET_PWD_HTML, token=token)
        
    # POST Request - perform the actual reset
    token = request.form.get("token")
    new_password = request.form.get("new_password")
    
    # Find user by token
    target_user = None
    for user, data in users.items():
        if data["reset_token"] == token:
            target_user = user
            break
            
    if target_user:
        users[target_user]["password"] = new_password
        users[target_user]["reset_token"] = None # Invalidate token
        flash("Password successfully reset! You can now login.")
        return redirect(url_for("home"))
    else:
        flash("Invalid or expired reset token.")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008)
