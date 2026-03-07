# 🕶️ Phase II: CSS Phantom Protocol (Medium Web Hunt)

**Category:** Web Application Security  
**Difficulty:** Medium (200 Points)  
**Flag Format:** `DAKSHH{flag}`

> *"You shattered the perimeter in Phase I. Now you face the Abyss Protocol. The Gatekeeper demands the master key you acquired previously. The shadows here hide their secrets not in the code itself, but in the rendering of the simulation. Can you see what the machines cannot?"*

---

## Challenge Overview
This is the second installment of the "Web Treasure Hunt Trilogy." Here, the core concept revolves around defeating automated scanning tools and AI web scrapers.

### Anti-AI / Trap Mechanisms
- **CSS Ghost Rendering:** Most scripts and LLM DOM parsers look for raw text hidden in `<p>` tags, `<!-- comments -->`, or JavaScript objects. In this room, **THERE ARE NO HINTS IN THE HTML**. The hints and passwords are dynamically injected into the browser's view using CSS pseudo-elements (`::before` / `::after` content).
- **Decoy Flags:** The actual HTML source is heavily trapped with realistic-looking decoy flags (e.g., `DAKSHH{5h4d0w_r34lm_4cc3ss_t0k3n_v1}`). "Lazy" players running automated regex scans will submit these flags and fail. Only a human reading the visuals rendered by the browser (or a human inspecting the CSS explicitly) can progress.

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
Launch the Flask application for Phase II:
```bash
python app.py
```
> **Note:** The server runs on **http://127.0.0.1:5005** (Port 5005).

### Step 3: Access the Challenge Room
Players open their browser and go to:
```
http://127.0.0.1:5005
```

### Step 4: Stop the Room (When Done)
Press `Ctrl + C` in the terminal where the server is running.

---

## 🔑 Writeup — How to Solve (Player Walkthrough)

### Phase 1: The Gatekeeper
1. Navigate to the application at `http://127.0.0.1:5005`.
2. You are immediately blocked by an authorization form demanding a sequence key. The hint text warns: *"Entry requires the master key acquired from the Easy Web Treasure Hunt..."*
3. You must paste the final flag obtained from the previous room.
4. Paste exactly: `DAKSHH{h1nglish_hunt_3asy}` and click **AUTHORIZE**.
5. You successfully bypass the Gatekeeper and enter `/stage1`.

### Phase 2: The Blind Spot (Defeating the Decoy)
1. You land on `Stage_01`. The visible text on the page says:
   *"Aankhein khuli par dikhta kuch nahi. (Eyes open but nothing is seen) - Search for the 'hidden_shadow' in the URL."*
2. **The Trap:** If you right-click the page and select "View Source", you will notice the text you just read is *nowhere* to be found in the raw HTML!
3. Instead, the HTML source contains a decoy flag: `DAKSHH{st4g3_1_1n1t14l1z4t10n_k3y}`. Submitting this flag will result in failure.
4. **The "Aha!" Moment:** Look closely at the `<style>` block in the `<head>` of the HTML source. The actual hint text is being injected directly into the browser view using CSS:
   ```css
   .puzzle1::after { content: "Search for the 'hidden_shadow' in the URL."; }
   ```
5. Heeding the visual hint, attach `/hidden_shadow` to the root URL and press Enter.

### Phase 3: The Shadow Realm
1. You load `/hidden_shadow`. 
2. The glowing purple text on the screen reads: *"You found the shadow. The password for the lower vault is: k3y_m4st3r_2026"*.
3. Once again, checking the source code only reveals another fake trap (`DAKSHH{5h4d0w_r34lm_4cc3ss_t0k3n_v1}`). The real password was rendered via CSS.
4. Type `k3y_m4st3r_2026` into the decryption prompt and click **DECRYPT**.

### Phase 4: Vault Access
1. You are redirected to `/vault`.
2. The CSS Phantom strikes one last time. In large glowing cyan letters, the browser renders the final flag.
3. However, if you inspect the raw HTML source, all you find is `<div class="decoy-flag">DAKSHH{v4ult_4cc3ss_d3n13d_f4k3_b0t}</div>`.
4. The true flag must be copied directly from the visual page output (or manually extracted from the CSS `<style>` block):

🏆 `DAKSHH{css_gh0st_m3d1um}`

*Save this flag. It is the final cipher required to breach the upcoming Hard challenge!*

---

## 🛡️ Admin Verification (Automated Test)

You can run the provided solver script to automatically verify the entire logic flow works:
```bash
python solve.py
```
*(Note: Because the solver is a script, it manually looks for the flags in the HTML source text. This proves exactly why the CSS trick works perfectly against standard bots!)*

---
Contributor: Jyotirmoy Karmakar (0xjyotirmoy)
