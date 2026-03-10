# 🏴‍☠️ Cyber-Quest – Challenges Repository

Welcome to the **Cyber-Quest Challenge Series**. This repository contains a collection of custom-built challenges categorized by domain.

---

**Contributor:** JEET BISWAS (JEETB03)


## 🌐 Web Exploitation Series

### Theme: *"The Web is a Lie."*

The **Polus Space Agency** has reported unusual behavior in several of their internal web systems. Logs indicate the presence of an unknown hacker group leaving cryptic references to hackers, vigilantes, pop stars, and… impostors. Your task is to investigate these web applications and recover the hidden flags.

Throughout the Web challenges, you will encounter subtle references to:
- 👨‍💻 **Mr. Robot**
- 🦇 **Batman / Wayne Enterprises**
- 🎶 **Alysa Liu – Stateside**
- 👨‍🚀 **Among Us**

**Challenges included:**
1. **Impostor in the DOM** (Easy) - Cross-Site Scripting (XSS)
2. **Wayne Enterprises Data Leak** (Easy/Medium) - Insecure Direct Object Reference (IDOR) via API
3. **Stateside Intercept** (Medium) - JWT Manipulation (`alg: none`)
4. **Mr. Robot's Archive Heist** (Hard) - Advanced Directory Traversal / LFI

All flags follow the format: `DAKSHH{example_flag_here}`

---

**Contributor:** JEET BISWAS (JEETB03)


## 🔐 Crypto Challenge Series

Welcome to the **Cyber-Quest Crypto Series**. These cryptography challenges focus on breaking realistic encryption implementations using thematic, pop-culture-inspired scenarios. 

Each challenge includes a player-facing `dist/` folder containing redacted source code and the exact output files.

**Challenges included:**
1. **Neo's Broken RNG** (Easy) - C++
    - *Theme*: The Matrix
    - *Concept*: Single-byte XOR key recovery via Known Plaintext Attack (KPA).
2. **Sherlock's Cipher Notebook** (Medium) - Java
    - *Theme*: Sherlock Holmes
    - *Concept*: Reused One-Time Pad (Many-Time Pad) vulnerability requiring crib-dragging.
3. **Cyberpunk Secure Broadcast** (Hard) - Python
    - *Theme*: Cyberpunk
    - *Concept*: RSA Broadcast Attack (Håstad's) exploiting a small public exponent ($e=3$).

All flags follow the format: `DAKSHH{example_flag_here}`

---

**Contributor:** Nabhonil Bhattacharjee (nabhocharger69)

Welcome to the **Cyber-Quest Reverse Engineering Series**. This section contains high-difficulty reverse engineering challenges designed to test your understanding of:

- Low-level program logic  
- LLVM IR analysis  
- XOR-based transformations  
- ASCII manipulation  
- Compiler-level thinking  

These are not brute-force challenges.  
They reward patience, structure, and deep reasoning.

**Challenges included:**
1. **Last Words of the Hacker** (Medium)
    - *Concept*: XOR-based transformations
2. **Are You Better Than Assembly?** (Hard)
    - *Concept*: LLVM IR / XOR / String manipulation

### 🛠 Recommended Tools
- Ghidra  
- IDA / Binary Ninja  
- clang (for compiling `.ll` files)  
- CyberChef  
- Python (for XOR analysis)  

### ⚠️ Rules
- No brute forcing.
- No patch-and-pray.
- No guessing flags.

Reverse it properly.

### 🧠 Final Advice
If you see:
- Static byte arrays  
- Suspicious modulo loops  
- XOR operations  
- Decoy output paths  

You’re on the right track.

Good luck.
*The compiler is watching.*

---

**Contributor:** Jyotirmoy Karmakar (0xjyotirmoy)

## 🌐 Web Exploitation Series (Extended)

These web challenges cover a wide spectrum of vulnerabilities — from classic SQL injection to advanced Anti-AI mechanisms designed to defeat automated scanners and LLMs. Each challenge includes detailed setup instructions, a step-by-step solving walkthrough, and an automated solve script for verification.

**Challenges included:**
1. **Authentication Bypass – Phantom Login** (Easy) - SQL Injection
    - *Concept*: Classic SQLi authentication bypass on a SQLite-backed login form.
2. **Blind SQL Injection – Advanced WAF Bypass** (Medium) [*Anti-AI*]
    - *Concept*: Blind SQLi via `ORDER BY` + `INSTR()` function to extract data while evading a keyword-based WAF.
3. **SQL Injection – Unicode Phantom** (Hard) [*Anti-AI*]
    - *Concept*: Unicode Normalization (`NFKC`) bypass — fullwidth apostrophe `＇` passes WAF, then normalizes to `'` on the backend.
4. **Web Treasure Hunt** (Easy) [*Anti-AI*]
    - *Concept*: Hinglish-hint reconnaissance with fake flag traps, Base64 decoding, and command injection.
5. **Web Treasure Hunt – CSS Ghost** (Medium) [*Anti-AI*]
    - *Concept*: All hints rendered via CSS `::after` pseudo-elements — invisible to `curl` and DOM scrapers.
6. **Web Treasure Hunt – Turing Test API** (Hard) [*Anti-AI*]
    - *Concept*: SVG-obfuscated instructions leading to a strict `OPTIONS → PATCH → GET` API sequence with state-dependent cookies.
7. **Reflective XSS Cookie Steal** (Medium)
    - *Concept*: WAF bypass using `<svg/onload=...>`, Puppeteer admin bot simulation, cookie exfiltration.
8. **Host Header Injection** (Medium)
    - *Concept*: Password Reset Poisoning via spoofed `Host` header to steal admin reset tokens.

All flags follow the format: `DAKSHH{example_flag_here}`

---

**Contributor:** Jyotirmoy Karmakar (0xjyotirmoy)

## 🔐 Crypto Challenge Series (Extended)

**Challenges included:**
1. **Quantum Steps** (Medium) - Python
    - *Theme*: Discrete Logarithm
    - *Concept*: Baby-step Giant-step algorithm to solve a DLP and recover the AES decryption key for the encrypted flag.

All flags follow the format: `dakshh{example_flag_here}`

---

**Contributor:** JEET BISWAS (JEETB03)

## 🕵️‍♂️ Misc Challenges

Cyberpunk hacker-themed narrative challenges involving various data analysis skills.

**Challenges included:**
1. **The Last Beacon** (Easy)
    - *Theme*: Morse Code / Signal Analysis
2. **Glitched Identity** (Easy)
    - *Theme*: QR Code Recovery / Error Correction
3. **Poisoned Intelligence** (Medium)
    - *Theme*: AI Data Poisoning / Dataset Inspection

These unique challenges have an alternative flag format: `dakshh{example_flag_here}`

---

**Contributor:** HARSH RAJ (Harshraj9142)

## 🔎 OSINT Challenge Series

Open-Source Intelligence challenges that test your ability to gather information from images, maps, and public databases to uncover hidden details.

**Challenges included:**
1. **Bike Shop Mystery** (Easy)
    - *Concept*: Image analysis / geo-location / storefront identification to find a bike shop's contact number in Kyoto, Japan.
2. **Holiday Bus Investigation** (Easy)
    - *Concept*: Political poster geo-location / Google Maps Street View / vehicle registration database lookup in Roskilde, Denmark.

All flags follow the format: `dakshh{example_flag_here}`

---

**Contributor:** HARSH RAJ (Harshraj9142)

## 🧩 Mixed Challenge Series

Browser-based challenges combining web exploitation, cryptography, and OSINT skills in thematic, multi-stage scenarios.

**Challenges included:**
1. **Time Travel Room** (Easy/Medium)
    - *Theme*: Cyberpunk / Time Travel
    - *Concept*: localStorage manipulation to fake a 365-day login streak, followed by Caesar Cipher decryption using an OSINT-derived shift key.
2. **Guest Cookie Paradox** (Easy)
    - *Theme*: Cookie Forgery / Reconnaissance
    - *Concept*: Base64 cookie decoding and forgery for privilege escalation, followed by a Caesar Cipher challenge with the shift key hidden in `robots.txt`.

All flags follow the format: `dakshh{example_flag_here}`

---

## 🛡️ Platform Security & Anti-Cheat

The Cyber-Quest platform includes custom features to ensure a fair and secure competitive environment.

### Anti-Cheat
- **Speed Run Prevention**: Impossibly fast flag submissions are rejected. Time calculations mandate a natural progression period based on the challenge's difficulty (e.g., 2 mins per 100 points).
- **Penalty Brute Force System**: Teams attempting 10 consecutive incorrect flags on a specific challenge incur a **30-minute lockout** and negative **10-point score deduction**.
- **Team-Based Model**: Scores are mapped dynamically to Team Names preventing standalone user score inflation.

### Frontend Protections
- **Strict Content Security Policy (CSP)**: Ensures inline Javascript, malicious `eval()`, and unknown external CDNs cannot execute to prevent Cross-Site Scripting (XSS).
- **DOM Sanitization**: Leaderboards securely inject usernames as standard text content natively preventing Stored XSS vectors in user inputs.
- **Anti-CSRF Logic**: The `/api/submit` endpoint incorporates a session-scoped secure UUID token system validating identical origins to prevent Request Forgery.
- **Tampering Shields**: Keyboard shortcuts for DevTools (F12) and context menus are administratively disabled.
