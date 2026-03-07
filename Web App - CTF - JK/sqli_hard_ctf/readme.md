# 🛡️ Ghost in the WAF — Unicode SQLi CTF

**Category:** Web Application Security  
**Difficulty:** Hard (500 Points) — "Anti-AI / Unicode Phantom"  
**Flag Format:** `DAKSHH{flag}`

> *"Welcome to the Restricted Vault Configuration portal. We take security seriously here. Our Web Application Firewall (WAF) was formally verified and provably blocks *all* SQL injection attempts. We dare you to try and break it. If you can read the `admin_note` configuration key, you get the flag."*

---

## Challenge Overview
This is the final and hardest challenge in the SQLi series. It is a highly specific "Anti-AI" challenge designed to defeat static code analysis tools and automated solvers like `sqlmap` or standard LLMs.

### The "Anti-AI" Mechanism:
The application's Web Application Firewall (`waf()`) flawlessly blocks all standard SQL injection characters: `'`, `"`, `;`, `UNION`, `SELECT`, `--`. It is seemingly impossible to inject SQL directly.

However, the application uses Python's `unicodedata.normalize('NFKC', user_input)` *after* the WAF check, but *before* formatting the SQL string.
Automated tools almost never test for Unicode translation bypasses unless explicitly programmed to do so for a specific framework.

---

## 🔧 How to Start the Challenge Room (Step-by-Step)

### Prerequisites
- **Python 3.x** installed

### Step 1: Install Python Dependencies
Open a terminal in the challenge directory and run:
```bash
pip install flask requests
```

### Step 2: Start the Web Server
Launch the Flask application:
```bash
python app.py
```
> **Note:** The server will automatically initialize the database `vault.db` and seed the flag upon startup. It runs entirely on **http://127.0.0.1:5003**.

### Step 3: Access the Challenge Room
Players can now open their browser and go to:
```
http://127.0.0.1:5003
```

### Step 4: Stop the Room (When Done)
Press `Ctrl + C` in the terminal where the server is running.

---

## 🔑 Writeup — How to Solve (Player Walkthrough)

Here is the exact manual path a player takes to solve this room from scratch without using automated scripts:

### Step 1: Reconnaissance (Finding the Wall)
Open your browser and navigate to the challenge: `http://127.0.0.1:5003`
You see a simple search box asking for a "Config Key" (like `sys_status`).

As a hacker, your very first instinct is to try a basic SQL Injection payload to bypass the login or dump data. 
You type in:
`' OR '1'='1` 
and hit **SEARCH**.

**The Result:** The screen flashes red: `[SECURITY] Intrusion Attempt Blocked! Illegal sequence/character ''' detected.`
The WAF (Web Application Firewall) caught you because it saw the standard single quote (`'`).

### Step 2: The Theorizing (The "Aha!" Moment)
You think: *"Okay, the WAF is perfectly blocking ASCII characters. I can't inject SQL syntax directly. But what if the backend processes the text *after* the WAF checks it?"*

If the application is written in Python (a very common CTF scenario), it might use a function called `unicodedata.normalize()` to clean up weird user inputs before putting them into the database query.

You need a character that **is NOT an apostrophe** (so the WAF ignores it), but will be **turned INTO an apostrophe** by the normalizer.

### Step 3: Finding the Phantom Characters
You open a new tab and Google: *"Unicode Fullwidth Characters"* or *"Unicode Normalization SQLi Bypass"*.
You learn about the **Fullwidth Apostrophe**, which is commonly used in Asian typography. 

You literally copy-paste these characters from the internet:
- Fullwidth Apostrophe: `＇`
- Fullwidth Equals Sign: `＝`

*Notice how they look slightly wider and weirder than normal `'` and `=`? To a computer, these are completely different numbers. The WAF has no idea what they are, so it lets them through!*

### Step 4: Building the Payload
Instead of typing `' OR 'a'='a`, you construct your payload using the copied Fullwidth characters.

You copy this exact string:
**`＇ OR ＇a＇＝＇a`**

### Step 5: Capture The Flag
1. Go back to `http://127.0.0.1:5003`
2. **Paste** that exact string into the search box.
3. Hit **SEARCH**.

**What happens in the backend:**
1. The WAF scans your string. It says, "I don't see any normal single quotes. You're good to go!"
2. Python takes your weird `＇` symbols and normalizes them into standard `'` marks.
3. The SQL query executes: `SELECT value FROM config WHERE key = '' OR 'a'='a'`
4. Since `'a'='a'` is always true, the database spits out the very first row in the table.

The webpage reloads, and right there on the screen in green text is the `admin_note` containing the flag:
🏆 `DAKSHH{un1c0d3_n0rm4l1z4t10n_sqli_ph4nt0m}`

---

## 🛡️ Admin Verification (Automated Test)

You can run the provided solver script to automatically verify the challenge is working and executing the Unicode Normalization bypass:
```bash
python solve.py
```
This script will bypass the WAF using fullwidth characters and extract the flag directly in your terminal.

---
Contributor: Jyotirmoy Karmakar (0xjyotirmoy)
