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

# --- Shared CSS ---
SHARED_CSS = '''
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Orbitron:wght@500;700&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
        font-family: 'Fira Code', monospace;
        background-color: #0a0a0a;
        color: #00ff41;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    /* Matrix rain background */
    body::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(ellipse at 20% 50%, rgba(0, 255, 65, 0.03) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 50%, rgba(0, 255, 65, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    .scanline {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 255, 65, 0.015) 2px,
            rgba(0, 255, 65, 0.015) 4px
        );
        pointer-events: none;
        z-index: 1;
    }
    
    .container {
        position: relative;
        z-index: 2;
        width: 420px;
        background: linear-gradient(145deg, #0d0d0d, #141414);
        border: 1px solid rgba(0, 255, 65, 0.2);
        border-radius: 12px;
        padding: 40px;
        box-shadow: 
            0 0 30px rgba(0, 255, 65, 0.08),
            0 0 60px rgba(0, 255, 65, 0.04),
            inset 0 1px 0 rgba(0, 255, 65, 0.1);
    }
    
    .logo {
        text-align: center;
        margin-bottom: 8px;
    }
    
    .logo-icon {
        font-size: 40px;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 10px rgba(0, 255, 65, 0.5));
    }
    
    h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        text-align: center;
        color: #00ff41;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        margin-bottom: 6px;
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        color: #3a7a3a;
        font-size: 0.75rem;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }
    
    .flash-messages {
        list-style: none;
        padding: 0;
        margin-bottom: 20px;
    }
    
    .flash-messages li {
        background: rgba(0, 255, 65, 0.08);
        border: 1px solid rgba(0, 255, 65, 0.2);
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.8rem;
        color: #00ff41;
    }
    
    .flash-messages.error li {
        background: rgba(255, 50, 50, 0.1);
        border-color: rgba(255, 50, 50, 0.3);
        color: #ff4040;
    }
    
    .input-group {
        position: relative;
        margin-bottom: 20px;
    }
    
    .input-group label {
        display: block;
        font-size: 0.7rem;
        color: #3a7a3a;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }
    
    .input-group input {
        width: 100%;
        padding: 12px 14px;
        background: rgba(0, 255, 65, 0.04);
        border: 1px solid rgba(0, 255, 65, 0.15);
        border-radius: 6px;
        color: #00ff41;
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        outline: none;
        transition: all 0.3s ease;
    }
    
    .input-group input:focus {
        border-color: #00ff41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.15);
        background: rgba(0, 255, 65, 0.06);
    }
    
    .input-group input::placeholder {
        color: #2a5a2a;
    }
    
    .btn {
        width: 100%;
        padding: 13px;
        background: linear-gradient(135deg, #00cc33, #00ff41);
        border: none;
        border-radius: 6px;
        color: #0a0a0a;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 2px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        margin-top: 5px;
    }
    
    .btn:hover {
        background: linear-gradient(135deg, #00ff41, #33ff66);
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.35);
        transform: translateY(-1px);
    }
    
    .btn:active {
        transform: translateY(0);
    }
    
    .link {
        display: block;
        text-align: center;
        margin-top: 24px;
        color: #3a7a3a;
        text-decoration: none;
        font-size: 0.8rem;
        transition: color 0.3s ease;
    }
    
    .link:hover {
        color: #00ff41;
        text-shadow: 0 0 8px rgba(0, 255, 65, 0.3);
    }
    
    .terminal-bar {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 24px;
        padding: 8px 12px;
        background: #0a0a0a;
        border-radius: 6px 6px 0 0;
        border-bottom: 1px solid rgba(0, 255, 65, 0.1);
    }
    
    .terminal-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }
    
    .dot-red { background: #ff5f57; }
    .dot-yellow { background: #ffbd2e; }
    .dot-green { background: #28c840; }
    
    .footer {
        text-align: center;
        margin-top: 28px;
        padding-top: 16px;
        border-top: 1px solid rgba(0, 255, 65, 0.08);
        color: #1a3a1a;
        font-size: 0.65rem;
        letter-spacing: 1px;
    }
    
    @keyframes glow-pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    .status-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        background: #00ff41;
        border-radius: 50%;
        margin-right: 6px;
        animation: glow-pulse 2s infinite;
        box-shadow: 0 0 6px #00ff41;
    }
'''

# --- HTML Templates ---
HOME_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HITK Secure Portal - Login</title>
    <style>''' + SHARED_CSS + '''</style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <div class="terminal-bar">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
        </div>
        <div class="logo">
            <div class="logo-icon">🛡️</div>
        </div>
        <h1>Secure Login</h1>
        <p class="subtitle"><span class="status-dot"></span>HITK Corporate Portal v2.6</p>
        
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul class="flash-messages error">
            {% for message in messages %}
              <li>⚠ {{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        
        <form method="POST" action="/login">
            <div class="input-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter username" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit" class="btn">Authenticate</button>
        </form>
        <a href="/forgot_password" class="link">[ Forgot Password? ]</a>
        <div class="footer">DAKSHH CTF &bull; Secure Systems Division</div>
    </div>
</body>
</html>
'''

FORGOT_PWD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HITK Secure Portal - Password Reset</title>
    <style>''' + SHARED_CSS + '''</style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <div class="terminal-bar">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
        </div>
        <div class="logo">
            <div class="logo-icon">🔑</div>
        </div>
        <h1>Password Reset</h1>
        <p class="subtitle">Enter your username to receive a reset link</p>
        
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul class="flash-messages">
            {% for message in messages %}
              <li>✓ {{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        
        <form method="POST" action="/forgot_password">
            <div class="input-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter username" required>
            </div>
            <button type="submit" class="btn">Send Reset Link</button>
        </form>
        <a href="/" class="link">[ Back to Login ]</a>
        <div class="footer">DAKSHH CTF &bull; Secure Systems Division</div>
    </div>
</body>
</html>
'''

RESET_PWD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HITK Secure Portal - Set New Password</title>
    <style>''' + SHARED_CSS + '''</style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <div class="terminal-bar">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
        </div>
        <div class="logo">
            <div class="logo-icon">🔐</div>
        </div>
        <h1>New Password</h1>
        <p class="subtitle">Set a new password for your account</p>
        
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul class="flash-messages error">
            {% for message in messages %}
              <li>⚠ {{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        
        <form method="POST" action="/reset_password">
            <input type="hidden" name="token" value="{{ token }}">
            <div class="input-group">
                <label>New Password</label>
                <input type="password" name="new_password" placeholder="Enter new password" required>
            </div>
            <button type="submit" class="btn">Reset Password</button>
        </form>
        <div class="footer">DAKSHH CTF &bull; Secure Systems Division</div>
    </div>
</body>
</html>
'''

FLAG_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HITK Secure Portal - Access Granted</title>
    <style>
        ''' + SHARED_CSS + '''
        
        .flag-box {
            background: rgba(0, 255, 65, 0.05);
            border: 1px solid rgba(0, 255, 65, 0.3);
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            text-align: center;
            word-break: break-all;
        }
        
        .flag-label {
            font-size: 0.7rem;
            color: #3a7a3a;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        
        .flag-value {
            font-family: 'Fira Code', monospace;
            font-size: 1.05rem;
            color: #00ff41;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
            animation: glow-pulse 2s infinite;
        }
        
        .welcome-text {
            text-align: center;
            color: #00ff41;
            font-size: 0.85rem;
            margin-top: 16px;
            line-height: 1.6;
        }
        
        .access-badge {
            display: inline-block;
            background: rgba(0, 255, 65, 0.12);
            border: 1px solid rgba(0, 255, 65, 0.25);
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.7rem;
            color: #00ff41;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <div class="terminal-bar">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
        </div>
        <div class="logo">
            <div class="logo-icon">🏆</div>
        </div>
        <h1>Access Granted</h1>
        <p class="subtitle"><span class="status-dot"></span>Authentication Successful</p>
        <div style="text-align:center;">
            <span class="access-badge">Admin Level</span>
        </div>
        <p class="welcome-text">Welcome back, Administrator.<br>Your classified data is below.</p>
        <div class="flag-box">
            <div class="flag-label">Captured Flag</div>
            <div class="flag-value">{{ flag }}</div>
        </div>
        <a href="/" class="link">[ Logout ]</a>
        <div class="footer">DAKSHH CTF &bull; Secure Systems Division</div>
    </div>
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
        return render_template_string(FLAG_HTML, flag=FLAG)
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
