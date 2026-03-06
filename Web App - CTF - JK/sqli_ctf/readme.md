# 💉 Query Breaker — SQL Injection CTF

**Category:** Web Application Security  
**Difficulty:** Easy (100 Points)  
**Flag Format:** `DAKSHH{flag}`

> *"The login portal stands between you and the admin's secrets. You don't know the password, but maybe the database is gullible enough to let you in anyway. Can you sweet-talk the backend into bypassing the authentication check?"*

---

## Challenge Overview

This is an introductory **SQL Injection (SQLi)** challenge focusing on **Authentication Bypass**. The application takes user input from the login form and concatenates it directly into the backend SQLite query without proper parameterization or sanitization.

### Hints for Players
- **Hint 1:** Have you tried logging in as `admin`? The application might be trusting your input too much.
- **Hint 2:** The backend query probably looks like `SELECT * FROM users WHERE username='[USER]' AND password='[PASS]';`.
- **Hint 3:** What happens if you try to make the password check evaluate to `TRUE` no matter what? Try an input like `' OR '1'='1`.

---

## 🔧 How to Start the Challenge Room (Step-by-Step)

### Prerequisites
- **Python 3.x** installed

### Step 1: Install Python Dependencies
Open a terminal in the challenge directory and run:
```bash
pip install flask
```

### Step 2: (Optional) Delete Old Database for Fresh Start
If you are restarting the challenge, delete the old database file so the server can generate a fresh one:
```bash
del challenge.db
```

### Step 3: Start the Web Server
Launch the Flask application:
```bash
python app.py
```
> **Note:** The server will start running on **http://127.0.0.1:5001**.
> **Database Initialization:** The database (`challenge.db`) and the `admin` user are automatically created the moment the server boots up. No manual setup required!

### Step 4: Access the Challenge Room
Players can now open their browser and go to:
```
http://127.0.0.1:5001
```

### Step 5: Stop the Room (When Done)
Press `Ctrl + C` in the terminal where the server is running.

---

## 🔑 Writeup — How to Solve (Player Walkthrough)

### Step 1: Reconnaissance
1. Navigate to `http://127.0.0.1:5001`
2. You see a standard Login and Registration form.
3. Trying to register as `admin` fails with the message: *"[ You can't register with admin username ]"*.
4. This confirms the `admin` user exists.

### Step 2: Formulate the Attack
The vulnerability lies in how the backend constructs the SQL query. It looks roughly like this:
```sql
SELECT * FROM users WHERE username='[INPUT_USER]' AND password='[INPUT_PASS]';
```

Our goal is to log in as `admin` without knowing the password. We can use SQL Injection to comment out the password check or make the condition universally true.

### Step 3: Execute the Injection
1. In the **Target Username** field, enter: `admin`
2. In the **Authorization Key** (Password) field, enter exactly this payload: `' OR 1=1 --`
3. Click **Initiate Login**.

### What happens in the backend?
The query becomes:
```sql
SELECT * FROM users WHERE username='admin' AND password='' OR 1=1 --';
```
- The `'` closes the password string early.
- The `OR 1=1` ensures the `WHERE` clause always evaluates to True (since 1 equals 1).
- The `--` is an SQL comment, making the database ignore the trailing `'` (preventing a syntax error).

### Step 4: Capture the Flag
The application successfully logs you in as the admin and immediately reveals a terminal access screen with the flag:
🏆 `DAKSHH{sqli_3asy_byP4ss_2026}`

---

## 🛡️ Admin Verification (Automated Test)

You can run the provided solver script to automatically verify the challenge is working:
```bash
python test_sqli.py
```

**Expected terminal output:**
```
1. Initializing DB...
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>

2. Trying to register as 'admin' (Should fail/reject)...
Admin register rejected? True

3. Trying to login with wrong credentials...
Wrong login rejected? True

4. Trying SQL Injection (' OR 1=1 --)...
SUCCESS! Found flag in response:
<div class="flag">DAKSHH{sqli_3asy_byP4ss_2026}</div>
```

---

Contributor: Jyotirmoy Karmakar(0xjyotirmoy)
