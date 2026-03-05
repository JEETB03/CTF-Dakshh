# Web Treasure Hunt CTF - Medium (200 Points)

**Difficulty:** Medium - "Anti-AI / CSS Ghost"
**Objective:** Navigate the second stage of the treasure hunt. Requires the flag from the Easy challenge to begin.
**Flag Format:** `DAKSHH{flag}`

## Admin Guide
This is Part 2 of the Web Treasure Hunt Trilogy.

### The "Anti-AI" Mechanism:
Automated tools (like `curl`, `wget`, or standard LLM DOM scrapers) typically read the raw HTML text to find flags or hints. 
In this challenge, **there is zero hint text in the HTML DOM**. All hints are injected into the browser visually using CSS pseudo-elements (e.g., `.puzzle1::before { content: "Aankhein khuli par dikhta kuch nahi..."; }`).
A human opening the page in a browser will see the text perfectly normal. An AI scraping the HTML will see empty `<div>` tags and assume the page is blank, except for a fake flag explicitly planted in the HTML to trick bots.

### Deployment & Setup:
1. **Dependencies:** Ensure Flask is installed.
   ```bash
   pip install flask
   ```
2. **Start Server:**
   ```bash
   python app.py
   ```
   The server runs on `http://0.0.0.0:5005`.
3. **Verification:**
   Run the solver script to verify the application logic. The solver requires the hardcoded `EASY_FLAG` to authenticate.
   ```bash
   python solve.py
   ```

---

## Player Guide

Welcome to the Shadow Realm. You will need the key you proved worthy of in the first trial to even step foot in here.

### Hints:
- **Hint 1:** Are you using a terminal or an automated tool to read this page? You might want to use a real browser. The shadows hide from machines.
- **Hint 2:** "Aankhein khuli par dikhta kuch nahi..." - If you see a fake flag in the source code, you've fallen for the bot trap. Read the glowing green text on your screen.

### Walkthrough / Solution
1. Visit the homepage `/`. You are prompted for a Key.
2. Enter the flag from the Easy challenge: `DAKSHH{h1nglish_hunt_3asy}`.
3. You are redirected to `/stage1`.
4. If you view the source code, you'll see empty divs and a fake flag `DAKSHH{th1s_is_4_f4k3...}`. Ignore the source code.
5. Read the rendered page in the browser. The CSS reveals the hint: "Search for the 'hidden_shadow' in the URL."
6. Navigate to `/hidden_shadow`.
7. The CSS on this page reveals the vault password: `k3y_m4st3r_2026`.
8. Submit the password.
9. You are redirected to `/vault` where the CSS reveals the Medium Flag: `DAKSHH{css_gh0st_m3d1um}`.
10. **Save this flag! You will need it to combine with the Hard challenge fragment to win the series.**

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
