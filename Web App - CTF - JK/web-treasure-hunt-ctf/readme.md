# Web Treasure Hunt CTF - Easy (100 Points)

**Difficulty:** Easy
**Objective:** Follow a sequence of Hinglish hints through various endpoints, decode a base64 string for credentials, and exploit a simple command injection vulnerability to read the flag.
**Flag Format:** `DAKSHH{flag}`

## Admin Guide
This is the first part of the "Web Treasure Hunt Trilogy". 

### Updates for 2026 / Anti-AI
- The hints have been translated from Tamil to Hinglish/Hindi logic.
- **Anti-AI Feature:** The HTML source code is littered with fake flags (e.g., `DAKSHH{f4ke_fl4g...}`). Automated scanners and web-scraping LLMs often blindly grab these strings if asked to look for flags. A human player will easily ignore them as they follow the actual logic path.

### Deployment & Setup
1. **Dependencies:**
   ```bash
   pip install flask
   ```
2. **Start Server:**
   ```bash
   python app.py
   ```
   The server runs on `http://0.0.0.0:5004`.
3. **Verification:**
   Run the solver script to verify the sequence works from start to finish.
   ```bash
   python solve.py
   ```

---

## Player Guide

Welcome to the Web Treasure Hunt! Follow the clues hidden in plain sight. Keep your eyes open.

### Hints:
- **Hint 1:** The source code often contains developer comments.
- **Hint 2:** `429` is the HTTP status code for "Too Many Requests".
- **Hint 3:** Base64 encoding ends with `=` padding sometimes. Use CyberChef or a terminal to decode it.
- **Hint 4:** For the final path, try entering system commands like `ls` to see what files are in the directory.

### Walkthrough / Solution
1. Visit the homepage `/`. 
   - Observe the hints: "Subah uthte hi sabse pehle (in short)" -> `gm` and "Jo hamare liye jaan de de (hindi)" -> `dost`. 
   - Navigate to `/gmdost`.
2. At `/gmdost`, the hint is about an SMS bomber and an error code to stop it. 
   - The HTTP status error code for "Too Many Requests" is `429`. 
   - Navigate to `/429`.
3. At `/429`, the source code comment says to login at `/yagf`.
   - Navigate to `/yagf`.
4. At `/yagf`, the HTML comment holds a Base64 string: `aHR0cDovL3RyYW5zZmVyLnNoLzFsZ0dibGMvbG9naW4udHh0`.
   - Decoding this points to a `login.txt` (the previous file), or you can just read `app.py` if testing locally. The credentials are `vn_daan_vararu` and `flag_find_panna_poraru`.
   - Logging in redirects to `/finalpath`.
5. At `/finalpath`, there is an input box for commands.
   - Enter `ls` to see files. Notice `flagpath`.
   - Enter `cat flagpath`. A hidden route is revealed: `/dshgfayiurhaejkhbdsajvn`.
6. Visit `/dshgfayiurhaejkhbdsajvn/<your_name>` to see the final flag: `DAKSHH{h1nglish_hunt_3asy}`.
7. **Keep this flag! You will need it to unlock the Medium Treasure Hunt.**

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
