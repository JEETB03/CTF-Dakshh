# Web Treasure Hunt CTF - Hard (500 Points)

**Difficulty:** Hard - "Anti-AI / API Turing Test"
**Objective:** Bypass the Turing Test API puzzle by sending a specific sequence of HTTP requests. Then combine the Medium Flag Content with the Hard Fragment to construct the final winning flag.
**Flag Format:** `DAKSHH{medium_content_hard_fragment}`

## Admin Guide
This is the epic conclusion to the Web Treasure Hunt Trilogy.

### The "Anti-AI" Mechanism:
The main puzzle is rendered as an inline styling SVG (`<svg> <text> <tspan>`). 
LLMs and basic DOM scrapers struggle immensely with spatial reasoning. An AI reading the source code will see a jumbled mess of `tspan` coordinates:
```xml
<tspan x="50" dy="0">OP</tspan>
<tspan x="75" dy="0">TI</tspan>...
```
A human looking at the browser simply reads: "OPTIONS /api/core", "Then PATCH it...", "Then GET the Fragment."
Furthermore, AIs are notoriously bad at piecing together multi-step HTTP request sequences if they can't natively test them in real-time.

### Deployment & Setup:
1. **Dependencies:** Ensure Flask is installed.
   ```bash
   pip install flask
   ```
2. **Start Server:**
   ```bash
   python app.py
   ```
   The server runs on `http://0.0.0.0:5006`.
3. **Verification:**
   Run the solver script to verify the API sequence works and the fragment is successfully extracted.
   ```bash
   python solve.py
   ```

---

## Player Guide

Welcome to The Final Lock.

Only human eyes can read the ancient runes to unlock the core. Machines will inevitably fail. 

### Hints:
- **Hint 1:** The image on the screen is not an image file. It's an SVG. Read the text carefully.
- **Hint 2:** The text instructs you to make specific HTTP requests (methods you don't normally use in a browser) to a specific endpoint (`/api/core`). Have your trusty `curl`, Postman, or Burp Suite ready.
- **Hint 3:** The first step is an `OPTIONS` request. Look closely at the response headers it gives you. It tells you exactly what to do next.
- **Hint 4:** The final flag expects you to combine the contents of the flag you got in the Medium challenge with the fragment you get here. If medium is `DAKSHH{abc}` and hard is `xyz`, the final string to submit is `DAKSHH{abc_xyz}`.

### Walkthrough / Solution
1. Visit the homepage `/`. Read the visual SVG puzzle:
   - `OPTIONS /api/core`
   - `Then PATCH it...`
   - `Then GET the Fragment.`
2. Send an `OPTIONS` request:
   `curl -X OPTIONS http://IP:5006/api/core -v`
   - The response includes a header: `X-Configuration-Required: Send PATCH request with JSON: {"status":"ready"}`
3. Send the `PATCH` request as instructed:
   `curl -X PATCH -H "Content-Type: application/json" -d '{"status":"ready"}' http://IP:5006/api/core -v`
   - The response says "Core synchronized" AND sets a cookie: `Set-Cookie: core_session=synchronized`
4. Send the final `GET` request, making sure to include the cookie you just received:
   `curl -X GET -b "core_session=synchronized" http://IP:5006/api/core`
   - The JSON response reveals the fragment: `{"fragment_value": "h4rd_fr4gm3nt_b0ss"}`
5. Construct the final flag.
   - You found the Medium flag earlier: `DAKSHH{css_gh0st_m3d1um}`
   - Extract its content: `css_gh0st_m3d1um`
   - Combine it with the hard fragment using an underscore: `DAKSHH{css_gh0st_m3d1um_h4rd_fr4gm3nt_b0ss}`.
6. Submit this string via the terminal on the homepage to win!

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
