# Authentication Bypass (Phantom Login)

**Difficulty:** Easy
**Objective:** Perform a basic SQL Authentication Bypass to log in as `admin`.
**Flag Format:** `DAKSHH{flag}`

## Overview
This is a classic introductory SQL Injection challenge. The application concatenates user string input directly into the SQL query used for authentication. 

## Hints for Players
- **Hint 1**: Have you tried logging in as `admin`? The application might be trusting your input too much.
- **Hint 2**: What happens if you try to make the password check true no matter what? Try an input like `' OR '1'='1`.

## Exploitation Path (Walkthrough)
1.  Navigate to the login page.
2.  The backend query looks roughly like: `select * from users where username='{user}' and password='{pwd}';`
3.  To bypass the login for the `admin` user, enter `admin` as the username.
4.  For the password, enter `' OR 1=1 --`.
5.  This changes the query to: `select * from users where username='admin' and password='' OR 1=1 --';`
6.  The `--` comments out the rest of the query, and `1=1` ensures the `WHERE` clause always evaluates to True.
7.  The application will log you in as `admin` and immediately reveal the flag: `DAKSHH{sqli_3asy_byP4ss_2026}`.

---

## Technical Details (For Admins) & Room Setup

### Architecture
- **`app.py`**: A Flask server backed by an SQLite database.
- **`test_sqli.py`**: An automated exploit script proving the vulnerability.

### Deployment & Verification
1.  **Dependencies:** Ensure requirements are installed. (e.g. `pip install flask`)
2.  **Start the Server:**
    ```bash
    python app.py
    ```
    This will launch the Web App on port 5001.
3.  **Database Intialization:** 
    Before players can solve it, visit the hidden route `http://localhost:5001/iusdyfuhu` via Browser or `curl` to initialize the SQLite database tables and insert the `admin` user.
4. **Verification:**
    Run the automated exploit script to ensure the challenge works correctly:
    ```bash
    python test_sqli.py
    ```

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
