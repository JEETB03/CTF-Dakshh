# Blind SQL Injection - Advanced WAF Bypass

**Difficulty:** Medium - "Anti-AI" 
**Objective:** Perform a Blind SQL Injection in an `ORDER BY` clause to extract the flag from the `profile_data` column.
**Flag Format:** `DAKSHH{flag}`

## Overview
This challenge introduces an interesting variation of Blind SQLi. It is specifically designed to confuse automated exploitation tools (like sqlmap) and AI chatbot assistants.

### The "Anti-AI" Mechanism:
The vulnerability is an injection in the `ORDER BY` clause: `SELECT id, username FROM users ORDER BY {sort_param}`. 
Normally, a script would exploit this using boolean comparisons (e.g., `ORDER BY (CASE WHEN (username='admin' AND substr(password,1,1)='H') THEN 1 ELSE 2 END)`). 
However, the **WAF blocks almost every single comparison operator and string function** typically used: `<`, `>`, `=`, `between`, `like`, `in`, `and`, `or`, `union`, `substr`, `char`, `ascii`, etc.

## Hints for Players
- **Hint 1:** The injection point is in the `ORDER BY` clause. If you inject a SQL expression that evaluates to a number, the table will sort by that number.
- **Hint 2:** Since `=`, `<`, and `>` are blocked, you can't compare letters. Is there a SQLite built-in function that searches for a string inside another string and returns an integer (which you can use to sort) without needing an equals sign?
- **Hint 3:** Look into the `INSTR(string, substring)` function in SQLite.

## Exploitation Path (Walkthrough)
1. Identify the injection endpoint: `?sort=id`
2. Since `INSTR(profile_data, 'DAKSHH{')` returns a positive integer (the index) if the string is found, and `0` if it is not found, we can sort by it!
3. To extract the flag letter by letter, you can use:
   `?sort=INSTR(profile_data, 'DAKSHH{w')`
4. If the letter is correct, the boolean expression evaluates to >0 (True). In ascending numerical order sort, the `0` (False) rows will come first, and the `>0` (True) row (the admin) will come last.
5. By iterating through the alphabet and observing how the 'admin' row shifts to the bottom of the HTML table response, a script can extract the flag without ever using an `=` or `SUBSTR` command.

---

## Technical Details (For Admins) & Room Setup

### Architecture
- **`app.py`**: A Flask server backed by an SQLite database. It auto-initializes `users.db` on startup and seeds the flag.
- **`solve.py`**: An automated exploit script proving the vulnerability.

### Deployment & Verification
1.  **Dependencies:** Ensure requirements are installed. (e.g. `pip install flask`)
2.  **Start the Server:**
    ```bash
    python app.py
    ```
    The server will run on `http://0.0.0.0:5002`.
3.  **Verification:**
    Run the automated exploit script to ensure the challenge works correctly and the WAF is functioning as intended:
    ```bash
    python solve.py
    ```

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
