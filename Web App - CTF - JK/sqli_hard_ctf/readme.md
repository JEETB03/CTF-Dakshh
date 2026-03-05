# SQL Injection CTF - Hard (500 Points)

**Difficulty:** Hard - "Anti-AI / Unicode Phantom" 
**Objective:** Bypass a perfect WAF by exploiting Python's Unicode Normalization to achieve an Authentication Bypass / Data Extraction SQL Injection.
**Flag Format:** `DAKSHH{flag}`

## Admin Guide
This is the final and hardest challenge in the SQLi series. It is a highly specific "Anti-AI" challenge designed to defeat static code analysis tools and automated solvers like `sqlmap` or standard LLMs.

### The "Anti-AI" Mechanism:
The application's Web Application Firewall (`waf()`) flawlessly blocks all standard SQL injection characters: `'`, `"`, `;`, `UNION`, `SELECT`, `--`. It is seemingly impossible to inject SQL directly.

However, the application uses Python's `unicodedata.normalize('NFKC', user_input)` *after* the WAF check, but *before* formatting the SQL string.
Automated tools almost never test for Unicode translation bypasses unless explicitly programmed to do so for a specific framework.

**The Exploit:** The player must send a "Fullwidth Apostrophe" (`＇` which is Unicode `U+FF07`).
1. The WAF checks `＇`. It looks completely different from `'`, so the WAF allows it through.
2. The `normalize('NFKC')` function converts the fullwidth `＇` into a standard ASCII `'` (U+0027) because they are visually compatible.
3. The normalized string is passed into the SQL format: `SELECT value FROM config WHERE key = '{normalized_key}'`. The newly formed standard apostrophe breaks out of the string!

### Deployment & Verification
1.  **Dependencies:** Ensure requirements are installed. (e.g. `pip install flask`)
2.  **Start the Server:**
    ```bash
    python app.py
    ```
    The server will run on `http://0.0.0.0:5003`.
3.  **Verification:**
    Run the automated exploit script to ensure the challenge works correctly and the WAF is functioning as intended:
    ```bash
    python solve.py
    ```

---

## Player Guide

Welcome to the Restricted Vault Configuration portal.

We take security seriously here. Our Web Application Firewall (WAF) was formally verified and provably blocks *all* SQL injection attempts. We dare you to try and break it.

If you can read the `admin_note` configuration key, you get the flag.

### Hints:
- **Hint 1:** The WAF is perfect. It blocks all standard ASCII quotes (`'`). You cannot bypass the WAF directly.
- **Hint 2:** What happens to your input *after* the WAF but *before* the SQL query executes? Does the backend programming language (Python) process strings in any special way regarding character encodings or normalizations?
- **Hint 3:** Research "NFKC Unicode Normalization vulnerabilities". Is there a character that *looks* like an apostrophe but isn't mathematically equal to one until it gets normalized?

### Walkthrough / Solution
1. Intercept the POST request to `/` for looking up a key.
2. If you try `admin_note' OR '1'='1`, the WAF blocks it because it contains `'`.
3. Find the "Fullwidth Apostrophe" unicode character: `＇` (U+FF07) and the Fullwidth Equals Sign: `＝` (U+FF1D).
4. Send the payload: `＇ OR ＇a＇＝＇a`
5. The WAF ignores the fullwidth characters. Python's normalizer turns them into real ascii characters.
6. The query becomes: `SELECT value FROM config WHERE key = '' OR 'a'='a'`
7. The application returns the first row, which happens to be the `admin_note` containing the flag: `DAKSHH{un1c0d3_n0rm4l1z4t10n_sqli_ph4nt0m}`.

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
