# Web Treasure Hunt CTF - Hard (500 Points)

**Name:** 🩸 Phase III: The Turing Gate (Hard Web Hunt)
**Difficulty:** Hard - "Anti-AI / API Turing Test"
**Objective:** Bypass the Turing Test API puzzle by sending a specific sequence of HTTP requests. Then combine the Medium Flag Content with the Hard Fragment to construct the final winning flag.
**Flag Format:** `DAKSHH{medium_content_hard_fragment}`

## Admin Guide
This is the epic conclusion to the Web Treasure Hunt Trilogy, heavily styled with the "Crimson Grid" UI theme. This challenge moves away from web inspection and focuses directly on API sequence exploitation.

### The "Anti-AI" Mechanism:
The main puzzle is rendered as an inline styling SVG (`<svg> <text> <tspan>`). 
LLMs and basic DOM scrapers struggle immensely with spatial reasoning. An AI reading the source code will see a jumbled mess of `tspan` coordinates:
```xml
<tspan x="50" dy="0">OP</tspan>
<tspan x="75" dy="0">TI</tspan>...
```
A human looking at the browser simply reads: "OPTIONS /api/core", "Then PATCH it...", "Then GET the Fragment."
Furthermore, AIs are notoriously bad at piecing together multi-step HTTP request sequences (OPTIONS -> PATCH -> GET) if they can't natively test them in real-time, relying on human operators to execute the commands.

There are also highly realistic decoy flags (e.g., `DAKSHH{4p1_c0r3_1n1t14l_t0k3n_x9}`) hidden in the HTML source to trap bot scanners before they figure out the API sequence.

Direct route bypassing has been closed. Hitting the `/submit` endpoint directly via GET will throw an explicit **[ UNAUTHORIZED ACCESS ]** template page until the player officially solves the challenge.

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

### Full Detailed Walkthrough / Solution

**Step 1: Analyzing the Core UI**
1. You land on the homepage `http://127.0.0.1:5006/`. The visual interface consists of the "Crimson Grid".
2. You will notice a fragmented, glitchy text box in the middle of the screen. 
3. If you right-click the page and "Inspect Element", you will see the text is actually composed of broken `<tspan>` tags inside an `<svg>` element. This is deliberately designed to break automated scrapers and bots trying to scrape hints from `<p>` tags.
4. If you read the text visually (like a human), it spells out a sequence:
   * **Line 1:** `OPTIONS /api/core`
   * **Line 2:** `Then PATCH it...`
   * **Line 3:** `Then GET the Fragment.`
5. This reveals you need to interact with a hidden API endpoint (`/api/core`) using specific HTTP methods. You cannot do this through a standard web browser click; you must use a terminal (`curl`) or a tool like Postman/Burp Suite.

**Step 2: The OPTIONS Request**
1. An `OPTIONS` request is used to ask a server what HTTP methods are supported at a specific endpoint. 
2. Open your terminal and run the following curl command:
   ```bash
   curl -X OPTIONS http://127.0.0.1:5006/api/core -v
   ```
   *Note: the `-v` (verbose) flag is crucial here so you can see the response headers.*
3. Looking closely at the output headers, you will see a custom, non-standard header returned by the server:
   `X-Configuration-Required: Send PATCH request with JSON: {"status":"ready"}`
4. This tells you exactly how to execute the second step in the sequence.

**Step 3: The PATCH Request (Synchronizing the Core)**
1. A `PATCH` request is typically used to apply partial modifications to a resource.
2. Based on the hint from the `OPTIONS` header, you need to send a JSON payload.
3. Run the following curl command:
   ```bash
   curl -X PATCH -H "Content-Type: application/json" -d '{"status":"ready"}' http://127.0.0.1:5006/api/core -c cookies.txt -v
   ```
   *Note: We added `-c cookies.txt` because we need to save the session cookie the server returns for the next step.*
4. The server responds with:
   ```json
   {"message": "Core synchronized. Proceed to GET."}
   ```
   And it sets a crucial authentication cookie: `Set-Cookie: core_session=synchronized`.

**Step 4: The GET Request (Extracting the Fragment)**
1. Now that your session is "synchronized", you can finally execute the third step of the visual puzzle.
2. You must send a `GET` request, and you *must* include the cookie from the previous step.
3. Run the following curl command:
   ```bash
   curl -X GET -b cookies.txt http://127.0.0.1:5006/api/core
   ```
4. The server verifies your cookie and successfully returns the final piece of the puzzle:
   ```json
   {
       "fragment_name": "Hard Fragment",
       "fragment_value": "h4rd_fr4gm3nt_b0ss",
       "instruction": "Combine this with the content inside the Medium Flag to craft the final flag.",
       "success": true
   }
   ```

**Step 5: Constructing the Final Flag**
1. The JSON instruction tells you to combine the content of the Medium challenge flag with this new fragment.
2. If you successfully completed Phase II (Medium Web Hunt), your flag was: `DAKSHH{css_gh0st_m3d1um}`
3. The content inside the brackets is: `css_gh0st_m3d1um`
4. The fragment you just got is: `h4rd_fr4gm3nt_b0ss`
5. Combine them using an underscore as requested in typical flag formats:
   `css_gh0st_m3d1um_h4rd_fr4gm3nt_b0ss`
6. Wrap it in the official prefix:
   `DAKSHH{css_gh0st_m3d1um_h4rd_fr4gm3nt_b0ss}`

**Step 6: Winning the Challenge**
1. Return to the homepage `http://127.0.0.1:5006/` in your browser.
2. Paste the final combined flag `DAKSHH{css_gh0st_m3d1um_h4rd_fr4gm3nt_b0ss}` into the "Combine Terminal" input box.
3. Click "EXECUTE INJECTION".
4. You will be successfully routed to the `[ SYSTEM OVERRIDE SUCCESS ]` / `ACCESS GRANTED` screen, officially beating the Web Treasure Hunt Trilogy!

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
