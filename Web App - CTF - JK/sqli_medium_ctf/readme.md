# 🛡️ Synth-Filter Override — Blind SQLi CTF

**Category:** Web Application Security  
**Difficulty:** Medium (200 Points) — "Anti-AI"  
**Flag Format:** `DAKSHH{flag}`

> *"The corporation's public directory is protected by a strict Synth-Filter. It blocks almost every known logic operator, comparison symbol, and string slicing command. The admin's data is hidden in plain sight, but the AI watching the query won't let you ask direct questions. You have to ask the database to sort itself based on the truth... without ever saying '='."*

---

## Challenge Overview
This challenge introduces an interesting variation of **Blind SQLi**. It is specifically designed to confuse automated exploitation tools (like `sqlmap`) and AI chatbot assistants by aggressively blocking standard SQL injection keywords.

### The "Anti-AI" Mechanism:
The vulnerability rests in the `ORDER BY` clause: `SELECT id, username FROM users ORDER BY {sort_param}`. 
Normally, a hacker would exploit this using boolean comparisons with `SUBSTR()` and `=`. 
However, the **WAF explicitly blocks all of these**: `<`, `>`, `=`, `between`, `like`, `in`, `and`, `or`, `union`, `substr`, `char`, `ascii`, etc.

## Hints for Players
- **Hint 1:** The injection point is in the `ORDER BY` clause via the `?sort=` parameter. If you inject a SQL expression that evaluates to a number, the table will sort by that number.
- **Hint 2:** Since `=`, `<`, and `>` are blocked, you can't compare letters. Is there an SQLite built-in function that searches for a string inside another string and returns an integer (which you can use to sort) without needing an equals sign?
- **Hint 3:** Look into the `INSTR(string, substring)` function in SQLite.

---

## 🔧 How to Start the Challenge Room (Step-by-Step)

### Prerequisites
- **Python 3.x** installed

### Step 1: Install Python Dependencies
Open a terminal in the challenge directory and run:
```bash
pip install flask
```

### Step 2: Start the Web Server
Launch the Flask application:
```bash
python app.py
```
> **Note:** The server will automatically initialize the database `users.db` and seed the flag upon startup. It runs entirely on **http://127.0.0.1:5002**. No manual database setup is required!

### Step 3: Access the Challenge Room
Players can now open their browser and go to:
```
http://127.0.0.1:5002
```

### Step 4: Stop the Room (When Done)
Press `Ctrl + C` in the terminal where the server is running.

---

## 🔑 Writeup — How to Solve (Player Walkthrough)

### Step 1: Reconnaissance
1. Navigate to the application at `http://127.0.0.1:5002`.
2. The UI displays a User Directory table, with `admin` at the top by default (ID: 1).
3. The UI allows sorting by ID or Username using the `?sort=` GET parameter.

### Step 2: Formulate the Attack
1. We know the database is vulnerable in the `ORDER BY` clause.
2. We know the flag format for this competition is `DAKSHH{...}`. **This is our starting anchor. We don't have to guess the first 7 characters!**
3. We need to extract the flag character by character using Blind SQL Injection. But, the WAF blocks basic comparisons like `=`.
4. **The Bypass:** We use the SQLite `INSTR(string, substring)` function. It searches for a `substring` inside a `string`. 
    - If the `substring` **is found**, it returns the position (a number > 0).
    - If the `substring` **is NOT found**, it returns `0`.

### Step 3: Executing the Filter Override
How exactly do we guess the flag? By injecting `INSTR()` and telling the database to sort itself based on whether our guess is True or False.

Let's say we want to guess the first letter inside the braces. Is it an `a`?
We inject: `http://127.0.0.1:5002/?sort=INSTR(profile_data, 'DAKSHH{a')`

**What happens in the backend?**
- For all the normal guests, `DAKSHH{a` is NOT in their profile, so `INSTR()` returns `0`.
- For the admin, their hidden flag doesn't start with `DAKSHH{a` either, so their `INSTR()` also returns `0`.
- Because everyone resulted in `0`, the database falls back to its default sorting (by ID). The **admin stays at the very top**. Our guess (`a`) was wrong.

Now let's try injecting `w`:
`http://127.0.0.1:5002/?sort=INSTR(profile_data, 'DAKSHH{w')`

- Guests result in `0`.
- But for the admin, the string `DAKSHH{w` **IS FOUND** inside their data! So `INSTR()` returns `1`.
- The database sorts the results in ascending number order. Since `0` comes before `1`, all the guests are listed first. The admin (who scored a `1`) is pushed to the **very bottom of the HTML table**!

### Step 4: The Brute-Force Script
Doing this manually for a 30+ character flag would take forever. The intended solution is to write an automated Python script (using the `requests` library) that does this:
1. Loops through every letter in the alphabet and every number.
2. Sends the `?sort=` request to the server with `DAKSHH{` + the guessed character.
3. Checks the HTML response. If the `admin` row appears *after* the `guest` row, that means the admin dropped to the bottom!
4. It accepts that character as correct, adds it to the known flag string (e.g., `DAKSHH{w`), and starts looping to guess the next character (`DAKSHH{wa`, `DAKSHH{wb`, etc.).

By repeating this loop, the script slowly leaks out the entire flag, character by character, straight out of the database:
🏆 `DAKSHH{w4f_byp4ss_w1th0ut_c0mp4r1s0ns}`

---

## 🛡️ Admin Verification (Automated Test)

You can run the provided solver script to automatically verify the challenge is working and perfectly executes the aforementioned blind data dump:
```bash
python solve.py
```
This script will bypass the WAF and slowly dump the flag character by character directly in your terminal.

---
Contributor: Jyotirmoy Karmakar (0xjyotirmoy)
